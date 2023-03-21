import pandas as pd
from snakemake.utils import validate
from snakemake.utils import min_version

min_version("5.4.0")

report: "../report/workflow.rst"

container: "plink:1.9"

###Config file ###
configfile: "config/config.yaml"

validate(config, schema="../schemas/config.schema.yaml")


validate(samples, schema="../schemas/samples.schema.yaml")