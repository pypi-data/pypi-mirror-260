""" Sequential Pattern Mining """

import re
import warnings
from typing import List, Text, Tuple

import pandas as pd

from spmf.base import Spmf


class SeqPat(Spmf):
    """ Base class for Sequential Pattern Mining """

    def _transform_input_dataframe(self, input_df: pd.DataFrame) -> pd.DataFrame:
        """ Transform input dataframe to the format required by SPMF

        :param input_df: Input Dataframe containing Sequences in 'Sequences' column
            NOTE: If Timestamp present, dataframe should contain it in 'Time points' column
        :return: Transformed dataframe
        """

        df = input_df.copy()

        df['Event_ID'] = (df.groupby('Items').ngroup()+1).astype(str)
        self.mapping = str.maketrans(df[['Items', 'Event_ID']].set_index('Event_ID', drop=True).to_dict()['Items'])

        return df.pipe(pd.DataFrame.groupby, by='Time Points') \
            .pipe(pd.core.groupby.generic.DataFrameGroupBy.agg, {'ID': 'first', 'Event_ID': (' ').join}) \
            .pipe(pd.DataFrame.reset_index) \
            .pipe(pd.DataFrame.groupby, by='ID') \
            .pipe(pd.core.groupby.generic.DataFrameGroupBy.agg, {'Event_ID': (' -1 ').join}) \
            .pipe(pd.DataFrame.reset_index) \
            .pipe(pd.DataFrame.rename, {'Event_ID': 'input'}, axis=1)

    def _parse_input_dataframe(self, input_df: pd.DataFrame) -> Text:
        """ Parse Input Dataframe to string format required for Sequential Pattern Mining

        :param input_df: Input Dataframe containing Sequence IDs in 'ID' column, time in
            'Time Points' column and items in 'Items' column.
            NOTE: Items in the same Itemset must have the same value in the 'Time Points' column
            NOTE: Items in the same sequence must have the same value in the 'ID' column
        :return: Parsed String representation
        """
        df = self._transform_input_dataframe(input_df)
        return (' -1 -2\n').join(df['input'].to_list()) + ' -1 -2'

    def _parse_output_file(self, **kwargs) -> Tuple[List[Text], List[int]]:
        """ Parse output txt file created by the Episode Mining algorithm

        :param kwargs: keyword arguments to read output file (delete)
        :return: Tuple of patterns and corresponding support
        """
        lines = self._read_file(**kwargs)
        patterns, supports = [], []

        for line in lines:
            line = line.strip().split('-1')
            patterns.append((' -> ').join([c.strip() for c in line[:-1]]))
            supports.append(re.search(r'(\d+)$', line[-1]).group(0))

        return patterns, list(map(int, supports))

    def _create_output_dataframe(self, patterns: List[Text], supports: List[int]) -> pd.DataFrame:
        """ Create Output Dataframe

        :param patterns: Frequent Episode Patterns return by the episode mining algorithm
        :param supports: Corresponding supports for each pattern
        :return: Dataframe containing patterns and corresponding support
        """
        patterns_mapped = [pattern.translate(self.mapping) for pattern in patterns]
        return pd.DataFrame((patterns_mapped, supports), index=['Frequent sequential pattern', 'Support']).T

    def run_pandas(self, input_df: pd.DataFrame) -> pd.DataFrame:
        """ Run Episode Mining algorithm on Pandas Dataframe

        :param input_df: Input Dataframe containing Sequence IDs in 'ID' column, time in
            'Time Points' column and items in 'Items' column.
            NOTE: Items in the same Itemset must have the same value in the 'Time Points' column
            NOTE: Items in the same sequence must have the same value in the 'ID' column
        :return: Dataframe containing the frequent sequential patterns and support.
        """
        return super().run_pandas(input_df)

    def run_file(self, input_file_name: Text) -> Tuple[List[Text], List[int]]:
        """ Run Episode Mining algorithm on an input txt file

        :param input_file_name: Input txt file name
        :return: Tuple of frequent sequential patterns and corresponding support
        """
        return super().run_file(input_file_name)


