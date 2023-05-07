import os
import yaml
import polars as pl
import logging as log


class CleanCheckRs:
    def __init__(self):
        self.load_config()
        self.run_bash()
        self.search_dup()

    def load_config(self):
        with open(
            os.path.join(
                os.path.dirname(__file__), "..", "..", "config", "config.yaml"
            ),
            "r",
        ) as file:
            prime_service = yaml.safe_load(file)
            self.path_full_data_clean_dup = prime_service["path"]["data_clean_dup"]
            self.path_full_data_clean = prime_service["path"]["data_clean"]
            self.db_snp_info = prime_service["path"]["db_snp"]
            self.path_snp_data = prime_service["path"]["raw_data"]

    def run_bash(self):
        os.system(
            f"head -n1 {os.path.normpath(self.path_snp_data)} > {os.path.normpath(self.path_full_data_clean_dup)}"
        )
        os.system(
            f"head -n1 {os.path.normpath(self.path_snp_data)} > {os.path.normpath(self.path_full_data_clean)}"
        )
        os.system(
            f"grep rs {os.path.normpath(self.path_snp_data)} >> {os.path.normpath(self.path_full_data_clean_dup)}"
        )
        os.system(
            f"bash {os.path.join(os.path.dirname(__file__), '..', 'docker', 'create_docker.sh')}"
        )
        # os.system("bash clean_data.sh")

    def search_dup(self):
        self.dup_file_cut = pl.read_csv(
            self.path_full_data_clean_dup,
            separator="\t",
            columns=["Name", "Chr", "Position"],
            dtypes={"Chr": str},
        )
        dic_check_dup = {}
        dic_dup_find = {}
        for row in self.dup_file_cut.iter_rows(named=True):
            # print(dic_check_dup.get(f"chr{row['Chr']}:{row['Position']}", False))

            if dic_check_dup.get(f"chr{row['Chr']}:{row['Position']}", False) == False:
                id = [row["Name"]]
                dic_check_dup[f"chr{row['Chr']}:{row['Position']}"] = id
            else:
                # Dans le cas ou on a une dup du coup
                dic_check_dup[f"chr{row['Chr']}:{row['Position']}"].append(row["Name"])
                dic_dup_find[f"chr{row['Chr']}:{row['Position']}"] = dic_check_dup[
                    f"chr{row['Chr']}:{row['Position']}"
                ]

        print(dic_dup_find.keys())
        self.load_db_snp_info()
        # print(self.dict_db_snp_info)
        self.final_data_uniq = pl.read_csv(
            self.path_full_data_clean_dup,
            separator="\t",
            dtypes={"Chr": str},
            ignore_errors=True,
        )
        lines = []
        for row in self.final_data_uniq.iter_rows(named=True):
            # print(row)
            if f"chr{row['Chr']}:{row['Position']}" == "chr0:0":
                # ajoute pas
                pass

            elif row["Name"] == "rs35664482":
                log.warning("rs35664482 this SNP are ignored because it's var delins")
                pass

            elif row["Name"] == "rs35548854":
                log.warning("rs35548854 this SNP are ignored because it's var delins")
                pass

            elif dic_dup_find.get(f"chr{row['Chr']}:{row['Position']}", False) == False:
                list_values = list(row.values())
                lines.append(list_values)

            elif dic_dup_find.get(f"chr{row['Chr']}:{row['Position']}", False) != False:
                if (
                    self.dict_db_snp_info.get(
                        f"chr{row['Chr']}:{row['Position']}", False
                    )
                    != False
                ):
                    # en gros si on a bien le chr: pos dans la db_snp_info
                    if (
                        self.dict_db_snp_info[f"chr{row['Chr']}:{row['Position']}"]
                        == row["Name"]
                    ):
                        list_values = list(row.values())
                        lines.append(list_values)
                    else:
                        pass
        with open(self.path_full_data_clean, "a") as final_data:
            for line in lines:
                line_str = [str(i) for i in line]
                final_data.write("\t".join(line_str) + "\n")

    def load_db_snp_info(self):
        self.db_snp = pl.read_csv(self.db_snp_info, separator="\t")
        self.dict_db_snp_info = {}
        for row in self.db_snp.iter_rows(named=True):
            self.dict_db_snp_info[f"{row['#CHROM']}:{row['POS']}"] = row["ID"]


if __name__ == "__main__":
    CleanCheckRs()
