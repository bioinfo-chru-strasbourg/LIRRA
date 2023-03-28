import yaml
import os 

class create_Mutation_script:
    def __init__(self, l_lenghts : str ,r_lenghts : str):
        self.l_lenghts=l_lenghts
        self.r_lenghts=r_lenghts
        self.load_config_args()
        self.create_file()

    def load_config_args(self):
        # patg=os.path.join(
        #     os.path.dirname(__file__), "..", "..", "..", "resources", "global_map.map"
        # )
        with open(os.path.join(os.path.dirname(__file__),"..","..","..","config","config.yaml"), "r") as file:
            prime_service = yaml.safe_load(file)
            # l.lengths=c(14.350858000000002, 2.3970820000000117, 6.903659000000005, 0.6434520000000106, 14.99928100000001, 7.289416000000003)
            # r.lengths=c(0.8310290000000009, 17.439640999999995, 6.81130499999999, 1.3227319999999878, 38.45637599999999, 6.81130499999999)
            self.confidence_coefficient = prime_service["params"]["confidence_coefficient"]
            self.chance_sharing_correction= prime_service["params"]["confidence_coefficient"]
            self.median_allele_frequency = prime_service["params"]["variant_frequency"]
            self.markers_on_chromosome = 219015  #commande bash pour connaitre le nombre de snp sur le chromosome
            self.chr_var = str(prime_service["variant_informations"]["location_variant"]).split(":")[0]
            self.length_of_chromosome = prime_service["ref"]["contig_lenght"][self.chr_var]
            # print(self.median_allele_frequency)
            
    def create_file(self):
        with open ("Mutation_age.R", "w") as script_r:
            script_r.write(
                "l.lengths=c("+self.l_lenghts+")\n"
            )
            script_r.write(
                "r.lengths=c("+self.r_lenghts+")\n"
            )
            script_r.write(
                "confidence.coefficient = "+str(self.confidence_coefficient)+"\n"
            )
            script_r.write(
                "chance.sharing.correction = "+str(self.chance_sharing_correction)+"\n"
            )
            script_r.write(
                "median.allele.frequency = "+str(self.median_allele_frequency)+"\n"
            )
            script_r.write(
                "markers.on.chromosome = "+str(self.markers_on_chromosome)+"\n"
            )
            script_r.write(
                "length.of.chromosome = "+str(self.length_of_chromosome)+"\n"
            )

            script_r.close()
        self.append_algo()

    def append_algo(self):
        with open("Mutation_age.R", "a") as script_r_append:
            with open("mutation_script_cut.R", "r") as script_r_read :
                for row_append in script_r_read:
                    if row_append == "":
                        continue
                        # script_r_append.write("\n")
                    else :
                        script_r_append.write(row_append)


if __name__ == "__main__":
    # with open("../../../config/config.yaml", "r") as file:
    #     prime_service = yaml.safe_load(file)


    # with open ("Mutation_Age_estimation.R","w") as file_r:
    #     file_r.write("l.lengths=c("+l.lenghts)")
    create_Mutation_script("14.350858000000002, 2.3970820000000117, 6.903659000000005, 0.6434520000000106, 14.99928100000001, 7.289416000000003", "0.8310290000000009, 17.439640999999995, 6.81130499999999, 1.3227319999999878, 38.45637599999999, 6.81130499999999")
                