class PrefixSpan(SeqPat):
    """ Mining Frequent Sequential Patterns Using The PrefixSpan Algorithm """

    def __init__(self, min_support: float, max_pattern_length: int = None, show_seq_ids: bool = False, **kwargs) -> None:
        """ Initialize Object. Refer to https://www.philippe-fournier-viger.com/spmf/PrefixSpan.php

        :param min_support: minimum occurence frequency
        :param max_pattern_length (optional): maximum number of items that patterns found should contain
        :param show_seq_id (not implemented): Show sequence IDs for patterns in the output
        """
        super().__init__(**kwargs)
        self.min_support = min_support
        self.max_pattern_length = max_pattern_length if max_pattern_length else ''

        # TODO
        if show_seq_ids:
            warnings.warn('Sequence IDs in output not implemented. Ignoring argument.')

    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """

        arguments = {
            'Subprocess': 'java',
            'Memory': f'-Xmx{self.memory}m',
            'Binary_Format': '-jar',
            'Binary_File': self.executable_path,
            'Command': 'run',
            'Algorithm': 'PrefixSpan',
            'Input': input_file_name,
            'Output': self.output_file_name,
            'min_support': str(self.min_support),
            'max_pattern_length': str(self.max_pattern_length),
        }

        return list(arguments.values())


class SPADE(SeqPat):
    """ Mining Frequent Sequential Patterns Using The SPADE Algorithm """

    def __init__(self, min_support: float, show_seq_ids: bool = False, **kwargs) -> None:
        """ Initialize Object. Refer to https://www.philippe-fournier-viger.com/spmf/SPADE.php

        :param min_support: minimum occurence frequency
        :param show_seq_id (not implemented): Show sequence IDs for patterns in the output
        """
        super().__init__(**kwargs)
        self.min_support = min_support

        # TODO
        if show_seq_ids:
            warnings.warn('Sequence IDs in output not implemented. Ignoring argument.')

    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """

        arguments = {
            'Subprocess': 'java',
            'Memory': f'-Xmx{self.memory}m',
            'Binary_Format': '-jar',
            'Binary_File': self.executable_path,
            'Command': 'run',
            'Algorithm': 'SPADE',
            'Input': input_file_name,
            'Output': self.output_file_name,
            'min_support': str(self.min_support)
        }

        return list(arguments.values())


class CMSPADE(SeqPat):
    """ Mining Frequent Sequential Patterns Using The CM-SPADE Algorithm """

    def __init__(self, min_support: float, show_seq_ids: bool = False, **kwargs) -> None:
        """ Initialize Object. Refer to https://www.philippe-fournier-viger.com/spmf/CM-SPADE.php

        :param min_support: minimum occurence frequency
        :param show_seq_id (not implemented): Show sequence IDs for patterns in the output
        """
        super().__init__(**kwargs)
        self.min_support = min_support

        # TODO
        if show_seq_ids:
            warnings.warn('Sequence IDs in output not implemented. Ignoring argument.')

    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """

        arguments = {
            'Subprocess': 'java',
            'Memory': f'-Xmx{self.memory}m',
            'Binary_Format': '-jar',
            'Binary_File': self.executable_path,
            'Command': 'run',
            'Algorithm': 'CM-SPADE',
            'Input': input_file_name,
            'Output': self.output_file_name,
            'min_support': str(self.min_support)
        }

        return list(arguments.values())


class SPAM(SeqPat):
    """ Mining Frequent Sequential Patterns Using The SPAM Algorithm """

    def __init__(self, min_support: float, min_pattern_length: int = None, max_pattern_length: int = None, max_gap: int = None, show_seq_ids: bool = False, **kwargs) -> None:
        """ Initialize Object. Refer to https://www.philippe-fournier-viger.com/spmf/SPAM.php

        :param min_support: minimum occurence frequency
        :param min_pattern_length (optional): minimum pattern length in the output. Default = 1
        :param max_pattern_length (optional): maximum pattern length in the output. Default = +inf
        :param max_gap (optional): maximum gap allowed between consecutive itemsets in the pattern. Default = +inf
        :param show_seq_id (not implemented): Show sequence IDs for patterns in the output
        """
        super().__init__(**kwargs)
        self.min_support = min_support
        self.min_pattern_length = min_pattern_length if min_pattern_length else ''
        self.max_pattern_length = max_pattern_length if max_pattern_length else ''
        self.max_gap = max_gap if max_gap else ''

        # TODO
        if show_seq_ids:
            warnings.warn('Sequence IDs in output not implemented. Ignoring argument.')

    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """

        arguments = {
            'Subprocess': 'java',
            'Memory': f'-Xmx{self.memory}m',
            'Binary_Format': '-jar',
            'Binary_File': self.executable_path,
            'Command': 'run',
            'Algorithm': 'SPAM',
            'Input': input_file_name,
            'Output': self.output_file_name,
            'min_support': str(self.min_support),
            'min_pattern_length': str(self.min_pattern_length),
            'max_pattern_length': str(self.max_pattern_length),
            'max_gap': str(self.max_gap)
        }

        return list(arguments.values())


