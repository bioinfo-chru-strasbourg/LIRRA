import pandas as pd
import polars as pl
#pip install "polars[all]"
#pip install "polars[numpy,pandas,pyarrow]"
import os
class map_file:
    """This class are used for transform a raw datas into fam file. It"s use like input for PLINK1.9"""

    def __init__(self, file_input,cM_map, output):
        self.file_input=file_input
        self.cM_map=cM_map
        self.output=output
        self.none_match=0
        self.generate_map()

    def search_cM_info(self, data) : 
        df_cM_map=pl.read_csv(self.cM_map, sep="\t")
        cM_target= {}
        cM_column=[]

        for row in df_cM_map.iter_rows(named=True) :
            keys_cM= row["Chromosome"] + " s " +str(row["Position(bp)"])
            cM_target[keys_cM] = row["Map(cM)"]

        for row in data.iter_rows(named=True) :
            target_key= "chr"+row["Chr"]+ " s " + str(row["Position"])
            
            cM_column.append(cM_target.get(target_key, 0.0))

        kk=[i for i in cM_column if i == 0.0]
        print(len(kk))
        return cM_column
    
    def generate_map(self):
        data = pl.read_csv(
            self.file_input,
            sep="\t",
            dtypes={
                "Name" : str,
                "Chr" : str,
                "Position" : int
            }
        )  
        cM_column=self.search_cM_info(data)

        output_dir = os.path.dirname(self.output) #recupere le chemin
        if not os.path.exists(output_dir) :
            os.makedirs(output_dir)


        map_final=pl.DataFrame(
                {
                    "Chr" : "chr"+data["Chr"],
                    "ID" : data["Name"],
                    "Position_morgan" : cM_column ,
                    "Position_pb" : data["Position"]
                }
            )

        
        map_final.write_csv(        
                file = self.output,
                has_header = False,
                sep="\t"
            )

        # df_lgen.to_csv(self.output, sep="\t",index=None, header=None)

        # TODO: il faut que je recupere le truc directe filepath+outputdir


if __name__ == "__main__":
    map = map_file("/home1/BAS/hameaue/TEST01/data_input.map","/home1/BAS/hameaue/db_snp/big_map/global_map.map","/home1/BAS/hameaue/TEST01/plink_with_zero.map")
