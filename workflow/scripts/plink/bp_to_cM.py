import yaml
import os
import polars as pl


class convert_bp_to_cM:
    def __init__(self):
        self.left_arms_cM = []
        self.right_arms_cM = []
        self.mutation_positions = int(self.init_mutation_position().split(":")[1])
        self.find_bp_arms()
        self.find_cM_plink()

    def init_mutation_position(self):
        with open(
            os.path.join(
                os.path.dirname(__file__), "..", "..", "..", "config", "config.yaml"
            ),
            "r",
        ) as file:
            prime_service = yaml.safe_load(file)
            self.chr_interest = str(
                prime_service["variant_informations"]["location_variant"]
            ).split(":")[0]
            return str(prime_service["variant_informations"]["location_variant"])

    def find_bp_arms(self):
        roh_select = pl.read_csv(
            os.path.join(
                os.path.dirname(__file__), "..", "..", "..", "results", "ROH_select.txt"
            ),
            sep="\t",
            has_header=False,
        )
        self.dico_sample_pos = {}
        self.left_arms_bp = roh_select["column_7"].to_list()
        self.right_arms_bp = roh_select["column_8"].to_list()
        self.id_roh = roh_select["column_2"].to_list()
        i = 0
        for row in roh_select.iter_rows(named=True):
            if self.dico_sample_pos.get(row["column_2"], "NA") == "NA":
                self.dico_sample_pos[row["column_2"]] = (
                    str(self.left_arms_bp[i]) + ":" + str(self.right_arms_bp[i])
                )

            else:
                pos1 = self.dico_sample_pos[row["column_2"]].split(":")[0]
                pos2 = self.dico_sample_pos[row["column_2"]].split(":")[1]
                if int(pos1) > int(self.left_arms_bp[i]):
                    self.dico_sample_pos[row["column_2"]] = (
                        str(self.left_arms_bp[i]) + ":" + pos2
                    )
                elif int(pos2) < int(self.right_arms_bp[i]):
                    self.dico_sample_pos[row["column_2"]] = (
                        pos1 + ":" + str(self.right_arms_bp[i])
                    )
            i = i + 1

    def closest(self, lst: list, target_value: int):
        return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - target_value))]

    def find_cM_plink(self):
        plink_data = pl.read_csv(
            os.path.join(
                os.path.dirname(__file__), "..", "..", "..", "results", "plink.map"
            ),
            has_header=False,
            sep="\t",
        )
        dico_closest_sample_cM = {}
        self.list_bp_chrinterest = []
        list_cM_chrinterest = []

        for row in plink_data.iter_rows(named=True):
            if "chr" + str(row["column_1"]) == self.chr_interest:
                self.list_bp_chrinterest.append(int(row["column_4"]))
                list_cM_chrinterest.append(row["column_3"])

        for sample in self.dico_sample_pos:
            pos1 = self.dico_sample_pos[sample].split(":")[0]
            pos2 = self.dico_sample_pos[sample].split(":")[1]
            dico_closest_sample_cM[sample] = (
                str(self.closest(self.list_bp_chrinterest, int(pos1)))
                + ":"
                + str(self.closest(self.list_bp_chrinterest, int(pos2)))
            )
            index_pos1 = self.list_bp_chrinterest.index(
                self.closest(self.list_bp_chrinterest, int(pos1))
            )
            index_pos2 = self.list_bp_chrinterest.index(
                self.closest(self.list_bp_chrinterest, int(pos2))
            )
            self.left_arms_cM.append(list_cM_chrinterest[index_pos1])
            self.right_arms_cM.append(list_cM_chrinterest[index_pos2])

        self.mutation_cM = list_cM_chrinterest[
            self.list_bp_chrinterest.index(
                self.closest(self.list_bp_chrinterest, self.mutation_positions)
            )
        ]
        self.create_input_datation()

    def create_input_datation(self):
        self.left_arms_final = []
        self.right_arms_final = []
        for i in self.left_arms_cM:
            if self.mutation_cM - i < 0:
                self.left_arms_final.append(abs(self.mutation_cM - i))

            else:
                self.left_arms_final.append((self.mutation_cM - i))

        for i in self.right_arms_cM:
            if self.mutation_cM - i < 0:
                self.right_arms_final.append(abs(self.mutation_cM - i))
            else:
                self.right_arms_final.append((self.mutation_cM - i))

    def get_markers_on_chromosome(self):
        """The size is proportional to the number of markers on chr since each time we had a chr of interest we create an element on this list"""
        return len(self.list_bp_chrinterest)

    def get_left_arms(self):
        return str(self.left_arms_final).strip("]").strip("[").strip("'")

    def get_right_arms(self):
        return str(self.right_arms_final).strip("]").strip("[").strip("'")

    __doc__ = """
    This class are use for find wich cM are associated to specific chr:bp
    Then it's use for calculate founder effect dating in our cohorte
    
    """


if __name__ == "__main__":
    convert_bp_to_cM()
