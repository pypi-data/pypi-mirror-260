""" Test Suite for Episode Mining algorithms """

import os
import re

import pandas as pd

from spmf.seq_pat import (CMSPADE, NOSEP, SPADE, SPAM, TKS, VGEN, VMSP, ClaSP,
                          CMClaSP, PrefixSpan)

test_file_path = os.path.join('tests', 'test_files', 'contextPrefixSpan.txt')
nosep_test_file_path = os.path.join('tests', 'test_files', 'contextNOSEP.txt')


def create_mock_raw_dataframe() -> pd.DataFrame:
    """ Create raw mock dataframe """
    return pd.DataFrame({
        'ID': ['S1']*9 + ['S2']*7 + ['S3']*8 + ['S4']*7,
        'Time Points': [0, 1, 1, 1, 2, 2, 3, 4, 4, 5, 5, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 13, 14, 15, 16, 16, 17, 18, 19],
        'Items': ['a', 'a', 'b', 'c', 'a', 'c', 'd', 'c', 'f', 'a', 'd', 'c', 'b', 'c', 'a', 'e', 'e', 'f', 'a', 'b', 'd', 'f', 'c', 'b', 'e', 'g', 'a', 'f', 'c', 'b', 'c'],
    })


def create_mock_raw_dataframe_nosep() -> pd.DataFrame:
    """ Create raw mock dataframe """
    return pd.DataFrame({
        'ID': ['S1']*16,
        'Time Points': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        'Items': ['A', 'A', 'G', 'T', 'A', 'C', 'G', 'A', 'C', 'G', 'C', 'A', 'T', 'C', 'T', 'A'],
    })


def test_prefixspan_file() -> None:
    """ Test PrefixSpan on given example in
        https://www.philippe-fournier-viger.com/spmf/PrefixSpan.php
    """
    prefixspan = PrefixSpan(min_support=0.5)
    patterns, support = prefixspan.run_file(test_file_path)
    assert len(patterns) > 0 and len(support) > 0
    assert all(x in set(patterns) for x in {'2 3 -> 1', '6 -> 2', '6 -> 2 -> 3'})

    prefixspan = PrefixSpan(min_support=0.5, max_pattern_length=3)
    patterns, support = prefixspan.run_file(test_file_path)
    assert all(len(pattern.split('->')) <= 3 for pattern in patterns)


def test_prefixspan_pandas() -> None:
    """ Test PrefixSpan on given example in
        https://www.philippe-fournier-viger.com/spmf/PrefixSpan.php
    """
    prefixspan = PrefixSpan(min_support=0.5)
    mock_df = create_mock_raw_dataframe()
    output = prefixspan.run_pandas(mock_df)
    assert len(output) > 0
    assert all(x in output['Frequent sequential pattern'].to_list() for x in {'b c -> a', 'f -> b', 'f -> b -> c'})


def test_spade_file() -> None:
    """ Test SPADE on given example in
        https://www.philippe-fournier-viger.com/spmf/SPADE.php
    """
    spade = SPADE(min_support=0.5)
    patterns, support = spade.run_file(test_file_path)
    assert len(patterns) > 0 and len(support) > 0
    assert all(x in set(patterns) for x in {'2 3 -> 1', '6 -> 2', '6 -> 2 -> 3'})


def test_spade_pandas() -> None:
    """ Test SPADE on given example in
        https://www.philippe-fournier-viger.com/spmf/SPADE.php
    """
    spade = SPADE(min_support=0.5)
    mock_df = create_mock_raw_dataframe()
    output = spade.run_pandas(mock_df)
    assert len(output) > 0
    assert all(x in output['Frequent sequential pattern'].to_list() for x in {'b c -> a', 'f -> b', 'f -> b -> c'})


def test_cmspade_file() -> None:
    """ Test SPADE on given example in
        https://www.philippe-fournier-viger.com/spmf/CM-SPADE.php
    """
    cmspade = CMSPADE(min_support=0.5)
    patterns, support = cmspade.run_file(test_file_path)
    assert len(patterns) > 0 and len(support) > 0
    assert all(x in set(patterns) for x in {'2 3 -> 1', '6 -> 2', '6 -> 2 -> 3'})


