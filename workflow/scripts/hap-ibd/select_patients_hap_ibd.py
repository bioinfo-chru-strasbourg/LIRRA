import yaml
import polars as pl
import os
import logging as log


class SelectPatients:
    def __init__(self):
        self.iteration = 0
        self.init_variant()
        self.prepare_file()
        self.find_patients()

    def init_variant(self):
        with open("../config/config.yaml", "r") as file:
            prime_service = yaml.safe_load(file)
            self.chr_var = str(
                prime_service["variant_informations"]["location_variant"]
            ).split(":")[0]
            self.bp_var = int(
                str(prime_service["variant_informations"]["location_variant"]).split(
                    ":"
                )[1]
            )
            self.ignore_centromere = prime_service["params"]["ignore_centromere"]
            if self.ignore_centromere.startswith(
                "T"
            ) or self.ignore_centromere.startswith("t"):
                self.ignore_centromere = True
            elif self.ignore_centromere.startswith(
                "F"
            ) or self.ignore_centromere.startswith("f"):
                self.ignore_centromere = False
            self.hap_ibd_hbd_gz = prime_service["path"]["hap-ibd_hbd_gz"]
            self.hap_ibd_hbd = prime_service["path"]["hap-ibd_hbd"]
            self.side_centromere = self.side_centromere(
                prime_service["puce_informations"]["location_centromeres"]
            )

    def prepare_file(self):
        if not os.path.exists(self.hap_ibd_hbd):
            os.system(f"gunzip {self.hap_ibd_hbd_gz}")
        data = pl.read_csv(self.hap_ibd_hbd, skip_rows=1, has_header=False).sort(
            "column_1"
        )
        self.data_work = []
        for row in data["column_1"]:
            self.data_work.append(str(row).split())

    def find_patients(self):
        nb_line = 0
        with open("../results/ROH_select.tsv", "w") as roh_select:
            for row in self.data_work:
                line = []
                # print(row)
                # print(row)
                if row[4] == self.chr_var:
                    pos1 = int(row[5])
                    pos2 = int(row[6])
                    # print(f"{pos1} <= {self.bp_var} and {pos2} >= {self.bp_var}")
                    # print(row[2])
                    if pos1 <= self.bp_var and pos2 >= self.bp_var:
                        line.extend(row)
                        # print(line)
                        roh_select.write("\t".join(row) + "\n")
                        nb_line = nb_line + 1

                    else:
                        if self.ignore_centromere == False:
                            if self.roh_centromerique(row):
                                line.extend(row)
                                roh_select.write("\t".join(row) + "\n")
                                nb_line = nb_line + 1

        self.iteration = self.iteration + 1

    def side_centromere(self, dict_centromere: dict):
        bounds_right = int(str(dict_centromere[self.chr_var]).split("-")[1])
        bounds_left = int(str(dict_centromere[self.chr_var]).split("-")[0])
        self.ref_centromere = []
        if self.bp_var < bounds_right:
            self.ref_centromere.append("right")
            self.ref_centromere.append(bounds_right)

        if self.bp_var > bounds_left:
            self.ref_centromere.append("left")
            self.ref_centromere.append(bounds_left)

        if bounds_left <= self.bp_var and self.bp_var <= bounds_right:
            raise KeyError(
                "The variant are locate in centromere and we can't define ROH"
            )

    def roh_centromerique(self, row):
        if self.ref_centromere[0] == "left":
            if int(row[6]) == self.ref_centromere[1]:
                return True
        if self.ref_centromere[0] == "right":
            if int(row[5]) == self.ref_centromere[1]:
                return True
        else:
            return False

    __doc__ = """
    This class manage case where one patients have many ROH. In this script we can manage 2 ROH for one patient.
    It's dependance from ignore_centromere option in config because if it's True or False bounds are not the same.
    """


if __name__ == "__main__":
    SelectPatients()
    ##TODO : on est obligé d'avoir la position exactement égale au snp de ref il va falloir allé regardé dans le raw data les position exacte
    # TODO : on dois faire un premier tri sur les chromosomes qui nous interessent suivis des regions qui contiennent la mutation
    # TODO : on pourrait aussi ajouter les limites de snp centromeres
