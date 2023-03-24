import yaml 
import polars as pl
import os

class select_patients:
    def __init__(self):
        self.init_variant()
        self.prepare_file()
        self.find_patient()

    def init_variant(self):
        with open('../../../config/config.yaml', 'r') as file:
            prime_service = yaml.safe_load(file)
            self.chr_var=str(prime_service["params"]["location_variant"]).split(":")[0]
            self.bp_var=str(prime_service["params"]["location_variant"]).split(":")[1]
    
    def prepare_file(self):
        data = pl.read_csv("../../../results/plink.hom", skip_rows=1, has_header=False)
        self.data_work=[]
        for row in data["column_1"]:
            self.data_work.append(str(row).split())

        # print(data)
        #TODO : faire un raise pour la vérification des tailles des colonnes


    def find_patient(self):
        with open("../../../results/ROH_select.txt", "w") as roh_select :
            for row in self.data_work:
                line=[]
                if "chr"+str(row[3]) == self.chr_var :
                    print(self.chr_var)
                    if row[6] <= self.bp_var and row[7] >= self.bp_var:
                        line.append(row)
                        print(row)
                        roh_select.write("\t".join(row) + "\n")
                
                else:
                    continue


        # psrint(line)


if __name__ == "__main__":
    print("hello")
    select_patients()
        #TODO : on dois faire un premier tri sur les chromosomes qui nous interessent suivis des regions qui contiennent la mutation
        #TODO : on pourrait aussi ajouter les limites de snp centromeres