def test_cmspade_pandas() -> None:
    """ Test SPADE on given example in
        https://www.philippe-fournier-viger.com/spmf/CM-SPADE.php
    """
    cmspade = CMSPADE(min_support=0.5)
    mock_df = create_mock_raw_dataframe()
    output = cmspade.run_pandas(mock_df)
    assert len(output) > 0
    assert all(x in output['Frequent sequential pattern'].to_list() for x in {'b c -> a', 'f -> b', 'f -> b -> c'})


def test_spam_file() -> None:
    """ Test SPAM on given example in
        https://www.philippe-fournier-viger.com/spmf/SPAM.php
    """
    spam = SPAM(min_support=0.5)
    patterns, support = spam.run_file(test_file_path)
    assert len(patterns) > 0 and len(support) > 0
    assert all(x in set(patterns) for x in {'2 3 -> 1', '6 -> 2', '6 -> 2 -> 3'})

    spam = SPAM(min_support=0.5, min_pattern_length=3)
    patterns, support = spam.run_file(test_file_path)
    assert all(len(re.split(r'\s|->', pattern)) >= 3 for pattern in patterns)


def test_spam_pandas() -> None:
    """ Test SPAM on given example in
        https://www.philippe-fournier-viger.com/spmf/SPAM.php
    """
    spam = SPAM(min_support=0.5)
    mock_df = create_mock_raw_dataframe()
    output = spam.run_pandas(mock_df)
    assert len(output) > 0
    assert all(x in output['Frequent sequential pattern'].to_list() for x in {'b c -> a', 'f -> b', 'f -> b -> c'})


def test_clasp_file() -> None:
    """ Test ClaSP on given example in
        https://www.philippe-fournier-viger.com/spmf/ClaSP.php
    """
    clasp = ClaSP(min_support=0.5)
    patterns, support = clasp.run_file(test_file_path)
    assert len(patterns) > 0 and len(support) > 0
    assert all(x in set(patterns) for x in {'1 2 -> 4 -> 3', '1 2 -> 6', '1 -> 2 -> 3'})


def test_clasp_pandas() -> None:
    """ Test ClaSP on given example in
        https://www.philippe-fournier-viger.com/spmf/ClaSP.php
    """
    clasp = ClaSP(min_support=0.5)
    mock_df = create_mock_raw_dataframe()
    output = clasp.run_pandas(mock_df)
    assert len(output) > 0
    assert all(x in output['Frequent sequential pattern'].to_list()
               for x in {'a b -> d -> c', 'a b -> f', 'a -> b -> c'})


def test_cmclasp_file() -> None:
    """ Test CM-ClaSP on given example in
        https://www.philippe-fournier-viger.com/spmf/CM-ClaSP.php
    """
    cmclasp = CMClaSP(min_support=0.5)
    patterns, support = cmclasp.run_file(test_file_path)
    assert len(patterns) > 0 and len(support) > 0
    assert all(x in set(patterns) for x in {'1 2 -> 4 -> 3', '1 2 -> 6', '1 -> 2 -> 3'})


def test_cmclasp_pandas() -> None:
    """ Test CM-ClaSP on given example in
        https://www.philippe-fournier-viger.com/spmf/CM-ClaSP.php
    """
    cmclasp = CMClaSP(min_support=0.5)
    mock_df = create_mock_raw_dataframe()
    output = cmclasp.run_pandas(mock_df)
    assert len(output) > 0
    assert all(x in output['Frequent sequential pattern'].to_list()
               for x in {'a b -> d -> c', 'a b -> f', 'a -> b -> c'})


def test_vmsp_file() -> None:
    """ Test VMSP on given example in
        https://www.philippe-fournier-viger.com/spmf/VMSP.php
    """
    vmsp = VMSP(min_support=0.5)
    patterns, support = vmsp.run_file(test_file_path)
    assert len(patterns) > 0 and len(support) > 0
    assert all(x in set(patterns) for x in {'4 -> 3 -> 2', '5 -> 6 -> 3 -> 2', '5 -> 1 -> 3 -> 2'})

    vmsp = VMSP(min_support=0.5, max_pattern_length=3)
    patterns, support = vmsp.run_file(test_file_path)
    print(patterns)
    assert all(len(pattern.split('->')) <= 3 for pattern in patterns)


