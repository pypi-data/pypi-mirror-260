#  Copyright (C) 2023 Y Hsu <yh202109@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public license as published by
#  the Free software Foundation, either version 3 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details
#
#  You should have received a copy of the GNU General Public license
#  along with this program. If not, see <https://www.gnu.org/license/>

import csv
import glob
import os
import re
import pandas as pd
from mtbp3.util.lsr import LsrTree
import mtbp3
import numpy as np


class Emt:
    """A class representing MedDRA terms.

    This class provides methods to interact with the Emt object,
    including listing files associated with the Emt.

    Attributes:
        folder_name (str): The folder name associated with the Emt.
        lsr (LsrTree): An instance of the LsrTree class for listing files.
        month (str): The month of the version published.
        year (str): The year of the version published.
    """


    def __init__(self, folder_name=''):
        """
        Initialize a new Emt object.

        Args:
            folder_name (str, optional): The folder name associated with the Emt.
                If not provided, the default folder name will be used.
        """
        if folder_name:
            self.folder_name = folder_name
        else:
            self.folder_name = mtbp3.get_data('test_emt/MedDRA')

        self.version_number = "00.0"
        self.version_number_us = "00_0"
        self.readme_file = None
        self.year = ""
        self.month = ""
        self.language = ""
        self.mdhier = None
        self.llt = None
        self.smq_list = None
        self.smq_content = None

        meddra_release_file = os.path.join(self.folder_name, 'MedAscii', 'meddra_release.asc')
        if os.path.isfile(meddra_release_file):
            with open(meddra_release_file, 'r') as file:
                reader = csv.reader(file, delimiter='$')
                header = next(reader)
                self.version_number = header[0]
                self.version_number_us = self.version_number.replace(".", "_")
                self.language = header[1]
        else:
            raise FileNotFoundError("meddra_release.asc file not found.")

        pattern = os.path.join(self.folder_name, '!!readme_[1-3][0-9]_[0-1]_English.txt')
        files = glob.glob(pattern, recursive=False)
        if len(files) == 1:
            self.readme_file = files[0]
        else:
            raise ValueError("Readme file not found or multiple files found.")

        with open(self.readme_file, 'r') as file:
            lines = file.readlines()[-3:]
            for line in lines:
                match = re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\b \d{4}', line)
                if match:
                    self.month, self.year = match.group().split()
                    break

    def expected_file_lists(self):
        """
        Get the three lists of files associated with the Emt.

        Returns:
            tuple: A tuple containing three lists of file names.
        """
        support_doc_files = [
            f"!!readme_{self.version_number_us}_English.txt",
            f"detail_report_{self.version_number_us}_English.pdf",
            f"dist_file_format_{self.version_number_us}_English.pdf",
            f"intguide_{self.version_number_us}_English.pdf",
            f"SMQ_intguide_{self.version_number_us}_English.pdf",
            f"SMQ_spreadsheet_{self.version_number_us}_English.xlsx",
            f"version_report_{self.version_number_us}_English.xlsx",
            f"whatsnew_{self.version_number_us}_English.pdf",
        ]
        med_ascii_files = [
            "hlgt.asc", "hlgt_hlt.asc", "hlt.asc", "hlt_pt.asc", "intl_ord.asc",
            "llt.asc", "mdhier.asc", "meddra_history_english.asc", "meddra_release.asc", 
            "pt.asc", "smq_content.asc", "smq_list.asc", "soc.asc", "soc_hlgt.asc"
        ]
        med_ascii_files = ["/MedAscii/" + file for file in med_ascii_files] 
        seq_ascii_files = [
            "hlgt.seq", "hlgt_hlt.seq", "hlt.seq", "hlt_pt.seq", "intl_ord.seq",
            "llt.seq", "mdhier.seq", "pt.seq", "soc.seq", "soc_hlgt.seq"
        ]
        seq_ascii_files = ["/SeqAscii/" + file for file in seq_ascii_files] 
        return support_doc_files, med_ascii_files, seq_ascii_files

    def find_files(self):
        """
        Find all expected files associated with the Emt.

        Returns:
            list: A list of missing file names.
        """
        lsr = LsrTree(self.folder_name, outfmt="list")
        lsr_files = lsr.list_files()
        support_doc_files, med_ascii_files, seq_ascii_files = self.expected_file_lists()

        missing_files = []
        for file in support_doc_files + med_ascii_files + seq_ascii_files:
            if file not in lsr_files:
                missing_files.append(file)

        if not missing_files:
            mdhierasc = os.path.join(self.folder_name, 'MedAscii', 'mdhier.asc')
            #self.mdhier = pd.read_csv(mdhierasc, delimiter='$', header=None, dtype=str)
            self.mdhier = pd.read_csv(mdhierasc, delimiter='$', header=None)
            nsoc = len(self.mdhier[7].unique())
            return [], f"All files found. Version: {self.version_number}; Year: {self.year}; Month: {self.month}; Language: {self.language}. N_SOC: {nsoc}."
        else:
            return missing_files, f"{len(missing_files)} files not found."

    def load_llt(self, unique=True):
        ids=[0,1,2]
        if not self.llt:
            #tmp = pd.read_csv(os.path.join(self.folder_name, 'MedAscii', 'llt.asc'), delimiter='$', header=None, dtype=str)
            tmp = pd.read_csv(os.path.join(self.folder_name, 'MedAscii', 'llt.asc'), delimiter='$', header=None)
            self.llt = tmp[ids]
        if unique:
            self.llt = self.llt.drop_duplicates().reset_index(drop=True)


    def list_files(self):
        """
        List all files associated with the Emt.

        Returns:
            list: A list of file names.
        """
        lsr = LsrTree(self.folder_name, outfmt="tree", with_counts=True)
        lsr_files = lsr.list_files()
        return lsr_files

    def find_soc(self, terms=[], ignore_case=False):
            """
            Find all unique SOC (System Organ Class) terms.

            Args:
                terms (list, optional): The specific SOC name(s) to filter the results. Defaults to an empty list.
                ignore_case (bool, optional): Flag to indicate whether to ignore case sensitivity when filtering terms. Defaults to False.

            Returns:
                list: A list of unique SOC terms. If terms is provided, it returns the corresponding ids.

            Raises:
                AssertionError: If terms is not a list.
            """
            return self.find_term_wi_level(terms, ignore_case, level=1)

    def find_hlgt(self, terms=[], ignore_case=False):
            """
            Find all unique HLGT terms.

            Args:
                terms (list, optional): The specific HLGT name(s) to filter the results. Defaults to an empty list.
                ignore_case (bool, optional): Flag to indicate whether to ignore case sensitivity when filtering terms. Defaults to False.

            Returns:
                list: A list of unique HLGT terms. If terms is provided, it returns the corresponding ids.

            Raises:
                AssertionError: If terms is not a list.
            """
            return self.find_term_wi_level(terms, ignore_case, level=2)

    def find_hlt(self, terms=[], ignore_case=False):
            """
            Find all unique HLT terms.

            Args:
                terms (list, optional): The specific HLT name(s) to filter the results. Defaults to an empty list.
                ignore_case (bool, optional): Flag to indicate whether to ignore case sensitivity when filtering terms. Defaults to False.

            Returns:
                list: A list of unique HLT terms. If terms is provided, it returns the corresponding ids.

            Raises:
                AssertionError: If terms is not a list.
            """
            return self.find_term_wi_level(terms, ignore_case, level=3)

    def find_pt(self, terms=[], ignore_case=False):
            """
            Find all unique PT terms.

            Args:
                terms (list, optional): The specific PT name(s) to filter the results. Defaults to an empty list.
                ignore_case (bool, optional): Flag to indicate whether to ignore case sensitivity when filtering terms. Defaults to False.

            Returns:
                list: A list of unique PT terms. If terms is provided, it returns the corresponding ids.

            Raises:
                AssertionError: If terms is not a list.
            """
            return self.find_term_wi_level(terms, ignore_case, level=4)

    def find_llt(self, terms=[], ignore_case=False):
            """
            Find all unique LLT terms.

            Args:
                terms (list, optional): The specific LLT name(s) to filter the results. Defaults to an empty list.
                ignore_case (bool, optional): Flag to indicate whether to ignore case sensitivity when filtering terms. Defaults to False.

            Returns:
                list: A list of unique LLT terms. If terms is provided, it returns the corresponding ids.

            Raises:
                AssertionError: If terms is not a list.
            """
            return self.find_term_wi_level(terms, ignore_case, level=5)

    def all_str_digit(self, lst=[]):
        """
        Check if all elements in a given list are strings containing only digits.

        Args:
            fin (list): The list to check.

        Returns:
            bool: True if all elements in the list are strings containing only digits, False otherwise.
        """
        if not isinstance(lst, list):
            return False
        return all(isinstance(element, int) or element is None for element in lst)

    def assert_terms(self, input, remove_none=False):
        """
        Assert that the input is either a string or a list.
        If the input is a string, it is converted to a length one list.
        All elements in the list are converted to strings and empty elements are removed.

        Args:
            input (str or list): The input to be validated.

        Returns:
            list: The validated list.

        Raises:
            AssertionError: If the input is neither a string nor a list.
        """
        range_8_int = [10000000, 99999999]
        less_term_warning = "Warning: Some input terms might be removed due to format"
        if isinstance(input, int):
            if range_8_int[0] <= input <= range_8_int:
                return [input]
            else:
                if remove_none:
                    print(less_term_warning)
                    return []
                else:
                    return [None]

        if isinstance(input, str):
            if len(input) == 8 and input.isdigit() and input[0] != '0':
                return [int(input)]
            else:
                return [input]

        if not isinstance(input, (list, pd.core.series.Series, np.ndarray)):
            raise ValueError("Input must be a list, pandas Series, or numpy array.")
        if len(input) == 0:
            return []

        len0 = len(input)

        if all(isinstance(element, int) or (element is None) or (element is np.nan) for element in input):
            out = [element if (range_8_int[0] <= element <= range_8_int[1]) else None for element in input]
        else:
            if all((isinstance(element, str) and ((len(element) == 8 and element.isdigit()) or len(element) == 0)) or (element is None) or (element is np.nan) for element in input):
                out = [int(element) if (len(element) == 8 and element.isdigit() and element[0] != '0') else None for element in input]
            else:
                out = [element if (element is not np.nan) else None for element in input]
        if remove_none:
            out = [element for element in out if element is not None]
        if len(out) != len0:
            print(less_term_warning)
        return out

    def find_term_wi_level(self, terms=[], ignore_case=False, level=1):
        """
        Find all unique terms.

        Args:
            terms (list, optional): The specific SOC name(s) to filter the results. Defaults to an empty list.
            ignore_case (bool, optional): Flag to indicate whether to ignore case sensitivity when filtering terms. Defaults to False.
            level (int, optional): The level of the SOC hierarchy to consider. Defaults to 1.

        Returns:
            list: A list of unique terms. If terms is provided, it returns the corresponding ids.

        Raises:
            AssertionError: If terms is not a list.

        """
        assert level in range(1, 6), "level should be between 1 and 5"
        ignore_case = ignore_case if isinstance(ignore_case, bool) and ignore_case else False
        if level < 5:
            id0 = 4-level 
            id1 = 8-level
            subset = self.mdhier[[id0, id1]].drop_duplicates().reset_index(drop=True)
        else:
            id0 = 0 
            id1 = 1
            self.load_llt()
            subset = self.llt[[id0,id1]]

        terms = self.assert_terms(terms)

        if terms:
            if self.all_str_digit(lst=terms):
                out = pd.merge(pd.DataFrame(terms), subset, left_on=0, right_on=id0)[id1].tolist()
            else:
                terms_df = pd.DataFrame(terms)
                if ignore_case:
                    out = pd.merge(terms_df, subset, left_on=terms_df[0].str.lower(), right_on=subset[id1].str.lower(), how='left', sort=False)[id0].tolist()
                else:
                    out = pd.merge(terms_df, subset, left_on=0, right_on=id1, how='left', sort=False)[id0].tolist()
        else:
            out = subset[id1].tolist()
        return out

    def find_pt_given_soc(self, soc=[], primary_soc_only=False, ignore_case=False):
        """
        Find all PTs (Preferred Terms) given a SOC (System Organ Class) name.

        Args:
            soc (str or list): The name of the SOC or a list of SOC names.
            primary_soc_only (bool, optional): If True, only return PTs associated with the primary SOC. 
                                                Defaults to False.

        Returns:
            pandas.DataFrame: A DataFrame containing the PTs associated with the given SOC. 
                                Each row represents a PT and contains the PT code and PT name.
        """

        df = self.mdhier
        if df.empty:
            return pd.DataFrame(columns=['pt_id', 'pt', 'primary'])
        soc = self.assert_terms(soc, remove_none=True)
        if self.all_str_digit(lst=soc):
            soc_id = soc
        else:
            soc_id = self.find_soc(soc, ignore_case=ignore_case)

        if primary_soc_only:
            subset_df = df[(df[3].isin(soc_id)) & (df[11] == 'Y')][[0, 4, 3, 7]].reset_index(drop=True)
            subset_df.columns = ['pt_id', 'pt', 'soc_id', 'soc']
        else:
            subset_df = df[df[3].isin(soc_id)][[0, 4, 3, 7, 11]].reset_index(drop=True)
            subset_df.columns = ['pt_id', 'pt', 'soc_id', 'soc', 'primary']
            
        return subset_df


    def find_llt_given_pt(self, pt=[], ignore_case=False):
        """
        Find all LLTs (Lowest Level Terms) given a PT (Preferred Term) name or a list of PT names.

        Args:
            pt (str or list): The name of the PT or a list of PT names.

        Returns:
            pandas.DataFrame: A DataFrame containing the LLTs associated with the given PT(s). 
                                Each row represents an LLT and contains the LLT code and LLT name.
        """
        self.load_llt()
        df = self.llt
        pt = self.assert_terms(pt, remove_none=True)

        if self.all_str_digit(lst=pt):
            pt_id = pt
        else:
            pt_id = self.find_pt(pt, ignore_case=ignore_case)

        subset_df = df[df[2].isin(pt_id)]
        subset_df.columns = ['llt_id', 'llt', 'pt_id']
        subset_df['pt'] = self.find_pt(subset_df['pt_id'])
        
        return subset_df

    def find_llt_given_soc(self, soc=[], primary_soc_only=False, ignore_case=False):
        """
        Find all LLTs (Lowest Level Terms) given a SOC (System Organ Class) name.

        Args:
            soc_name (str): The name of the SOC.
            primary_soc_only (bool, optional): If True, only return LLTs associated with the primary SOC. 
                                                Defaults to False.

        Returns:
            pandas.DataFrame: A DataFrame containing the LLTs associated with the given SOC. 
                                Each row represents an LLT and contains the LLT code and LLT name.
        """
        pt_df = self.find_pt_given_soc(soc=soc, primary_soc_only=primary_soc_only, ignore_case=ignore_case)
        llt_df = self.find_lt_given_pt(pt=pt_df['pt_id'], ignore_case=ignore_case)
        return llt_df.merge(pt_df, on='pt_id')

    def find_soc_given_pt(self, pt=[], primary_only=True, ignore_case=False):
        """
        Find the SOC (System Organ Class) given a list of PT (Preferred Term) names.

        Args:
            pt (list): A list of PT names.

        Returns:
            str: The name of the primary SOC.

        Raises:
            AssertionError: If pt is not a list.
        """
        df = self.mdhier
        pt = self.assert_terms(pt, remove_none=True)

        if self.all_str_digit(lst=pt):
            pt_id = pt
        else:
            pt_id = self.find_pt(pt, ignore_case=ignore_case)

        pt_soc = df[[0,4, 3,7, 11]]
        pt_soc.columns=['pt_id', 'pt', 'soc_id','soc','primary']
        if primary_only:
            pt_soc = pt_soc[pt_soc['primary'] == 'Y']

        out = pd.DataFrame(pt_id)
        out.columns = ['pt_id']
        
        out = out.merge(pt_soc, on='pt_id', how='left')

        return out

    def load_smq(self):
        if self.smq_list is None:
            #tmp = pd.read_csv(os.path.join(self.folder_name, 'MedAscii', 'smq_list.asc'), delimiter='$', header=None, dtype=str)
            tmp = pd.read_csv(os.path.join(self.folder_name, 'MedAscii', 'smq_list.asc'), delimiter='$', header=None)
            if not tmp.empty:
                tmp = tmp.iloc[:, :-1]
                tmp.columns = ['id', 'name', 'level', 'description', 'source', 'note', 'MedDRA_version', 'status', 'algorithm']
                self.smq_list = tmp
       #if self.smq_content is None:
        #    #tmp = pd.read_csv(os.path.join(self.folder_name, 'MedAscii', 'smq_content.asc'), delimiter='$', header=None, dtype=str)
        #    tmp = pd.read_csv(os.path.join(self.folder_name, 'MedAscii', 'smq_content.asc'), delimiter='$', header=None)
        #    if tmp is not None and not tmp.empty:
        #        tmp = tmp.iloc[:, :-1]
        #        self.smq_content = tmp


    def find_smq(self, terms=[], with_detail=False, ignore_case=False):
        """
        Find all unique SMQ (Standard MedDRA Queries) terms.

        Args:
            terms (list, optional): The specific SMQ name(s) to filter the results. Defaults to an empty list.
            ignore_case (bool, optional): Flag to indicate whether to ignore case sensitivity when filtering terms. Defaults to False.

        Returns:
            list: A list of unique SMQ terms. If terms is provided, it returns the corresponding ids.

        Raises:
            AssertionError: If terms is not a list.
        """
        self.load_smq()
        if self.smq_list is None:
            return 'smq file not found'

        df = self.smq_list

        terms = self.assert_terms(terms)

        if len(terms) == 0:
            return df['name'].tolist()

        if not with_detail:
            if self.all_str_digit(terms):
                return df[df['id'].isin(terms)]['name'].tolist()
            else:
                if ignore_case:
                    out = df[df['name'].str.lower().isin([term.lower() for term in terms])]['id'].tolist()
                else: 
                    out=df[df['name'].isin(terms)]['id'].tolist()
                return out
        else:
            if self.all_str_digit(terms):
                out = df[df['id'].isin(terms)]
            else:
                if ignore_case:
                    out = df[df['name'].str.lower().isin([term.lower() for term in terms])]
                else:
                    out = df[df['name'].isin(terms)]
            return out

    def find_llt_given_smq(self, smq=[], ignore_case=False):
        """
        Find all LLTs (Lowest Level Terms) given an SMQ (Standard MedDRA Query) name or a list of SMQ names.

        Args:
            smq (str or list): The name of the SMQ or a list of SMQ names.
            ignore_case (bool, optional): Flag to indicate whether to ignore case sensitivity when filtering terms. Defaults to False.

        Returns:
            pandas.DataFrame: A DataFrame containing the LLTs associated with the given SMQ(s). 
                                Each row represents an LLT and contains the LLT code and LLT name.
        """
        self.load_smq()
        df = self.smq_content

        smq = self.assert_terms(smq)

        if len(smq) == 1:
            subset_df = df[df['SMQ_NAME'].str.contains(smq[0], case=ignore_case)]
        else:
            subset_df = df[df['SMQ_NAME'].isin(smq)]
        llt_df = self.find_llt(subset_df['LLT_CODE'], ignore_case=ignore_case)
        return llt_df

if __name__ == "__main__":
    pass
