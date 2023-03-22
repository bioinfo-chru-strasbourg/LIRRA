import pandas as pd

class fam_file :
    """This class are used for transform a raw datas into fam file. It's use like input for PLINK1.9"""
    def __init__(self, file_name, output):
        self.file_name=file_name
        self.output=output
        self.data_transform()
    
    def data_transform(self):
        """We transform nan values into 0 like format for PLINK"""
        data = pd.read_csv(self.file_name, sep= '\t')
        id_mother =[]
        id_father =[]
        for i in range(data.shape[0]):
            if (str(data.iloc[i,2]) == 'nan'):
                id_father.append(0)
            else:
                id_father.append(data.iloc[i,2])

            if (str(data.iloc[i,3]) == 'nan'):
                id_mother.append(0)
            else:
                id_mother.append(data.iloc[i,3])
            
            

        final_fam = pd.DataFrame({'Family_id': data.iloc[:,0], 'Sample':data.iloc[:,1], 'Father_id' : id_father, 'Mother_id':id_mother, 'Sex':data.iloc[:,4], 'Phenotype':data.iloc[:,5]})
        final_fam.to_csv(self.output, sep='\t', header=None, index=None)
        final_fam.to_csv('puce_for_lgen.fam', sep='\t', index=None)

if __name__ == '__main__':
    fam=fam_file('input_puce.fam','puce_final.fam')