def test_vmsp_pandas() -> None:
    """ Test VMSP on given example in
        https://www.philippe-fournier-viger.com/spmf/VMSP.php
    """
    vmsp = VMSP(min_support=0.5)
    mock_df = create_mock_raw_dataframe()
    output = vmsp.run_pandas(mock_df)
    assert len(output) > 0
    assert all(x in output['Frequent sequential pattern'].to_list()
               for x in {'d -> c -> b', 'e -> f -> c -> b', 'e -> a -> c -> b'})


def test_vgen_file() -> None:
    """ Test VGEN on given example in
        https://www.philippe-fournier-viger.com/spmf/VGEN.php
    """
    vgen = VGEN(min_support=0.5)
    patterns, support = vgen.run_file(test_file_path)
    assert len(patterns) > 0 and len(support) > 0
    assert all(x in set(patterns) for x in {'6 -> 3', '3 -> 2', '1 -> 2 -> 3'})

    vgen = VGEN(min_support=0.5, max_pattern_length=3)
    patterns, support = vgen.run_file(test_file_path)
    print(patterns)
    assert all(len(pattern.split('->')) <= 3 for pattern in patterns)


def test_vgen_pandas() -> None:
    """ Test VGEN on given example in
        https://www.philippe-fournier-viger.com/spmf/VGEN.php
    """
    vgen = VGEN(min_support=0.5)
    mock_df = create_mock_raw_dataframe()
    output = vgen.run_pandas(mock_df)
    assert len(output) > 0
    assert all(x in output['Frequent sequential pattern'].to_list() for x in {'f -> c', 'c -> b', 'a -> b -> c'})


def test_nosep_file() -> None:
    """ Test NOSEP on given example in
        https://www.philippe-fournier-viger.com/spmf/NOSEP.php
    """
    nosep = NOSEP(min_pattern_length=1, max_pattern_length=20, min_gap=0, max_gap=2, min_support=3)
    patterns, support = nosep.run_file(nosep_test_file_path)
    assert len(patterns) > 0 and len(support) > 0
    assert all(x in set(patterns) for x in {'1 -> 1 -> 7', '1 -> 7 -> 3 -> 3', '1 -> 1 -> 7 -> 1 -> 3 -> 1'})


def test_nosep_pandas() -> None:
    """ Test NOSEP on given example in
        https://www.philippe-fournier-viger.com/spmf/NOSEP.php
    """
    nosep = NOSEP(min_pattern_length=1, max_pattern_length=20, min_gap=0, max_gap=2, min_support=3)
    mock_df = create_mock_raw_dataframe_nosep()
    output = nosep.run_pandas(mock_df)
    assert len(output) > 0
    assert all(x in output['Frequent sequential pattern'].to_list()
               for x in {'A -> A -> G', 'A -> G -> C -> C', 'A -> A -> G -> A -> C -> A'})


def test_tks_file() -> None:
    """ Test TKS on given example in
        https://www.philippe-fournier-viger.com/spmf/TKS.php
    """
    tks = TKS(k=5)
    patterns, support = tks.run_file(test_file_path)
    assert len(patterns) == 5 and len(support) == 5
    assert all(x in set(patterns) for x in {'2', '1 -> 2', '1 -> 3', '3', '1'})


def test_tks_pandas() -> None:
    """ Test TKS on given example in
        https://www.philippe-fournier-viger.com/spmf/TKS.php
    """
    tks = TKS(k=5)
    mock_df = create_mock_raw_dataframe()
    output = tks.run_pandas(mock_df)
    assert len(output) > 0
    assert all(x in output['Frequent sequential pattern'].to_list()
               for x in {'b', 'a -> b', 'a -> c', 'c', 'a'})
