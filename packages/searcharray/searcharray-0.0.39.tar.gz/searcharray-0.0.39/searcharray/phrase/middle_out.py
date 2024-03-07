"""Encode positions in bits along with some neighboring information for wrapping.

See this notebook for motivation:

https://colab.research.google.com/drive/10tIEkdlCE_1J_CcgEcV0jkLfBc-0H4am?authuser=1#scrollTo=XWzy-n9dF3PG

"""
import numpy as np
import sortednp as snp
from copy import deepcopy
from typing import List, Tuple, Dict, Union, cast, Optional
from searcharray.utils.roaringish import RoaringishEncoder, convert_keys, sorted_unique
import numbers
import logging
from collections import defaultdict

from searcharray.utils.bitcount import bit_count64


logger = logging.getLogger(__name__)

# When running in pytest
import sys  # noqa
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.ERROR)
formatter = logging.Formatter("[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.ERROR)


encoder = RoaringishEncoder()

# To not constantly type coerce
_64 = np.uint64(64)
_2 = np.uint64(2)
_1 = np.uint64(1)
_0 = np.uint64(0)
_neg1 = np.int64(-1)

MAX_POSN = encoder.max_payload


def inner_bigram_freqs(lhs: np.ndarray, rhs: np.ndarray,
                       phrase_freqs: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Count bigram matches between two encoded arrays, within a 64 bit word with same MSBs.

    Returns:
    --------
    count: number of matches per doc
    rhs_next: the next rhs array to continue matching

    """
    lhs_int, rhs_int = encoder.intersect(lhs, rhs)
    lhs_doc_ids = encoder.keys(lhs_int)
    if len(lhs_int) != len(rhs_int):
        raise ValueError("Encoding error, MSBs apparently are duplicated among your encoded posn arrays.")
    if len(lhs_int) == 0:
        return phrase_freqs, rhs_int
    same_term = (len(lhs_int) == len(rhs_int) and lhs_int[0] == rhs_int[0])
    if same_term:
        # Find adjacent matches
        rhs_shift = rhs_int << _1
        overlap = lhs_int & rhs_shift
        overlap = encoder.payload_lsb(overlap)
        adjacents = bit_count64(overlap).astype(np.int64)
        adjacents -= -np.floor_divide(adjacents, -2)  # ceiling divide
        phrase_freqs[lhs_doc_ids] += adjacents
        return phrase_freqs, rhs_int

    overlap_bits = (lhs_int & encoder.payload_lsb_mask) & ((rhs_int & encoder.payload_lsb_mask) >> _1)
    rhs_next2 = (overlap_bits << _1) & encoder.payload_lsb_mask
    rhs_next2 |= (rhs_int & (encoder.key_mask | encoder.payload_msb_mask))
    phrase_freqs2 = phrase_freqs.copy()
    matches2 = overlap_bits > 0
    if np.any(matches2):
        transitions = np.argwhere(np.diff(lhs_doc_ids[matches2]) != 0).flatten() + 1
        transitions = np.insert(transitions, 0, 0)
        counted_bits = bit_count64(overlap_bits[matches2])
        reduced = np.add.reduceat(counted_bits,
                                  transitions)
        phrase_freqs2[np.unique(lhs_doc_ids[matches2])] += reduced
    return phrase_freqs2, rhs_next2


def adjacent_bigram_freqs(lhs: np.ndarray, rhs: np.ndarray,
                          phrase_freqs: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Count bigram matches between two encoded arrays where they occur in adjacent 64 bit words.

    Returns:
    --------
    count: number of matches per doc
    rhs_next: the next rhs array to continue matching

    """
    lhs_int, rhs_int = encoder.intersect_rshift(lhs, rhs, rshift=_neg1)
    lhs_doc_ids = encoder.keys(lhs_int)
    # lhs lsb set and rhs lsb's most significant bit set
    upper_bit = _1 << (encoder.payload_lsb_bits - _1)
    matches = ((lhs_int & upper_bit) != 0) & ((rhs_int & _1) != 0)
    unique, counts = np.unique(lhs_doc_ids[matches], return_counts=True)
    phrase_freqs[unique] += counts
    rhs_next = rhs_int
    rhs_next[~matches] |= ~encoder.payload_lsb_mask
    rhs_next[matches] |= (encoder.payload_lsb_mask & _1)
    return phrase_freqs, rhs_next


def bigram_freqs(lhs: np.ndarray, rhs: np.ndarray, phrase_freqs: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Count bigram matches between two encoded arrays.

    Returns:
    --------
    count: number of matches per doc
    rhs_next: the next rhs array to continue matching

    """
    # Combine lhs and rhs matches from two strategies
    phrase_freqs, rhs_next_inner = inner_bigram_freqs(lhs, rhs, phrase_freqs)
    phrase_freqs, rhs_next_adj = adjacent_bigram_freqs(lhs, rhs, phrase_freqs)
    rhs_next = np.sort(np.concatenate([rhs_next_inner, rhs_next_adj]))

    # Combine
    return phrase_freqs, rhs_next


def trim_phrase_search(encoded_posns: List[np.ndarray],
                       phrase_freqs: np.ndarray) -> List[np.ndarray]:
    """Trim long phrases by searching the rarest terms first."""

    # Start with rarest term
    shortest_keys = None
    shortest_idx = None
    min_len = 1e100
    max_len = 0
    for idx, enc_posn in enumerate(encoded_posns):
        if len(enc_posn) < min_len:
            shortest_keys = encoder.keys(enc_posn)
            shortest_idx = idx
            min_len = len(enc_posn)
        if len(enc_posn) > max_len:
            max_len = len(enc_posn)

    if shortest_keys is None:
        return encoded_posns

    for enc_posn_idx in range(len(encoded_posns)):
        if enc_posn_idx == shortest_idx:
            continue
        if len(encoded_posns[enc_posn_idx]) > (10 * min_len):
            encoded_posns[enc_posn_idx] = encoder.slice(encoded_posns[enc_posn_idx],
                                                        shortest_keys)

    return encoded_posns


def compute_phrase_freqs(encoded_posns: List[np.ndarray],
                         phrase_freqs: np.ndarray) -> np.ndarray:
    if len(encoded_posns) < 2:
        raise ValueError("phrase must have at least two terms")

    # Trim long phrases by searching the rarest terms first
    if len(encoded_posns) > 3:
        encoded_posns = trim_phrase_search(encoded_posns, phrase_freqs)

    mask = np.ones(len(phrase_freqs), dtype=bool)
    lhs = encoded_posns[0]
    for rhs in encoded_posns[1:]:
        # Only count the count of the last bigram (ignoring the ones where priors did not match)
        phrase_freqs[mask] = 0
        phrase_freqs, lhs = bigram_freqs(lhs, rhs, phrase_freqs)
        mask &= (phrase_freqs > 0)
    phrase_freqs[~mask] = 0
    return phrase_freqs


class PosnBitArrayFromFlatBuilder:
    """ Build from sorted array shape num terms x 3.

        0th is term id
        1st is doc id
        2nd is posn

        Sorted by term id then posns

    """

    def __init__(self, flat_array: np.ndarray):
        self.flat_array = flat_array

    def build(self):
        """Slice the flat array into a 2d array of doc ids and posns."""
        term_boundaries = np.argwhere(np.diff(self.flat_array[0]) > 0).flatten() + 1
        term_boundaries = np.concatenate([[0], term_boundaries, [len(self.flat_array[1])]])

        encoded, enc_term_boundaries = encoder.encode(keys=self.flat_array[1].view(np.uint64),
                                                      boundaries=term_boundaries[:-1],
                                                      payload=self.flat_array[2].view(np.uint64))
        term_ids = self.flat_array[0][term_boundaries[:-1]]

        encoded_term_posns = {}
        for into_terms, (beg_idx, end_idx) in enumerate(zip(enc_term_boundaries[:-1], enc_term_boundaries[1:])):
            sliced = encoded[beg_idx:end_idx]
            encoded_term_posns[term_ids[into_terms]] = sliced

        return PosnBitArray(encoded_term_posns, self.flat_array[1].max())


class PosnBitArrayBuilder:

    def __init__(self):
        self.term_posns = defaultdict(list)
        self.term_posn_doc_ids = defaultdict(list)
        self.max_doc_id = 0

    def add_posns(self, doc_id: int, term_id: int, posns: List[int]):
        doc_ids = [doc_id] * len(posns)
        self.term_posns[term_id].extend(posns)
        self.term_posn_doc_ids[term_id].extend(doc_ids)

    def ensure_capacity(self, doc_id):
        self.max_doc_id = max(self.max_doc_id, doc_id)

    def build(self, check=False):
        encoded_term_posns = {}
        for term_id, posns in self.term_posns.items():
            if len(posns) == 0:
                posns = np.asarray([], dtype=np.uint32).flatten()
            elif isinstance(posns, list):
                posns_arr = np.asarray(posns, dtype=np.uint32).flatten()
                posns = posns_arr
            doc_ids = self.term_posn_doc_ids[term_id]
            if isinstance(doc_ids, list):
                doc_ids = np.asarray(doc_ids, dtype=np.uint32)
            encoded = encoder.encode(keys=doc_ids, payload=posns)
            if check:
                decode_again = encoder.decode(encoded)
                docs_to_posns = dict(decode_again)
                doc_ids_again = []
                posns_again = []
                for doc_id, posns_dec in docs_to_posns.items():
                    for posn in posns_dec:
                        doc_ids_again.append(doc_id)
                        posns_again.append(posn)
                assert np.array_equal(doc_ids_again, doc_ids)
                assert np.array_equal(posns, posns_again)
            encoded_term_posns[term_id] = encoded

        return PosnBitArray(encoded_term_posns, self.max_doc_id)


class PosnBitArrayAlreadyEncBuilder:

    def __init__(self):
        self.encoded_term_posns = {}
        self.max_doc_id = 0

    def add_posns(self, doc_id: int, term_id: int, posns):
        self.encoded_term_posns[term_id] = posns

    def ensure_capacity(self, doc_id):
        self.max_doc_id = max(self.max_doc_id, doc_id)

    def build(self, check=False):
        return PosnBitArray(self.encoded_term_posns, self.max_doc_id)


def index_range(rng, key):
    if key is None:
        return rng
    if isinstance(rng, np.ndarray):
        return rng[key]

    if isinstance(key, slice):
        return rng[key]
    elif isinstance(key, numbers.Number):
        return rng[key]
    elif isinstance(key, np.ndarray):
        try:
            # UNFORTUNATE COPY
            r_val = np.asarray(list(rng))[key]
            return r_val
        except IndexError as e:
            raise e
    # Last resort
    # UNFORTUNATE COPY
    # Here probably elipses or a tuple of various things
    return np.asarray(list(rng))[key]


class PosnBitArray:

    def __init__(self, encoded_term_posns, max_doc_id: int):
        self.encoded_term_posns = encoded_term_posns
        self.max_doc_id = max_doc_id
        self.docfreq_cache : Dict[int, np.uint64] = {}
        self.termfreq_cache : Dict[int, Tuple[np.ndarray, np.ndarray]] = {}

    def warm(self):
        """Warm tf / df cache of most common terms."""
        for term_id, encoded in self.encoded_term_posns.items():
            if len(encoded) > 255:
                self.docfreq(term_id)
                self.termfreqs(term_id)

    def clear_cache(self):
        self.docfreq_cache = {}
        self.termfreq_cache = {}

    def copy(self):
        new = PosnBitArray(deepcopy(self.encoded_term_posns), self.max_doc_id)
        return new

    def concat(self, other):
        """Merge other into self.

        Assumes other's doc ids are not overlapping with self's doc ids.
        """
        # Shared terms
        shared_terms = set(self.encoded_term_posns.keys()).intersection(set(other.encoded_term_posns.keys()))
        for term_id in shared_terms:
            # Append then sort
            self.encoded_term_posns[term_id] = np.concatenate([self.encoded_term_posns[term_id], other.encoded_term_posns[term_id]])
            self.encoded_term_posns[term_id].sort()

        only_other_terms = set(other.encoded_term_posns.keys()).difference(set(self.encoded_term_posns.keys()))
        for term_id in only_other_terms:
            self.encoded_term_posns[term_id] = other.encoded_term_posns[term_id]
        self.max_doc_id = max(self.max_doc_id, other.max_doc_id)
        self.clear_cache()

    def slice(self, key):
        sliced_term_posns = {}
        doc_ids = convert_keys(key)
        max_doc_id = np.max(doc_ids)
        for term_id, posns in self.encoded_term_posns.items():
            encoded = self.encoded_term_posns[term_id]
            assert len(encoded.shape) == 1
            sliced_term_posns[term_id] = encoder.slice(encoded, keys=doc_ids)

        return PosnBitArray(sliced_term_posns, max_doc_id)

    def __getitem__(self, key):
        return self.slice(key)

    def merge(self, other):
        # Unique terms
        unique_terms = set(self.encoded_term_posns.keys()).union(set(other.encoded_term_posns.keys()))

        for term_id in unique_terms:
            if term_id not in other.encoded_term_posns:
                continue
            elif term_id not in self.encoded_term_posns:
                self.encoded_term_posns[term_id] = other.encoded_term_posns[term_id]
            else:
                posns_self = self.encoded_term_posns[term_id]
                posns_other = other.encoded_term_posns[term_id]
                self.encoded_term_posns[term_id] = snp.merge(posns_self, posns_other)
        self.max_doc_id = self.max_doc_id + other.max_doc_id
        self.clear_cache()

    def doc_encoded_posns(self, term_id: int, doc_id: int) -> np.ndarray:
        term_posns = encoder.slice(self.encoded_term_posns[term_id],
                                   keys=np.asarray([doc_id], dtype=np.uint64))
        return term_posns

    def phrase_freqs(self, term_ids: List[int], phrase_freqs: np.ndarray,
                     doc_ids: np.ndarray) -> np.ndarray:
        if len(term_ids) < 2:
            raise ValueError("Must have at least two terms")
        if phrase_freqs.shape[0] == self.max_doc_id + 1:
            enc_term_posns = [self.encoded_term_posns[term_id] for term_id in term_ids]
        else:
            enc_term_posns = [encoder.slice(self.encoded_term_posns[term_id],
                                            keys=doc_ids.view(np.uint64)) for term_id in term_ids]
        return compute_phrase_freqs(enc_term_posns, phrase_freqs)

    def positions(self, term_id: int, doc_ids) -> Union[List[np.ndarray], np.ndarray]:
        if isinstance(doc_ids, numbers.Number):
            doc_ids = np.asarray([doc_ids])

        try:
            np_doc_ids = convert_keys(doc_ids)
            term_posns = encoder.slice(self.encoded_term_posns[term_id],
                                       keys=np_doc_ids)
        except KeyError:
            r_val = [np.array([], dtype=np.uint32) for doc_id in doc_ids]
            if len(r_val) == 1 and len(doc_ids) == 1 and isinstance(doc_ids[0], numbers.Number):
                return [r_val[0]]
            return r_val

        decoded = encoder.decode(encoded=term_posns, get_keys=True)

        if len(decoded) == 0:
            return [np.array([], dtype=np.uint32)]
        if len(decoded) != len(doc_ids):
            # Fill non matches
            decoded = cast(List[Tuple[np.uint64, np.ndarray]], decoded)
            as_dict: Dict[np.uint64, np.ndarray] = dict(decoded)
            decs = []
            for doc_id in doc_ids:
                if doc_id in as_dict:
                    decs.append(as_dict[doc_id])
                else:
                    decs.append(np.array([], dtype=np.uint32))
            return decs
        else:
            decs = [dec[1] for dec in decoded]
            return decs

    def termfreqs(self, term_id: int, doc_ids: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray]:
        """Count term freqs using unique positions."""
        if doc_ids is None:
            return self._termfreqs_with_cache(term_id)

        encoded = self.encoded_term_posns[term_id]
        term_posns = encoded
        term_posns = encoder.slice(encoded,
                                   keys=doc_ids.astype(np.uint64))
        return self._computed_term_freqs(term_posns)

    def _computed_term_freqs(self, term_posns) -> Tuple[np.ndarray, np.ndarray]:
        doc_ids = encoder.keys(term_posns)
        change_indices = np.nonzero(np.diff(doc_ids))[0]
        change_indices = np.concatenate((np.asarray([0]), change_indices + 1))
        posns = term_posns & encoder.payload_lsb_mask
        bit_counts = bit_count64(posns)

        term_freqs = np.add.reduceat(bit_counts, change_indices, dtype=np.float32)
        return sorted_unique(doc_ids), term_freqs

    def _termfreqs_with_cache(self, term_id: int) -> Tuple[np.ndarray, np.ndarray]:
        try:
            return self.termfreq_cache[term_id]
        except KeyError:
            term_posns = self.encoded_term_posns[term_id]
            doc_ids, term_freqs = self._computed_term_freqs(term_posns)
            if self._is_cached(term_id):
                self.termfreq_cache[term_id] = (doc_ids, term_freqs)
            return doc_ids, term_freqs

    def _is_cached(self, term_id: int) -> bool:
        return term_id in self.docfreq_cache

    def _docfreq_from_cache(self, term_id: int) -> np.uint64:
        return self.docfreq_cache[term_id]

    def _maybe_cache_docfreq(self, term_id: int, docfreq: np.uint64):
        if self.max_doc_id >= 100000 and docfreq > (self.max_doc_id // 100):
            self.docfreq_cache[term_id] = docfreq

    def docfreq(self, term_id: int) -> np.uint64:
        try:
            return self.docfreq_cache[term_id]
        except KeyError:
            encoded = self.encoded_term_posns[term_id]
            docfreq = np.uint64(encoder.keys_unique(encoded).size)
            self._maybe_cache_docfreq(term_id, docfreq)
            return docfreq

    def insert(self, key, term_ids_to_posns, is_encoded=False):
        new_posns = PosnBitArrayBuilder()
        if is_encoded:
            new_posns = PosnBitArrayAlreadyEncBuilder()
        max_doc_id = 0
        for doc_id, new_posns_row in enumerate(term_ids_to_posns):
            for term_id, positions in new_posns_row:
                new_posns.add_posns(doc_id, term_id, positions)
            max_doc_id = max(doc_id, max_doc_id)
            new_posns.max_doc_id = max_doc_id
        ins_arr = new_posns.build()
        self.merge(ins_arr)

    @property
    def nbytes(self):
        arr_bytes = 0
        for doc_id, posn in self.encoded_term_posns.items():
            arr_bytes += posn.nbytes
        for term_id, (doc_ids, term_freqs) in self.termfreq_cache.items():
            arr_bytes += doc_ids.nbytes
            arr_bytes += term_freqs.nbytes
        for term_id, docfreq in self.docfreq_cache.items():
            arr_bytes += docfreq.nbytes
        return arr_bytes
