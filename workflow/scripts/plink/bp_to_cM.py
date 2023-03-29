import math as m
import yaml
import os
import polars as pl

class convert_bp_to_cM :
    def __init__(self):
        self.left_arms_cM=[]
        self.right_arms_cM=[]
        self.mutation_positions=int(self.init_mutation_position().split(":")[1])
        # self.path_plink_map=path_plink_map
        self.find_bp_arms()
        self.find_cM_plink()

    def init_mutation_position(self):
        with open(os.path.join(os.path.dirname(__file__),"..","..","..","config","config.yaml"), "r") as file:
            prime_service = yaml.safe_load(file)
            self.chr_interest=str(prime_service["variant_informations"]["location_variant"]).split(":")[0]
            return str(prime_service["variant_informations"]["location_variant"])
            
    def find_bp_arms(self):
        roh_select=pl.read_csv(os.path.join(os.path.dirname(__file__),"..","..","..","results","ROH_select.txt"), sep="\t", has_header=False)
        # print(roh_select)
        #column 7 et 8
        self.dico_sample_pos={}
        self.left_arms_bp=roh_select["column_7"].to_list()
        self.right_arms_bp=roh_select["column_8"].to_list()
        self.id_roh=roh_select["column_2"].to_list()
        i=0
        for row in roh_select.iter_rows(named=True):
            if self.dico_sample_pos.get(row["column_2"], "NA") == "NA" :
                self.dico_sample_pos[row["column_2"]]=str(self.left_arms_bp[i])+":"+str(self.right_arms_bp[i])
            
            else :
                #cas ou on a deja 1 ROH d'associer au sample il faut faire gaffe au bp que l'on va remplacer et l'ordre
                #ici c'est facile on a tout dans l'ordre mais on aura peux etre un cas ou ça ne le sera pas justement
                pos1= self.dico_sample_pos[row["column_2"]].split(":")[0]
                pos2= self.dico_sample_pos[row["column_2"]].split(":")[1]
                if int(pos1) > int(self.left_arms_bp[i]) :
                    self.dico_sample_pos[row["column_2"]]=str(self.left_arms_bp[i])+":"+pos2
                elif int(pos2) < int(self.right_arms_bp[i]) :
                    self.dico_sample_pos[row["column_2"]]=pos1+":"+str(self.right_arms_bp[i])
            i=i+1
                

    def convert_bp_to_cM(self):
        #it's an old version when we don't look cM in plink.map 
        nw_left_arms=[]
        nw_right_arms=[]
        for i in self.left_arms_bp :
            # print(self.mutation_positions-i)
            if self.mutation_positions-i <0 :
                nw_left_arms.append(((self.mutation_positions-i)*-1)*m.pow(10,-6))
                
            else :
                nw_left_arms.append((self.mutation_positions-i)*m.pow(10,-6))

        for i in self.right_arms_bp :
            if self.mutation_positions-i <0 :
                nw_right_arms.append(((self.mutation_positions-i)*-1)*m.pow(10,-6))
            else :
                nw_right_arms.append((self.mutation_positions-i)*m.pow(10,-6))
        # print(self.left_arms[0]-self.mutation_positions)
        # print(nw_left_arms)
        # print(nw_right_arms)

    def closest(self, lst : list, target_value : int):
        return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-target_value))]
    
    def find_cM_plink (self) :
        plink_data=pl.read_csv(os.path.join(os.path.dirname(__file__),"..","..","..","results","plink.map"), has_header=False, sep="\t")
        # print(plink_data)
        dico_closest_sample_cM={}
        self.list_bp_chrinterest=[]
        list_cM_chrinterest=[]
        bp_plink_map=plink_data["column_4"].to_list()

        #search in first bp more closest than over if it's not a perfect match in plink.map build list of bp at chr interest
        for row in plink_data.iter_rows(named=True):
            if "chr"+str(row['column_1']) == self.chr_interest:
                self.list_bp_chrinterest.append(int(row["column_4"]))
                list_cM_chrinterest.append(row["column_3"])
        
        for sample in self.dico_sample_pos:
            pos1=self.dico_sample_pos[sample].split(":")[0]
            pos2=self.dico_sample_pos[sample].split(":")[1]
            dico_closest_sample_cM[sample]= str(self.closest(self.list_bp_chrinterest, int(pos1))) + ":" + str(self.closest(self.list_bp_chrinterest, int(pos2)))
            index_pos1=self.list_bp_chrinterest.index(self.closest(self.list_bp_chrinterest, int(pos1)))
            index_pos2=self.list_bp_chrinterest.index(self.closest(self.list_bp_chrinterest, int(pos2)))
            self.left_arms_cM.append(list_cM_chrinterest[index_pos1])
            self.right_arms_cM.append(list_cM_chrinterest[index_pos2])

        self.mutation_cM=list_cM_chrinterest[self.list_bp_chrinterest.index(self.closest(self.list_bp_chrinterest, self.mutation_positions))]
#trouve pas exactement même end de ASG186327

        # print(self.closest(list_bp_chrinterest, int(pos1)))
        # print(self.left_arms_cM)
        self.create_input_datation() 

    def create_input_datation(self):
        self.left_arms_final=[]
        self.right_arms_final=[]
        for i in self.left_arms_cM :
            # print(self.mutation_positions-i)
            if self.mutation_cM-i <0 :
                self.left_arms_final.append(abs(self.mutation_cM-i))
                
            else :
                self.left_arms_final.append((self.mutation_cM-i))

        for i in self.right_arms_cM :
            if self.mutation_cM-i <0 :
                self.right_arms_final.append(abs(self.mutation_cM-i))
            else :
                self.right_arms_final.append((self.mutation_cM-i))

    def get_markers_on_chromosome(self):
        #la taille est proportionelle au nombre de marqueur sur chr3 puisque a chaque fois que l'on avait un chr d'interet on créer un élement de la liste
        return len(self.list_bp_chrinterest)

    def get_left_arms(self):
        return str(self.left_arms_final).strip("]").strip("[").strip("'")
    
    def get_right_arms(self):
        return str(self.right_arms_final).strip("]").strip("[").strip("'")
        
if __name__ =='__main__' : 
    convert_bp_to_cM()
    # print(convert().markers_on_chromosome())
    
    #for BBS5
    # convert=convert([163.081788, 161.306357, 135.549599,140.54431, 181.589631, 182.276059, 182.440829, 182.240034 ], [198.363314, 184.686627, 201.712025, 208.271113, 188.880055, 188.461092, 186.199093, 186.025423],182.974602,"")
    #for BBS3


    # convert=convert([95.854083, 107.807859, 103.301282, 109.561489, 95.20566, 102.915525], [111.03597, 127.644582, 117.016246, 111.527673, 148.661317, 117.016246],110.204941,"")
    # convert=convert([71758015, 86222845, 76181089, 95107211, 71681950, 75726925], [98895637, 116842805, 106380005, 99954721, 139271591, 106380005],109.962394)
    # convert.find_cM_plink()