import pandas as pd
from snakemake.utils import validate
from snakemake.utils import min_version
import yaml
import os
import sys

min_version("5.4.0")



# print(os.getcwd())
# report: config["path"]["report"]

###Config file ###
configfile: "../config/config.yaml"



# print("3")
validate(config, schema= config["path"]["schema_config"])

# print("4")
if config["params"]["Data_input"] == "SNP":
    samples = pd.read_csv(config["path"]["raw_data"], sep="\t")
    # # print(samples)
    # #pas sur que ça va marcher
    validate(samples, schema=config["path"]["schema_samples"])

    list_puce_fam=pd.read_csv(config["path"]["list_puce_fam"], sep="\t")
    # print(list_puce_fam)
    validate(list_puce_fam, schema=config["path"]["raw_list"])

elif config["params"]["Data_input"] == "VCF":
    pass

####Helper Function####


