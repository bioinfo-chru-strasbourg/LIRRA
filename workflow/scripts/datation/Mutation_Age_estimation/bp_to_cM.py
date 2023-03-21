import math as m
class convert :
    def __init__(self, left_arms : list, right_arms : list, mutation_position, path_plink_map):
        self.left_arms=left_arms
        self.right_arms=right_arms
        self.mutation_positions=mutation_position
        self.path_plink_map=path_plink_map

    def convert_bp_to_cM(self):
        nw_left_arms=[]
        nw_right_arms=[]
        for i in self.left_arms :
            print(self.mutation_positions-i)
            if self.mutation_positions-i <0 :
                nw_left_arms.append(((self.mutation_positions-i)*-1)*m.pow(10,-6))
                
            else :
                nw_left_arms.append((self.mutation_positions-i)*m.pow(10,-6))

        for i in self.right_arms :
            if self.mutation_positions-i <0 :
                nw_right_arms.append(((self.mutation_positions-i)*-1)*m.pow(10,-6))
            else :
                nw_right_arms.append((self.mutation_positions-i)*m.pow(10,-6))
        # print(self.left_arms[0]-self.mutation_positions)
        print(nw_left_arms)
        print(nw_right_arms)
    
    def find_cM_plink (self) :
        nw_left_arms=[]
        nw_right_arms=[]
        for i in self.left_arms :
            print(self.mutation_positions-i)
            if self.mutation_positions-i <0 :
                nw_left_arms.append(((self.mutation_positions-i)*-1))
                
            else :
                nw_left_arms.append((self.mutation_positions-i))

        for i in self.right_arms :
            if self.mutation_positions-i <0 :
                nw_right_arms.append(((self.mutation_positions-i)*-1))
            else :
                nw_right_arms.append((self.mutation_positions-i))
        # print(self.left_arms[0]-self.mutation_positions)
        print(nw_left_arms)
        print(nw_right_arms)

if __name__ =='__main__' : 
    print("h")
    
    #for BBS5
    # convert=convert([163.081788, 161.306357, 135.549599,140.54431, 181.589631, 182.276059, 182.440829, 182.240034 ], [198.363314, 184.686627, 201.712025, 208.271113, 188.880055, 188.461092, 186.199093, 186.025423],182.974602,"")
    #for BBS3
    convert=convert([95.854083, 107.807859, 103.301282, 109.561489, 95.20566, 102.915525], [111.03597, 127.644582, 117.016246, 111.527673, 148.661317, 117.016246],110.204941,"")
    # convert=convert([71758015, 86222845, 76181089, 95107211, 71681950, 75726925], [98895637, 116842805, 106380005, 99954721, 139271591, 106380005],109.962394)
    convert.find_cM_plink()