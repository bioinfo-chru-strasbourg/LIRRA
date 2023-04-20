import sys
import logging as log
from common import OutputChecker
import os
import subprocess as sp


def test_dialog_user():
    choix = input(
        "If you execut this pytest all results directory are overwrite, do you want continue ? [y/n] \n"
    )

    if choix.lower() == "y":
        pass
    elif choix.lower() == "n":
        exit()
    else:
        print(
            "Thanks write Y for agree and continue this pytest or N for quit and save your previous results"
        )
        test_dialog_user()


def test_run_snakefile():
    com = OutputChecker(os.path.dirname(__file__))
    if os.path.exists(com.snp_file):
        # save previous snp_data
        sp.run(
            ["mv", com.snp_file, com.config_directories_path + "/snp_data_previous.tsv"]
        )

        sp.run(
            ["cp", com.test_path + "/unit/snp_data.tsv", com.config_directories_path]
        )
    else:
        # export snp_data test
        sp.run(
            ["cp", com.test_path + "/unit/snp_data.tsv", com.config_directories_path]
        )

    if os.path.exists(com.lisfam_file):
        # save previous list fam
        sp.run(
            [
                "mv",
                com.lisfam_file,
                com.config_directories_path + "/list_puce_fam_previous.fam",
            ]
        )

        sp.run(
            [
                "cp",
                com.test_path + "/unit/list_puce_fam.fam",
                com.config_directories_path,
            ]
        )
    else:
        # export list fam test
        sp.run(
            [
                "cp",
                com.test_path + "/unit/list_puce_fam.fam",
                com.config_directories_path,
            ]
        )

    if os.path.exists(com.config_directories_path + "/config.yaml"):
        sp.run(
            [
                "mv",
                com.config_directories_path + "/config.yaml",
                com.config_directories_path + "/config_previous.yaml",
            ]
        )

        sp.run(["cp", com.test_path + "/unit/config.yaml", com.config_directories_path])
    else:
        sp.run(["cp", com.test_path + "/unit/config.yaml", com.config_directories_path])

    if os.path.exists(com.config_directories_path + "/target_data.tsv"):
        sp.run(
            [
                "mv",
                com.config_directories_path + "/target_data.tsv",
                com.config_directories_path + "/target_data_previous.tsv",
            ]
        )
        sp.run(
            ["cp", com.test_path + "/unit/target_data.tsv", com.config_directories_path]
        )

    else:
        sp.run(
            ["cp", com.test_path + "/unit/target_data.tsv", com.config_directories_path]
        )

    # run snakemake
    os.system("rm ../results/*")

    path_config = os.path.join(os.path.dirname(__file__), "..", "config")
    os.system(
        f"snakemake -c10 --use-conda --conda-frontend conda --directory {path_config}/../workflow/ -s {path_config}/../workflow/Snakefile"
    )


def test_rule_clean_data():
    com = OutputChecker(os.path.dirname(__file__))
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/clean_data/expected/Full_data_clean.tsv",
            com.results_path + "/Full_data_clean.tsv",
        ]
    )


def test_rule_pre_create_file():
    com = OutputChecker(os.path.dirname(__file__))
    ##input##
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/pre_create_file/data/Full_data_clean.tsv",
            com.results_path + "/Full_data_clean.tsv",
        ]
    )

    ##output##
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/pre_create_file/expected/data_input.map",
            com.results_path + "/data_input.map",
        ]
    )
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/pre_create_file/expected/input_puce.fam",
            com.results_path + "/input_puce.fam",
        ]
    )


def test_rule_create_file_map_first():
    com = OutputChecker(os.path.dirname(__file__))
    ##input##
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/create_file_map_first/data/data_input.map",
            com.results_path + "/data_input.map",
        ]
    )

    ##output##
    sp.check_output(
        [
            "cmp",
            com.integration_path
            + "/create_file_map_first/expected/plink_with_zero.map",
            com.results_path + "/plink_with_zero.map",
        ]
    )


def test_rule_create_file_map_second():
    com = OutputChecker(os.path.dirname(__file__))
    ##input##
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/create_file_map_second/data/plink_with_zero.map",
            com.results_path + "/plink_with_zero.map",
        ]
    )

    ##output##
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/create_file_map_second/expected/plink.map",
            com.results_path + "/plink.map",
        ]
    )


def test_rule_create_file_lgen():
    com = OutputChecker(os.path.dirname(__file__))
    ##input##
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/create_file_lgen/data/Full_data_clean.tsv",
            com.results_path + "/Full_data_clean.tsv",
        ]
    )

    ##output##
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/create_file_lgen/expected/plink.lgen",
            com.results_path + "/plink.lgen",
        ]
    )


def test_rule_create_file_fam():
    com = OutputChecker(os.path.dirname(__file__))
    ##input##
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/create_file_fam/data/input_puce.fam",
            com.results_path + "/input_puce.fam",
        ]
    )

    ##output##
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/create_file_fam/expected/plink.fam ",
            com.results_path + "/plink.fam",
        ]
    )


def test_rule_create_file_fam():
    com = OutputChecker(os.path.dirname(__file__))
    ##input##
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/find_ROH/data/plink.fam",
            com.results_path + "/plink.fam",
        ]
    )
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/find_ROH/data/plink.lgen",
            com.results_path + "/plink.lgen",
        ]
    )
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/find_ROH/data/plink.map",
            com.results_path + "/plink.map",
        ]
    )

    ##output##
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/find_ROH/expected/plink.hom",
            com.results_path + "/plink.hom",
        ]
    )


def test_rule_roh_select():
    com = OutputChecker(os.path.dirname(__file__))
    ##input##
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/roh_select/data/plink.hom",
            com.results_path + "/plink.hom",
        ]
    )

    ##output##
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/roh_select/expected/ROH_select.tsv",
            com.results_path + "/ROH_select.tsv",
        ]
    )


def test_rule_summary_first():
    com = OutputChecker(os.path.dirname(__file__))
    ##input##
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/summary_first/data/ROH_select.tsv",
            com.results_path + "/ROH_select.tsv",
        ]
    )

    ##output##
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/summary_first/expected/dating.txt",
            com.results_path + "/dating.txt",
        ]
    )


def test_create_output():
    com = OutputChecker(os.path.dirname(__file__))
    ##input##
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/create_output/data/ROH_select.tsv",
            com.results_path + "/ROH_select.tsv",
        ]
    )
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/create_output/data/dating.txt",
            com.results_path + "/dating.txt",
        ]
    )
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/create_output/data/plink.hom",
            com.results_path + "/plink.hom",
        ]
    )
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/create_output/data/target_data.tsv",
            com.config_directories_path + "/target_data.tsv",
        ]
    )

    ##output##
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/create_output/expected/custom_track.tsv",
            com.results_path + "/custom_track.tsv",
        ]
    )
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/create_output/expected/full_results.tsv",
            com.results_path + "/full_results.tsv",
        ]
    )
    sp.check_output(
        [
            "cmp",
            com.integration_path + "/create_output/expected/global_summary.tsv",
            com.results_path + "/global_summary.tsv",
        ]
    )
