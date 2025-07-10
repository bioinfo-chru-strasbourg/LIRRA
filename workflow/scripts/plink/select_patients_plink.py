import yaml
import polars as pl
import wide_search_roh
import os
import logging as log


class SelectPatients:
    def __init__(self):
        self.lines = []
        self.init_variant()
        self.prepare_file()
        self.find_patients()
        self.write_roh_select()

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
            self.plink_hom = prime_service["path"]["plink_hom"]

            self.ignore_centromere = prime_service["params"]["ignore_centromere"]
            if self.ignore_centromere.startswith(
                "T"
            ) or self.ignore_centromere.startswith("t"):
                self.ignore_centromere = True
            elif self.ignore_centromere.startswith(
                "F"
            ) or self.ignore_centromere.startswith("f"):
                self.ignore_centromere = False
            self.side_centromere = self.side_centromere(
                prime_service["puce_informations"]["location_centromeres"]
            )

    def prepare_file(self):
        data = pl.read_csv(self.plink_hom, skip_rows=1, has_header=False)
        self.data_work = []
        for row in data["column_1"]:
            self.data_work.append(str(row).split())
        log.debug("prepare_file data_work", self.data_work)

    def find_patients(self):
        for row in self.data_work:
            if "chr" + row[3] == self.chr_var:
                # print(row)
                pos1 = int(row[6])
                pos2 = int(row[7])
                print(row)
                # if self.ignore_centromere == True:
                if pos1 <= self.bp_var and pos2 >= self.bp_var:
                    self.lines.append(row)

                else:
                    if self.ignore_centromere == False:
                        if self.roh_centromerique(row):
                            # print("hey")
                            self.lines.append(row)
        log.debug("find_patients lines", self.lines)
        self.check_ROH_find()

    def check_ROH_find(self):
        if len(self.lines) <= 1:
            log.info(
                "The default settings do not allow to retrieve all ROHs, use wider search parameters"
            )

            os.system("python scripts/plink/wide_search_roh.py ")
            self.lines.clear()
            self.prepare_file()
            for row in self.data_work:
                if "chr" + row[3] == self.chr_var:
                    pos1 = int(row[6])
                    pos2 = int(row[7])
                    if pos1 <= self.bp_var and pos2 >= self.bp_var:
                        self.lines.append(row)

                    else:
                        if self.ignore_centromere == False:
                            if self.roh_centromerique(row):
                                self.lines.append(row)

    def write_roh_select(self):
        with open("../results/ROH_select.tsv", "w") as roh_select:
            print(self.lines)
            for line in self.lines:
                roh_select.write("\t".join(line) + "\n")

    def side_centromere(self, dict_centromere: dict):
        # For locate where is the variant compare too centromere
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
            if int(row[7]) == self.ref_centromere[1]:
                return True
        if self.ref_centromere[0] == "right":
            if int(row[6]) == self.ref_centromere[1]:
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