class ClaSP(SeqPat):
    """ Mining Frequent Closed Sequential Patterns Using The ClaSP Algorithm """

    def __init__(self, min_support: float, show_seq_ids: bool = False, **kwargs) -> None:
        """ Initialize Object. Refer to https://www.philippe-fournier-viger.com/spmf/ClaSP.php

        :param min_support: minimum occurence frequency
        :param show_seq_id (not implemented): Show sequence IDs for patterns in the output
        """
        super().__init__(**kwargs)
        self.min_support = min_support

        # TODO
        if show_seq_ids:
            warnings.warn('Sequence IDs in output not implemented. Ignoring argument.')

    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """

        arguments = {
            'Subprocess': 'java',
            'Memory': f'-Xmx{self.memory}m',
            'Binary_Format': '-jar',
            'Binary_File': self.executable_path,
            'Command': 'run',
            'Algorithm': 'ClaSP',
            'Input': input_file_name,
            'Output': self.output_file_name,
            'min_support': str(self.min_support)
        }

        return list(arguments.values())


class CMClaSP(SeqPat):
    """ Mining Frequent Closed Sequential Patterns Using The CM-ClaSP Algorithm """

    def __init__(self, min_support: float, show_seq_ids: bool = False, **kwargs) -> None:
        """ Initialize Object. Refer to https://www.philippe-fournier-viger.com/spmf/CM-ClaSP.php

        :param min_support: minimum occurence frequency
        :param show_seq_id (not implemented): Show sequence IDs for patterns in the output
        """
        super().__init__(**kwargs)
        self.min_support = min_support

        # TODO
        if show_seq_ids:
            warnings.warn('Sequence IDs in output not implemented. Ignoring argument.')

    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """

        arguments = {
            'Subprocess': 'java',
            'Memory': f'-Xmx{self.memory}m',
            'Binary_Format': '-jar',
            'Binary_File': self.executable_path,
            'Command': 'run',
            'Algorithm': 'CM-ClaSP',
            'Input': input_file_name,
            'Output': self.output_file_name,
            'min_support': str(self.min_support)
        }

        return list(arguments.values())


class VMSP(SeqPat):
    """ Mining Frequent Maximal Sequential Patterns Using The VMSP Algorithm """

    def __init__(self, min_support: float, max_pattern_length: int = None, max_gap: int = None, show_seq_ids: bool = False, **kwargs) -> None:
        """ Initialize Object. Refer to https://www.philippe-fournier-viger.com/spmf/VMSP.php

        :param min_support: minimum occurence frequency
        :param max_pattern_length (optional): maximum pattern length in the output. Default = +inf
        :param max_gap (optional): maximum gap allowed between consecutive itemsets in the pattern. Default = +inf
        :param show_seq_id (not implemented): Show sequence IDs for patterns in the output
        """
        super().__init__(**kwargs)
        self.min_support = min_support
        self.max_pattern_length = max_pattern_length if max_pattern_length else ''
        self.max_gap = max_gap if max_gap else ''

        # TODO
        if show_seq_ids:
            warnings.warn('Sequence IDs in output not implemented. Ignoring argument.')

    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """

        arguments = {
            'Subprocess': 'java',
            'Memory': f'-Xmx{self.memory}m',
            'Binary_Format': '-jar',
            'Binary_File': self.executable_path,
            'Command': 'run',
            'Algorithm': 'VMSP',
            'Input': input_file_name,
            'Output': self.output_file_name,
            'min_support': str(self.min_support),
            'max_pattern_length': str(self.max_pattern_length),
            'max_gap': str(self.max_gap)
        }

        return list(arguments.values())


class VGEN(SeqPat):
    """ Mining Frequent Sequential Generator Patterns Using The VGEN Algorithm """

    def __init__(self, min_support: float, max_pattern_length: int = None, max_gap: int = None, show_seq_ids: bool = False, **kwargs) -> None:
        """ Initialize Object. Refer to https://www.philippe-fournier-viger.com/spmf/VGEN.php

        :param min_support: minimum occurence frequency
        :param max_pattern_length (optional): maximum pattern length in the output. Default = +inf
        :param max_gap (optional): maximum gap allowed between consecutive itemsets in the pattern. Default = +inf
        :param show_seq_id (not implemented): Show sequence IDs for patterns in the output
        """
        super().__init__(**kwargs)
        self.min_support = min_support
        self.max_pattern_length = max_pattern_length if max_pattern_length else ''
        self.max_gap = max_gap if max_gap else ''

        # TODO
        if show_seq_ids:
            warnings.warn('Sequence IDs in output not implemented. Ignoring argument.')

    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """

        arguments = {
            'Subprocess': 'java',
            'Memory': f'-Xmx{self.memory}m',
            'Binary_Format': '-jar',
            'Binary_File': self.executable_path,
            'Command': 'run',
            'Algorithm': 'VGEN',
            'Input': input_file_name,
            'Output': self.output_file_name,
            'min_support': str(self.min_support),
            'max_pattern_length': str(self.max_pattern_length),
            'max_gap': str(self.max_gap)
        }

        return list(arguments.values())


