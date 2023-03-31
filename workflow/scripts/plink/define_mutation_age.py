import yaml
import os
import bp_to_cM

class CreateMutationScript:
    def __init__(self):
        self.input_dating = bp_to_cM.ConvertBpToCM()
        self.load_config_args()
        self.create_variable()

    def load_config_args(self):
        with open(
            os.path.join(
                os.path.dirname(__file__), "..", "..", "..", "config", "config.yaml"
            ),
            "r",
        ) as file:
            prime_service = yaml.safe_load(file)
            self.confidence_coefficient = prime_service["params"][
                "confidence_coefficient"
            ]
            self.chance_sharing_correction = str(
                prime_service["params"]["correction_dating"]
            ).upper()
            self.median_allele_frequency = prime_service["params"]["variant_frequency"]
            self.chr_var = str(
                prime_service["variant_informations"]["location_variant"]
            ).split(":")[0]
            self.length_of_chromosome = prime_service["ref"]["contig_lenght"][
                self.chr_var
            ]

    def create_variable(self):
        with open(
            os.path.join(os.path.dirname(__file__), "Mutation_Age_estimation.R"), "w"
        ) as script_r:
            script_r.write("l.lengths=c(" + self.input_dating.get_left_arms() + ")\n")
            script_r.write("r.lengths=c(" + self.input_dating.get_right_arms() + ")\n")
            script_r.write(
                "confidence.coefficient = " + str(self.confidence_coefficient) + "\n"
            )
            script_r.write(
                "chance.sharing.correction = "
                + str(self.chance_sharing_correction)
                + "\n"
            )
            script_r.write(
                "median.allele.frequency = " + str(self.median_allele_frequency) + "\n"
            )
            script_r.write(
                "markers.on.chromosome = "
                + str(self.input_dating.get_markers_on_chromosome())
                + "\n"
            )
            script_r.write(
                "length.of.chromosome = " + str(self.length_of_chromosome) + "\n"
            )
            for line in self.append_algo():
                script_r.write(line)

            script_r.close()

        with open(
            os.path.join(
                os.path.dirname(__file__), "..", "..", "..", "results", "summary.txt"
            ),
            "w",
        ) as summary_file:
            summary_file.write("Dating results : \n")
            summary_file.close()

    def append_algo(self):
        lines = []
        with open(
            os.path.join(os.path.dirname(__file__), "mutation_script_cut.R"), "r"
        ) as script_r_read:
            for row_append in script_r_read:
                if row_append == "":
                    continue
                else:
                    lines.append(row_append)
            script_r_read.close()
        return lines

    __doc__ = """
    The original script of Mutation Age estimation are freely in https://github.com/bahlolab/DatingRareMutations
    But in our case we should re write this script because we can't write in raw left and right arms use for estimate age of this mutation 
    """


if __name__ == "__main__":
    CreateMutationScript()
