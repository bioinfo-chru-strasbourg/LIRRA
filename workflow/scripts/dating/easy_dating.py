import polars as pl
import sys
import os
import yaml

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from homozigosity_individual import HomozigosityIndividual


class EasyDating:
    def __init__(self) -> None:
        cohorte_homozygous = HomozigosityIndividual()
        self.dating = ""
        self.confidence = ""
        self.load_path()
        self.load_map()
        self.search_cM_length()

    def load_path(self):
        with open(
            os.path.join(
                os.path.dirname(__file__), "..", "..", "..", "config", "config.yaml"
            ),
            "r",
        ) as file:
            prime_service = yaml.safe_load(file)
            self.path_plink_map = prime_service["path"]["plink_map"]
            self.software_search_roh = prime_service["params"]["ROH_detect_software"]
            self.path_roh_detect = prime_service["path"]["ROH_select"]

    def load_map(self):
        if self.software_search_roh == "plink":
            self.dict_map = {}
            map = pl.read_csv(self.path_plink_map, has_header=False)
            # print(map)
            for row in map["column_1"]:
                row_ash = str(row).split()
                if row_ash[0] != "chrX":
                    self.dict_map[f"chr{row_ash[0]}:{row_ash[3]}"] = row_ash[2]

        else:
            pass

        # print(self.dict_map)

    def search_cM_length(self):
        if self.software_search_roh == "plink":
            df = pl.read_csv(self.path_roh_detect, has_header=False, separator="\t")
            start_roh_com = max(df["column_7"].to_list())
            end_roh_com = min(df["column_8"].to_list())
            chr_interest = f"chr{str(list(set(df['column_4'].to_list()))).replace('[','').replace(']','')}"
            cM_start = self.dict_map[f"{chr_interest}:{start_roh_com}"]
            cM_end = self.dict_map[f"{chr_interest}:{end_roh_com}"]
            print(df)
            nb_id = 2 * (int(len(set(df["column_2"].to_list()))))

            print(f"{(200 / ((float(cM_end) - float(cM_start)) * nb_id)) * 25} years")
            self.dating = (
                f"{(200 / ((float(cM_end) - float(cM_start)) * (nb_id))) * 25} years"
            )
            self.confidence = ""


if __name__ == "__main__":
    EasyDating()