class NOSEP(SeqPat):
    """ Mining Nonoverlapping Sequential Patterns In One Or Many Sequences Using The NOSEP Algorithm """

    def __init__(self, min_support: float, min_pattern_length: int = 1, max_pattern_length: int = 20, min_gap: int = 0, max_gap: int = 2, **kwargs) -> None:
        """ Initialize Object. Refer to https://www.philippe-fournier-viger.com/spmf/NOSEP.php

        :param min_support: minimum occurence frequency
        :param min_pattern_length (optional): minimum pattern length in the output. Default = 1
        :param max_pattern_length (optional): maximum pattern length in the output. Default = 20
        :param min_gap (optional): minimum gap allowed between consecutive itemsets in the pattern. Default = 0
        :param max_gap (optional): maximum gap allowed between consecutive itemsets in the pattern. Default = 2
        """
        super().__init__(**kwargs)
        self.min_support = min_support
        self.min_pattern_length = min_pattern_length
        self.max_pattern_length = max_pattern_length
        self.min_gap = min_gap
        self.max_gap = max_gap

    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """

        arguments = {
            'Subprocess': 'java',
            'Memory': f'-Xmx{self.memory}m',
            'Binary_Format': '-jar',
            'Binary_File': self.executable_path,
            'Command': 'run',
            'Algorithm': 'NOSEP',
            'Input': input_file_name,
            'Output': self.output_file_name,
            'min_pattern_length': str(self.min_pattern_length),
            'max_pattern_length': str(self.max_pattern_length),
            'min_gap': str(self.min_gap),
            'max_gap': str(self.max_gap),
            'min_support': str(self.min_support),
        }

        return list(arguments.values())


class TKS(SeqPat):
    """ Mining Top-K Sequential Patterns Using The TKS Algorithm """

    def __init__(self, k: int, min_pattern_length: int = None, max_pattern_length: int = None, required_items: List[int] = None, max_gap: int = None, **kwargs) -> None:
        """ Initialize Object. Refer to https://www.philippe-fournier-viger.com/spmf/TKS.php

        :param k: number of patterns to output
        :param min_pattern_length (optional): minimum pattern length in the output. Default = 1
        :param max_pattern_length (optional): maximum pattern length in the output. Default = +inf
        :param max_gap (optional): maximum gap allowed between consecutive itemsets in the pattern. Default = +inf
        :param required_items (not implemented): list of items that must appears in every patterns found
        """
        super().__init__(**kwargs)
        self.k = k
        self.min_pattern_length = min_pattern_length if min_pattern_length else ''
        self.max_pattern_length = max_pattern_length if max_pattern_length else ''
        self.max_gap = max_gap if max_gap else ''

        # TODO
        if required_items:
            warnings.warn('Required items in output not implemented. Ignoring argument.')

    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """

        arguments = {
            'Subprocess': 'java',
            'Memory': f'-Xmx{self.memory}m',
            'Binary_Format': '-jar',
            'Binary_File': self.executable_path,
            'Command': 'run',
            'Algorithm': 'TKS',
            'Input': input_file_name,
            'Output': self.output_file_name,
            'k': str(self.k),
            'min_pattern_length': str(self.min_pattern_length),
            'max_pattern_length': str(self.max_pattern_length),
            'required_items': '',
            'max_gap': str(self.max_gap),
        }

        return list(arguments.values())
