""" Episode Mining """

import re
from typing import Dict, List, Text, Tuple

import pandas as pd

from spmf.base import Spmf


class Episode(Spmf):
    """ Base class for Episode Mining """

    def _transform_input_dataframe(self, input_df: pd.DataFrame) -> pd.DataFrame:
        """ Transform input dataframe to the format required by SPMF

        :param input_df: Input Dataframe containing Itemsets in 'Itemset' column
            NOTE: If Timestamp present, dataframe should contain it in 'Time points' column
        :return: Transformed dataframe
        """

        df = input_df.copy()

        if not self.timestamp_present:
            df = df.reset_index(names='Time points')
            self.timestamp_present = True       # override timestamp parameter

        if not self.transform:
            self.mapping = dict()
            return df

        df['Items'] = (input_df.groupby('Itemset').ngroup()+1).astype(str)
        self.mapping = df.set_index('Items', drop=True).to_dict()['Itemset']

        df = df.groupby('Time points').agg((' ').join).reset_index()
        return df.rename({'Items': 'Itemset', 'Itemset': 'Items'}, axis=1)

    def _parse_input_dataframe(self, input_df: pd.DataFrame) -> Text:
        """ Parse Input Dataframe to string format required for Episode Mining

        :param input_df: Input Dataframe containing Itemsets in 'Itemset' column
            NOTE: If Timestamp present, dataframe should contain it in 'Time points' column
        :return: Parsed String representation
        """
        df = self._transform_input_dataframe(input_df)
        df['input'] = df.apply(lambda x: '|'.join([x['Itemset'], str(x['Time points'])]), axis=1)
        return ('\n').join(df['input'].to_list())

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

    @staticmethod
    def map_pattern(pattern: Text, mapping: Dict[Text, Text]) -> Text:
        """ Re-map each word in pattern to the corresponding value in the mapping dictionary

        :param pattern: Pattern to map
        :param mapping: Dictionary with words in input pattern as key and corresponding substitution string as values
        :return: All words in pattern replaced by the corresponding value in mapping
            NOTE: Original word in pattern is retained if a matching key is not found in mapping
        """

        for p in re.findall(r'\d+', pattern):
            pattern = pattern.replace(p, mapping.get(p, p))

        return pattern

    def _create_output_dataframe(self, patterns: List[Text], supports: List[int]) -> pd.DataFrame:
        """ Create Output Dataframe

        :param patterns: Frequent Episode Patterns return by the episode mining algorithm
        :param supports: Corresponding supports for each pattern
        :return: Dataframe containing patterns and corresponding support
        """
        patterns_mapped = [self.map_pattern(pattern, self.mapping) for pattern in patterns]
        return pd.DataFrame((patterns_mapped, supports), index=['Frequent episode', 'Support']).T

    def run_pandas(self, input_df: pd.DataFrame) -> pd.DataFrame:
        """ Run Episode Mining algorithm on Pandas Dataframe

        :param input_df: Input Dataframe containing Itemsets in 'Itemset' column
            NOTE: If Timestamp present, dataframe should contain it in 'Time points' column
        :return: Dataframe containing the frequent episodes and support.
        """
        return super().run_pandas(input_df)

    def run_file(self, input_file_name: Text) -> Tuple[List[Text], List[int]]:
        """ Run Episode Mining algorithm on an input txt file

        :param input_file_name: Input txt file name
        :return: Tuple of frequent episode patterns and corresponding support
        """
        return super().run_file(input_file_name)


class EpisodeRules(Episode):
    """ Base class for Episode Rule Mining """

    def _parse_output_file(self, **kwargs) -> Tuple[List[Text], List[int], List[float]]:
        """ Parse output txt file created by the Episode Rule Mining algorithm

        :param kwargs: keyword arguments to read output file (delete)
        :return: Tuple of patterns and corresponding support and confidence
        """
        lines = self._read_file(**kwargs)
        patterns, supports, confidence = [], [], []
        for line in lines:
            line = line.strip().split('#')
            patterns.append(line[0].strip())
            supports.append(re.search(r'(\d+)$', line[1].strip()).group(0))
            confidence.append(re.search(r'([\d.]+)$', line[2].strip()).group(0))

        return patterns, list(map(int, supports)), list(map(float, confidence))

    def _create_output_dataframe(self, patterns: List[Text], supports: List[int], confidence: List[float]) -> pd.DataFrame:
        """ Create Output Dataframe

        :param patterns: Frequent Episode Rules returned by the episode rule mining algorithm
        :param supports: Corresponding supports for each rule
        :param confidence: Corresponding confidence for each rule
        :return: Dataframe containing patterns and corresponding support and confidence
        """
        patterns_mapped = [self.map_pattern(pattern, self.mapping) for pattern in patterns]
        return pd.DataFrame((patterns_mapped, supports, confidence), index=['Frequent episode', 'Support', 'Confidence']).T

    def run_pandas(self, input_df: pd.DataFrame) -> pd.DataFrame:
        """ Run Episode Mining algorithm on Pandas Dataframe

        :param input_df: Input Dataframe containing Itemsets in 'Itemset' column
            NOTE: If Timestamp present, dataframe should contain it in 'Time points' column
        :return: Dataframe containing the frequent episodes and support.
        """
        return super().run_pandas(input_df)

    def run_file(self, input_file_name: Text) -> Tuple[List[Text], List[int], List[float]]:
        """ Run Episode Mining algorithm on an input txt file

        :param input_file_name: Input txt file name
        :return: Tuple of frequent episode patterns and corresponding support and confidence
        """
        return super().run_file(input_file_name)


