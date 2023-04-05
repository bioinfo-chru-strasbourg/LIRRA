"""
Common code for unit testing of rules generated with Snakemake 7.24.2.
"""

from pathlib import Path
import subprocess as sp
import os


class OutputChecker:
    def __init__(self, path_current):
        self.snp_file=os.path.join(path_current,"..","config","snp_data.tsv")
        self.lisfam_file=os.path.join(path_current,"..","config","list_puce_fam.fam")
        self.config_directories_path=os.path.join(path_current,"..","config")
        self.test_path=os.path.join(path_current)
        self.results_path=os.path.join(path_current,"..","results")
        self.integration_path=os.path.join(path_current,"integration")

        # self.data_path = data_path
        # self.expected_path = expected_path

    # def check(self):
    #     self.input_files = set(
    #         (Path(path) / f).relative_to(self.data_path)
    #         for path, subdirs, files in os.walk(self.data_path)
    #         for f in files
    #     )
    #     self.expected_files = set(
    #         (Path(path) / f).relative_to(self.expected_path)
    #         for path, subdirs, files in os.walk(self.expected_path)
    #         for f in files
    #     )

    # def compare_files(self):
    #     if len(self.input_files) > 1 :

    #     sp.check_output(["cmp", generated_file, expected_file])
