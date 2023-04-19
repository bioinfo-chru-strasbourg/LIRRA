import os
import logging as log
import sys
from lirra.commons import set_log_level
import yaml
from lirra.extract_samples import ExtractSamples


class InitConfig:
    def __init__(self, args):
        self.args = args
        print(self.args)
        self.write_config()

    def path_user(self):
        list_path = str(os.path.join(os.path.dirname(__file__))).split("/")
        list_path = list_path[: len(list_path) - 1]
        return "/".join(list_path)

    def write_config(self):
        dict_config = {
            "samples": "config/snp_data.tsv",
            "ref": {
                "species": "homo_sapiens",
                "data_type": "snp",
                "build": "hg19",
                "contig_length": {
                    "chr1": "249250621",
                    "chr2": "243199373",
                    "chr3": "198022430",
                    "chr4": "191154276",
                    "chr5": "180915260",
                    "chr6": "171115067",
                    "chr7": "159138663",
                    "chr8": "146364022",
                    "chr9": "141213431",
                    "chr10": "135534747",
                    "chr11": "135006516",
                    "chr12": "133851895",
                    "chr13": "115169878",
                    "chr14": "107349540",
                    "chr15": "102531392",
                    "chr16": "90354753",
                    "chr17": "81195210",
                    "chr18": "78077248",
                    "chr19": "59128983",
                    "chr20": "63025520",
                    "chr21": "48129895",
                    "chr22": "51304566",
                },
            },
            "params": {
                "ignore_centromere": self.args.Ignore_centromere,
                "confidence_coefficient": self.args.confidence_coefficient,
                "variant_frequency": self.args.variant_frequency,
                "correction_dating": self.args.correction_dating,
                "ROH_detect_software": self.args.ROH_software,
                "dating_software": self.args.Dating_software,
                "n_cores": self.args.ncores,
                "Data_input": self.args.Data_input,
                "Analysis_mode": self.args.Analysis_mode,
            },
            "variant_informations": {"location_variant": self.args.location},
            "puce_informations": {
                "location_centromeres": {
                    "chr1": "121000000-144000000",
                    "chr2": "90000000-96000000",
                    "chr3": "90439303-93641533",
                    "chr4": "49000000-52000000",
                    "chr5": "46000000 -49500000",
                    "chr6": "58500000-62500000",
                    "chr7": "57500000-62500000",
                    "chr8": "42500000-48000000",
                    "chr9": "47000000-65000000",
                    "chr10": "39000000-42500000",
                    "chr11": "51000000-56000000",
                    "chr12": "34000000-38000000",
                    "chr13": "16419000-19500000",
                    "chr14": "15500000-19500000",
                    "chr15": "15000000-20500000",
                    "chr16": "34500000-39000000",
                    "chr17": "22000000-26000000",
                    "chr18": "15000000-19500000",
                    "chr19": "24000000-28800000",
                    "chr20": "25000000-29500000",
                    "chr21": "10500000-14500000",
                    "chr22": "11500000-16000000",
                },
            },
            "path": {
                "envs_R": self.path_user() + "/workflow/envs/R_env.yml",
                "final_summary": self.path_user() + "/results/summary.txt",
                "ROH_select": self.path_user() + "/results/ROH_select.txt",
                "plink_hom": self.path_user() + "/results/plink.hom",
                "plink_map": self.path_user() + "/results/plink.map",
                "plink_fam": self.path_user() + "/results/plink.fam",
                "plink_lgen": self.path_user() + "/results/plink.lgen",
                "input_fam": self.path_user() + "/results/input_puce.fam",
                "data_clean": self.path_user() + "/results/Full_data_clean.tsv",
                "plink_zero": self.path_user() + "/results/plink_with_zero.map",
                "input_map": self.path_user() + "/results/data_input.map",
                "list_puce_fam": self.path_user() + "/config/list_puce_fam.fam",
                "report": self.path_user() + "/workflow/report/workflow.rst",
                "schema_config": self.path_user()
                + "/workflow/schemas/config.schema.yaml",
                "config": self.path_user() + "/config/config.yaml",
                "schema_samples": self.path_user()
                + "/workflow/schemas/samples.schema.yaml",
                "raw_data": self.path_user() + "/config/snp_data.tsv",
                "raw_list": self.path_user()
                + "/workflow/schemas/list_puce_fam.schema.yaml",
            },
        }
        with open(self.path_user() + "/config/config.yaml", "w") as configfile:
            yaml.dump(dict_config, configfile, sort_keys=True)

        ExtractSamples(int(self.args.ncores))
