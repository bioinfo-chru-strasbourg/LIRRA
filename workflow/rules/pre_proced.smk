import pandas as pd
from snakemake.utils import validate
from snakemake.utils import min_version
import yaml
import os
import sys

min_version("5.4.0")



# print(os.getcwd())
report: "../report/workflow.rst"

# print("1")
#je ne sais pas si il faut 
container: "plink:1.9"

# print("2")
###Config file ###
configfile: "../config/config.yaml"


# print("3")
validate(config, schema= "../schemas/config.schema.yaml")

# print("4")

samples = pd.read_csv("../config/snp_data.csv", sep="\t")
# # print(samples)
# #pas sur que ça va marcher
validate(samples, schema="../schemas/samples.schema.yaml")

list_puce_fam=pd.read_csv("../config/list_puce_fam.fam", sep="\t")
# print(list_puce_fam)
validate(list_puce_fam, schema="../schemas/list_puce_fam.schema.yaml")


####Helper Function####