class TKE(Episode):
    """ Mining The Top-K Frequent Episodes In A Complex Event Sequence Using The TKE Algorithm """

    def __init__(self, k: int, max_window: int, timestamp_present: bool = False, **kwargs) -> None:
        """ Initialize Object. Refer to https://www.philippe-fournier-viger.com/spmf/TKEepisodes.php

        :param k: (a positive integer) indicating the number of episodes to find
        :param max_window: maximum window length
        :param timestamp_present: Bool indicating if timestamp is present
        :param kwargs: Keyword arguments to base SPMF. (transform, memory and executable_path)
        """
        super().__init__(**kwargs)

        self.k = k
        self.max_window = max_window
        self.timestamp_present = timestamp_present

    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """

        arguments = {
            'Subprocess': 'java',
            'Memory': f'-Xmx{self.memory}m',
            'Binary_Format': '-jar',
            'Binary_File': self.executable_path,
            'Command': 'run',
            'Algorithm': 'TKE',
            'Input': input_file_name,
            'Output': self.output_file_name,
            'K': str(self.k),
            'max_window': str(self.max_window),
            'Timestamp': str(not self.timestamp_present)
        }

        return list(arguments.values())


class TKERules(EpisodeRules):
    """ Mining Episode Rules In A Complex Sequence Using The TKE Algorithm """

    def __init__(self, k: int, max_window: int, timestamp_present: bool = False, min_confidence: float = 0.5, max_consequent_count: int = 1, min_support: int = 2, **kwargs) -> None:
        """ Initialize Object. Refer to https://www.philippe-fournier-viger.com/spmf/standard_episode_rules.php

        :param k: (a positive integer) indicating the number of episodes to find
        :param max_window: maximum window length
        :param timestamp_present: Bool indicating if timestamp is present
        :param min_confidence: minimum confidence level
        :param max_consequent_count: max consequent
        :param min_support: minimum occurrence frequency
        :param kwargs: Keyword arguments to base SPMF. (transform, memory and executable_path)
        """
        super().__init__(**kwargs)

        self.k = k
        self.max_window = max_window
        self.timestamp_present = timestamp_present
        self.min_confidence = min_confidence
        self.max_consequent_count = max_consequent_count
        self.min_support = min_support

    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """

        arguments = {
            'Subprocess': 'java',
            'Memory': f'-Xmx{self.memory}m',
            'Binary_Format': '-jar',
            'Binary_File': self.executable_path,
            'Command': 'run',
            'Algorithm': 'TKE-Rules',
            'Input': input_file_name,
            'Output': self.output_file_name,
            'K': str(self.k),
            'max_window': str(self.max_window),
            'Timestamp': str(not self.timestamp_present),
            'min_confidence': str(self.min_confidence),
            'max_consequent_event': str(self.max_consequent_count),
            'min_support': str(self.min_support)
        }

        return list(arguments.values())


class EMMA(Episode):
    """ Mining Frequent Episodes In A Complex Event Sequence Using The EMMA Algorithm """

    def __init__(self, min_support: int, max_window: int, timestamp_present: bool = False, **kwargs) -> None:
        """ Initialize Object. Refer to https://www.philippe-fournier-viger.com/spmf/EMMA.php

        :param min_support: minimum occurence frequency
        :param max_window: maximum window length
        :param timestamp_present: Bool indicating if timestamp is present
        :param kwargs: Keyword arguments to base SPMF. (transform, memory and executable_path)
        """
        super().__init__(**kwargs)

        self.min_support = min_support
        self.max_window = max_window
        self.timestamp_present = timestamp_present

    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """

        arguments = {
            'Subprocess': 'java',
            'Memory': f'-Xmx{self.memory}m',
            'Binary_Format': '-jar',
            'Binary_File': self.executable_path,
            'Command': 'run',
            'Algorithm': 'EMMA',
            'Input': input_file_name,
            'Output': self.output_file_name,
            'min_support': str(self.min_support),
            'max_window': str(self.max_window),
            'Timestamp': str(not self.timestamp_present)
        }

        return list(arguments.values())


class EMMARules(EpisodeRules):
    """ Mining Episode Rules In A Complex Sequence Using the EMMA Algorithm """

    def __init__(self, min_support: int, max_window: int, timestamp_present: bool = False, min_confidence: float = 0.5, max_consequent_count: int = 1, **kwargs) -> None:
        """ Initialize Object. Refer to https://www.philippe-fournier-viger.com/spmf/standard_episode_rules.php

        :param min_support: minimum occurence frequency
        :param max_window: maximum window length
        :param timestamp_present: Bool indicating if timestamp is present
        :param kwargs: Keyword arguments to base SPMF. (transform, memory and executable_path)
        """
        super().__init__(**kwargs)

        self.min_support = min_support
        self.max_window = max_window
        self.timestamp_present = timestamp_present
        self.min_confidence = min_confidence
        self.max_consequent_count = max_consequent_count

    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """

        arguments = {
            'Subprocess': 'java',
            'Memory': f'-Xmx{self.memory}m',
            'Binary_Format': '-jar',
            'Binary_File': self.executable_path,
            'Command': 'run',
            'Algorithm': 'EMMA-Rules',
            'Input': input_file_name,
            'Output': self.output_file_name,
            'min_support': str(self.min_support),
            'max_window': str(self.max_window),
            'Timestamp': str(not self.timestamp_present),
            'min_confidence': str(self.min_confidence),
            'max_consequent_event': str(self.max_consequent_count),
        }

        return list(arguments.values())


