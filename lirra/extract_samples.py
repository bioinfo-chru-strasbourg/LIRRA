import sys
import os
import pandas as pd
import polars as pl
import logging as log


class ExtractSamples:
    def __init__(self, ncores: int):
        self.ncores = ncores
        self.exist_full_raw = False
        self.lines = []
        self.path_config = os.path.join(os.path.dirname(__file__), "..", "config")

        self.excel_user_path = os.path.join(
            os.path.dirname(__file__), "..", "config", "target_data.tsv"
        )
        self.path_full_data = os.path.join(
            os.path.dirname(__file__), "..", "config", "Raw_data", "Full_data.txt"
        )

        if os.path.exists(self.path_full_data):
            self.exist_full_raw = True
        else:
            self.exist_full_raw = False

        if os.path.exists(
            os.path.join(os.path.dirname(__file__), "..", "config", "snp_data.tsv")
        ):
            self.exist_snp_data = True
            self.path_snp_data = os.path.join(
                os.path.dirname(__file__), "..", "config", "snp_data.tsv"
            )

        else:
            self.exist_snp_data = False

        if not os.path.exists(self.excel_user_path):
            raise FileNotFoundError(
                f"target_data.tsv doesn't exist. Please check your data contains required informations(Group,Samples,Family(pedigree)) and they are in ({os.path.dirname(os.path.normpath(self.excel_user_path))}) directory."
            )
        else:
            self.check_entry_excel_user()

        self.load_data_user(self.excel_user_path)

    def load_data_user(self, excel_path):
        self.file_user = pd.read_csv(excel_path, sep="\t")
        group = self.file_user["Group"].to_dict()
        sample = self.file_user["Sample"].to_dict()
        dict_extract = {}
        for row in range(len(group)):
            if dict_extract.get(group[row], False) == False:
                dict_extract[group[row]] = [sample[row]]
            else:
                samples = dict_extract[group[row]]
                samples.append(sample[row])
                dict_extract[group[row]] = samples

        if self.exist_snp_data:
            # print("1 hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
            if not self.check_snp_data_exist(dict_extract):
                # print("2 hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")

                if self.exist_full_raw:
                    # print("3 hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")

                    if not self.check_full_data_exist(dict_extract):
                        # print("4 hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")

                        raise ValueError(
                            "Impossible de construire les donées car pas de snp_data.tsv ni de Full data qui contiennent les bonnes donées (checker le nom des samples soit les mêmes que dans le target)"
                        )
                    else:
                        self.create_snp(dict_extract)

                else:
                    raise ValueError(
                        "Impossible de construire les donées car il n'y a pas de Full data raw ni de snp_data contenant les informations nécéssaires"
                    )
            else:
                self.run_pipeline()

        else:
            if self.exist_full_raw:
                if not self.check_full_data_exist(dict_extract):
                    raise ValueError(
                        "Impossible de construire les donées car pas de snp_data.tsv ni de Full data qui contiennent les bonnes donées (checker le nom des samples soit les mêmes que dans le target)"
                    )
                else:
                    self.create_snp(dict_extract)

            else:
                log.critical(
                    f"Il n'existe pas {os.path.dirname(os.path.normpath(self.excel_user_path))}/Raw_data/Full_data.tsv"
                )
                raise ValueError(
                    "Impossible de construire les donées car il n'y a pas de Full data raw ni de snp_data"
                )

    def create_snp(self, dict_extract):
        log.info("snp_data.tsv building")
        self.create_base_snp_data()
        self.path_raw = os.path.join(
            os.path.dirname(__file__), "..", "config", "Raw_data"
        )
        for group_list in dict_extract:
            sample_search = "|^".join(dict_extract[group_list])
            sample_search = "^" + sample_search
            self.lines.append(
                f"cut -f \"$(head -n1 {os.path.normpath(self.path_full_data)} | tr '\\t' '\\n' | grep -n -E '{sample_search}' | cut -d: -f1 | paste -sd,)\" {os.path.normpath(self.path_full_data)} > {os.path.normpath(self.path_raw)}/group.tsv \n"
            )
            self.lines.append(
                f"paste -d'\\t' {os.path.normpath(self.base_path)} {os.path.normpath(self.path_raw)}/group.tsv > {os.path.normpath(self.path_config)}/snp_data.tsv  \n"
            )
            self.lines.append(
                f"rm {os.path.normpath(self.path_raw)}/group.tsv {os.path.normpath(self.path_raw)}/base.tsv"
            )

        with open(f"{self.path_config}/create_files.sh", "w") as cmd_sh:
            for line in self.lines:
                cmd_sh.write(line)

        os.system(f"bash {self.path_config}/create_files.sh")
        os.system(f"rm {self.path_config}/create_files.sh")
        self.run_pipeline()

    def create_base_snp_data(self):
        self.base_path = os.path.join(
            os.path.dirname(__file__), "..", "config", "Raw_data", "base.tsv"
        )
        full_data_exist = pl.read_csv(
            self.path_full_data,
            separator="\t",
            dtypes={"Chr": str},
            columns=["Index", "Name", "Address", "Chr", "Position"],
        )
        pl.DataFrame(
            {
                "Index": full_data_exist["Index"].to_list(),
                "Name": full_data_exist["Name"].to_list(),
                "Address": full_data_exist["Address"].to_list(),
                "Chr": full_data_exist["Chr"].to_list(),
                "Position": full_data_exist["Position"].to_list(),
            }
        ).write_csv(
            self.base_path,
            separator="\t",
        )

    def check_entry_excel_user(self):
        excel_user = pl.read_csv(self.excel_user_path, separator="\t")
        # print(len(excel_user["Family(pedigree)"]))
        if excel_user.shape[0] == 0:
            log.critical(
                f"You should please fill in the target_data.tsv file in the directory {self.excel_user_path}"
            )
            exit()

        elif excel_user.shape[0] >= 1:
            if excel_user.shape[0] >= 1:
                log.info(
                    f"You can't obtain any dating for your cohorte it's necessary to have more 1 patient for one group"
                )
            """
            Check if they are all columns required
            Then check if they are all informations for each sample
            """
            target_columns = [
                "Group",
                "Sample",
                "Sex (1=M, 2=F)",
                "Phenotype (1=unaffected, 2=affected)",
                "Family(pedigree)",
            ]
            for item in target_columns:
                try:
                    excel_user.columns.index(item)

                except ValueError:
                    log.critical(
                        f"He miss {item} column in target_sample.tsv, thanks to add this column and fill in"
                    )
                    exit()
            dic_sample = {}
            index = 1
            for sample in excel_user["Sample"].to_list():
                dic_sample[index] = sample
                index = index + 1
            empty_info_patient = []
            for item in target_columns:
                if excel_user.shape[0] != len(excel_user[str(item)]):
                    log.warning(
                        f"Check length for your column {item} ans he is not empty for any patients"
                    )
                index = 1
                # print(index)
                for information in excel_user[str(item)].to_list():
                    if information == None:
                        empty_info_patient.append(dic_sample[index])
                    index = index + 1
                if len(empty_info_patient) != 0:
                    log.critical(
                        f"Tanks to check information for your patients {empty_info_patient} in column {str(item)}. This columns can't be empty for any patients"
                    )
                    exit()

    def check_snp_data_exist(self, dict_extract):
        result = True
        snp_data_exist = pl.read_csv(
            self.path_snp_data, separator="\t", dtypes={"Chr": str}, ignore_errors=True
        )
        excel_user = pl.read_csv(self.excel_user_path, separator="\t")
        for group in set(excel_user["Group"].to_list()):
            # print(group)
            target_sample = [str(i) + ".Top Alleles" for i in dict_extract[group]]

        target_sample.extend(["Index", "Name", "Address", "Chr", "Position"])
        for item in target_sample:
            try:
                snp_data_exist.columns.index(item)

            except ValueError:
                result = False

        return result

    def check_full_data_exist(self, dict_extract):
        result = True
        full_data_exist = pl.read_csv(
            self.path_full_data, separator="\t", dtypes={"Chr": str}, ignore_errors=True
        )
        excel_user = pl.read_csv(self.excel_user_path, separator="\t")
        for group in set(excel_user["Group"].to_list()):
            target_sample = [str(i) + ".Top Alleles" for i in dict_extract[group]]

        target_sample.extend(["Index", "Name", "Address", "Chr", "Position"])
        for item in target_sample:
            try:
                full_data_exist.columns.index(item)

            except ValueError:
                result = False
        return result

    def init_fam_file(self):
        pd.DataFrame(
            {
                "Family ID": self.file_user["Family(pedigree)"].to_list(),
                "Sample ID": self.file_user["Sample"].to_list(),
                "Project": self.file_user["Project"].to_list(),
                "Paternal IDd": self.file_user["Paternal_id"].to_list(),
                "Maternal ID": self.file_user["Maternal_id"].to_list(),
                "Sex (1=M, 2=F)": self.file_user["Sex (1=M, 2=F)"].to_list(),
                "Phenotype (1=unaffected, 2=affected)": self.file_user[
                    "Phenotype (1=unaffected, 2=affected)"
                ].to_list(),
            },
        ).to_csv(
            os.path.join(
                os.path.dirname(__file__), "..", "config", "list_puce_fam.fam"
            ),
            sep="\t",
            index=False,
        )

    def run_pipeline(self):
        self.init_fam_file()
        os.system(
            f"snakemake -c{self.ncores} --use-conda --conda-frontend conda --directory {self.path_config}/../workflow/ -s {self.path_config}/../workflow/Snakefile"
        )
