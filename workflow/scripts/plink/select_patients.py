import yaml 
import polars as pl

class select_patients:
    def __init__(self):
        self.init_variant()
        self.prepare_file()
        self.find_patient()

    def init_variant(self):
        with open("../config/config.yaml", "r") as file:
            prime_service = yaml.safe_load(file)
            self.chr_var=str(prime_service["variant_informations"]["location_variant"]).split(":")[0]
            self.bp_var=int(str(prime_service["variant_informations"]["location_variant"]).split(":")[1])
            self.ignore_centromere=prime_service["params"]["ignore_centromere"]
            self.side_centromere=self.side_centromere(prime_service["puce_informations"]["location_centromeres"])
    
    def prepare_file(self):
        data = pl.read_csv("../results/plink.hom", skip_rows=1, has_header=False)
        self.data_work=[]
        for row in data["column_1"]:
            self.data_work.append(str(row).split())

        # print(data)
        #TODO : faire un raise pour la vérification des tailles des colonnes


    def find_patient(self):
        with open("../results/ROH_select.txt", "w") as roh_select :
            for row in self.data_work:
                line=[]
                if "chr"+row[3] == self.chr_var :
                    pos1=int(row[6])
                    pos2=int(row[7])
                    # print(self.chr_var)
                    if pos1 <= self.bp_var and pos2 >= self.bp_var:
                        line.append(row)
                        # print(row)
                        roh_select.write("\t".join(row) + "\n")                    
                    else :
                        if not self.ignore_centromere:
                            #ROH centromerique seulement si on est a false pour ignorer le centromere
                            if self.roh_centromerique(row):
                                line.append(row)
                                print("dedans")
                                roh_select.write("\t".join(row) + "\n")                    



    def side_centromere(self,dict_centromere : dict):
        bounds_right=int(str(dict_centromere[self.chr_var]).split("-")[1])
        bounds_left=int(str(dict_centromere[self.chr_var]).split("-")[0])
        self.ref_centromere=[]
        if self.bp_var < bounds_right :
            self.ref_centromere.append("right") 
            self.ref_centromere.append(bounds_right)
        
        if self.bp_var > bounds_left :
            self.ref_centromere.append("left") 
            self.ref_centromere.append(bounds_left)

        if bounds_left <= self.bp_var and self.bp_var <= bounds_right :
            raise KeyError("The variant are locate in centromere and we can't define ROH")        

    def roh_centromerique(self,row):
        # print(self.ref_centromere[0] == "left")
        if self.ref_centromere[0] == "left" :
            if int(row[7]) == self.ref_centromere[1]:
                return True
        if self.ref_centromere[0] == "right" :
            if int(row[6]) == self.ref_centromere[1]:
                return True
        else :
            return False
        
        ##TODO : on est obligé d'avoir la position exactement égale au snp de ref il va falloir allé regardé dans le raw data les position exacte 
        
if __name__ == "__main__":
    select_patients()
        #TODO : on dois faire un premier tri sur les chromosomes qui nous interessent suivis des regions qui contiennent la mutation
        #TODO : on pourrait aussi ajouter les limites de snp centromeres