class AFEM(Episode):
    """ Mining Frequent Episodes In A Complex Event Sequence Using The AFEM Algorithm """

    def __init__(self, min_support: int, max_window: int, timestamp_present: bool = False, **kwargs) -> None:
        """ Initialize Object. Refer to https://www.philippe-fournier-viger.com/spmf/AFEM_temporal.php

        :param min_support: minimum occurence frequency
        :param max_window: maximum window length
        :param timestamp_present: Bool indicating if timestamp is present
        :param kwargs: Keyword arguments to base SPMF. (transform, memory and executable_path)
        """
        super().__init__(**kwargs)

        self.min_support = min_support
        self.max_window = max_window
        self.timestamp_present = timestamp_present

    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """

        arguments = {
            'Subprocess': 'java',
            'Memory': f'-Xmx{self.memory}m',
            'Binary_Format': '-jar',
            'Binary_File': self.executable_path,
            'Command': 'run',
            'Algorithm': 'AFEM',
            'Input': input_file_name,
            'Output': self.output_file_name,
            'Min_Support': str(self.min_support),
            'max_window': str(self.max_window),
            'Timestamp': str(not self.timestamp_present)
        }

        return list(arguments.values())


class MaxFEM(Episode):
    """ Mining Maximal Frequent Episodes In A Complex Event Sequence Using The MaxFEM Algorithm """

    def __init__(self, min_support: int, max_window: int, timestamp_present: bool = False, **kwargs) -> None:
        """ Initialize Object. Refer to https://www.philippe-fournier-viger.com/spmf/MAXFEM_MAXIMAL_EPISODE_MINING.php

        :param min_support: minimum occurence frequency
        :param max_window: maximum window length
        :param timestamp_present: Bool indicating if timestamp is present
        :param kwargs: Keyword arguments to base SPMF. (transform, memory and executable_path)
        """
        super().__init__(**kwargs)

        self.min_support = min_support
        self.max_window = max_window
        self.timestamp_present = timestamp_present

    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """

        arguments = {
            'Subprocess': 'java',
            'Memory': f'-Xmx{self.memory}m',
            'Binary_Format': '-jar',
            'Binary_File': self.executable_path,
            'Command': 'run',
            'Algorithm': 'MaxFEM',
            'Input': input_file_name,
            'Output': self.output_file_name,
            'Min_Support': str(self.min_support),
            'max_window': str(self.max_window),
            'Timestamp': str(not self.timestamp_present)
        }

        return list(arguments.values())


class NONEPI(EpisodeRules):
    """ Mining Episode Rules In A Complex Sequence With The Non-Overlapping Frequency Using The NONEPI Algorithm """

    def __init__(self, min_support: int, min_confidence: float = 0.5, **kwargs) -> None:
        """ Initialize Object. Refer to https://www.philippe-fournier-viger.com/spmf/NONEPI_episode_rules.php

        :param min_support: minimum occurence frequency
        :param max_window: maximum window length
        :param timestamp_present: Bool indicating if timestamp is present
        :param kwargs: Keyword arguments to base SPMF. (transform, memory and executable_path)
        """
        super().__init__(**kwargs)

        self.min_support = min_support
        self.min_confidence = min_confidence
        self.timestamp_present = True   # Requires timestamps

    def _create_subprocess_arguments(self, input_file_name: Text) -> List:
        """ Create arguments list to pass to subprocess """

        arguments = {
            'Subprocess': 'java',
            'Memory': f'-Xmx{self.memory}m',
            'Binary_Format': '-jar',
            'Binary_File': self.executable_path,
            'Command': 'run',
            'Algorithm': 'NONEPI',
            'Input': input_file_name,
            'Output': self.output_file_name,
            'min_support': str(self.min_support),
            'min_confidence': str(self.min_confidence),
        }

        return list(arguments.values())
