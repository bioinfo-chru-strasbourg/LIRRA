import yaml
import os
import polars as pl
import pandas as pd
import logging as log


class HomozigosityIndividual:
    def __init__(self):
        self.load_config()
        self.length_pb_tot = self.coverage()  # 2881033286
        self.prepare_file()
        # self.build_df()

    def load_config(self):
        with open(
            os.path.join(
                os.path.dirname(__file__), "..", "..", "config", "config.yaml"
            ),
            "r",
        ) as file:
            prime_service = yaml.safe_load(file)
            self.software = prime_service["params"]["ROH_detect_software"]
            if self.software == "plink":
                self.path_homo_file = prime_service["path"]["plink_hom"]
            elif self.software == "hap-ibd":
                self.path_homo_file = prime_service["path"]["hap-ibd_hbd"]
            self.plink_map = prime_service["path"]["plink_map"]
        print(self.path_homo_file)

    def coverage(self):
        chr_coverage = {}
        lenght_tot = 0
        map = pl.read_csv(self.plink_map, has_header=False)
        for row in map["column_1"]:
            row_ash = str(row).split()
            if row_ash[0] != "chrX":
                # print(row_ash)
                if chr_coverage.get(row_ash[0], False) == False:
                    chr_coverage[row_ash[0]] = [int(row_ash[3])]
                    # print(chr_coverage)
                elif chr_coverage.get(row_ash[0], False) != False:
                    # print("lolo")
                    # print(type((row_ash[3])))
                    chr_coverage[row_ash[0]].append(int(row_ash[3]))
        for item in chr_coverage:
            bp = list(chr_coverage[str(item)])
            lenght_tot = lenght_tot + (max(bp) - min(bp))

        return lenght_tot
        # print(list(chr_coverage.values())

    def prepare_file(self):
        self.hbd_work = []
        if self.software == "plink":
            data = pl.read_csv(self.path_homo_file, skip_rows=1, has_header=False)
            for row in data["column_1"]:
                self.hbd_work.append(str(row).split())
                start = 6
                end = 7
                sample_id = 1

            self.check_length(13)

        elif self.software == "hap-ibd":
            data = pl.read_csv(self.path_homo_file, skip_rows=1, has_header=False)
            for row in data["column_1"]:
                self.hbd_work.append(str(row).split())
                start = 5
                end = 6
                sample_id = 0
            self.check_length(8)

        self.run_homozigosity(start, end, sample_id)

        # print(len(i) for i in self.hbd_work)

    def check_length(self, int_software):
        for i in self.hbd_work:
            if int(len(i)) != int_software:
                print(i)
                log.critical(
                    f"They are a problem with lenght of {i} he could be {int_software}"
                )

    def run_homozigosity(self, start: int, end: int, sample_id: int):
        sample_length = {}
        for row in self.hbd_work:
            length = int(row[end]) - int(row[start]) + 1
            if length > 1000000:
                if sample_length.get(row[sample_id], False) == False:
                    sample_length[row[sample_id]] = length

                elif sample_length.get(row[sample_id], False) != False:
                    sample_length[row[sample_id]] = (
                        sample_length[row[sample_id]] + length
                    )
            else:
                pass

        # print(list(sample_length.keys()))
        # print(sample_length)

        print(list(sample_length.values()))
        self.df_homo = pd.DataFrame(
            {
                "Sample ID": list(sample_length.keys()),
                "% Homozigosity": [
                    i / self.length_pb_tot for i in list(sample_length.values())
                ],
            }
        )


if __name__ == "__main__":
    HomozigosityIndividual()
