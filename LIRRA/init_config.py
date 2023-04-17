import os
import logging as log
import sys
from commons import set_log_level


class InitConfig:
    def __init__(self, args):
        self.args = args
        self.write_config()

    def path_user(self):
        list_path = str(os.path.join(os.path.dirname(__file__))).split("/")
        list_path = list_path[: len(list_path) - 1]
        return "/".join(list_path)

    def write_config(self):
        with open("../config/config.yaml", "w") as config:
            config.write(
                f"samples: config/snp_data.tsv\n\
\n\
ref :\n\
  species: homo_sapiens\n\
\n\
  data_type: snp\n\
\n\
  build: hg19\n\
\n\
  contig_lenght: {{{}}}".format("\n\
        \"chr1\" : \"249250621\",\n\
        \"chr2\" : \"243199373\",\n\
        \"chr3\" : \"198022430\",\n\
        \"chr4\" : \"191154276\",\n\
        \"chr5\" : \"180915260\",\n\
        \"chr6\" : \"171115067\",\n\
        \"chr7\" : \"159138663\",\n\
        \"chr8\" : \"146364022\",\n\
        \"chr9\" : \"141213431\",\n\
        \"chr10\" : \"135534747\",\n\
        \"chr11\" : \"135006516\",\n\
        \"chr12\" : \"133851895\",\n\
        \"chr13\" : \"115169878\",\n\
        \"chr14\" : \"107349540\",\n\
        \"chr15\" : \"102531392\",\n\
        \"chr16\" : \"90354753\",\n\
        \"chr17\" : \"81195210\",\n\
        \"chr18\" : \"78077248\",\n\
        \"chr19\" : \"59128983\",\n\
        \"chr20\" : \"63025520\",\n\
        \"chr21\" : \"48129895\",\n\
        \"chr22\" : \"51304566\"\n\
        ")"\n\)
# \n\
# params:\n\
#   ignore_centromere: True\n\
# \n\
#   confidence_coefficient: 0.95\n\
# \n\
#   variant_frequency: 2.22E-6\n\
# \n\
#   #Mode en cours de création qui va permettre de lancer un script qui cherchera a optimiser les para plink pour trouver le plus de ROH entre les patients, ce sera plus long par conséquent\n\
#   optimisation_mode: False\n\
# \n\
#   correction_dating: False\n\
# \n\
#   ROH_detect_software: \"plink\"\n\
# \n\
#   dating_software: \"Mutation_Age\"\n\
# \n\
# variant_informations:\n\
#   location_variant: \"chr2:170338824\"\n\
#   \n\
# puce_informations:\n\
#   location_centromeres: {\n\
#     \"chr1\" : \"121000000-144000000\",\n\
#     \"chr2\" : \"90000000-96000000\",\n\
#     \"chr3\" : \"90439303-93641533\",\n\
#     \"chr4\" : \"49000000-52000000\",\n\
#     \"chr5\" : \"46000000 -49500000\",\n\
#     \"chr6\" : \"58500000-62500000\",\n\
#     \"chr7\" : \"57500000-62500000\",\n\
#     \"chr8\" : \"42500000-48000000\",\n\
#     \"chr9\" : \"47000000-65000000\",\n\
#     \"chr10\" : \"39000000-42500000\",\n\
#     \"chr11\" : \"51000000-56000000\",\n\
#     \"chr12\" : \"34000000-38000000\",\n\
#     \"chr13\" : \"16419000-19500000\",\n\
#     \"chr14\" : \"15500000-19500000\",\n\
#     \"chr15\" : \"15000000-20500000\",\n\
#     \"chr16\" : \"34500000-39000000\",\n\
#     \"chr17\" : \"22000000-26000000\",\n\
#     \"chr18\" : \"15000000-19500000\",\n\
#     \"chr19\" : \"24000000-28800000\",\n\
#     \"chr20\" : \"25000000-29500000\",\n\
#     \"chr21\" : \"10500000-14500000\",\n\
#     \"chr22\" : \"11500000-16000000\"\n\
#     }\n\
# \n\
# path:\n\
#   envs_R: "+ self.path_user() + "/workflow/envs/R_env.yaml"\n\
# \n\
#   final_summary: "+ self.path_user() + "/results/summary.txt"\n\
# \n\
#   ROH_select: "+ self.path_user() + "/results/ROH_select.txt"\n\
# \n\
#   plink_hom: "+ self.path_user() + "/results/plink.hom"\n\
# \n\
#   plink_map: "+ self.path_user() + "/results/plink.map"\n\
# \n\
#   plink_fam: "+ self.path_user() + "/results/plink.fam"\n\
# \n\
#   plink_lgen: "+ self.path_user() + "/results/plink.lgen"\n\
# \n\
#   input_fam: "+ self.path_user() + "/results/input_puce.fam"\n\
# \n\
#   data_clean: "+ self.path_user() + "/results/Full_data_clean.tsv"\n\
# \n\
#   plink_zero: "+ self.path_user() + "/results/plink_with_zero.map"\n\
# \n\
#   input_map: "+ self.path_user() + "/results/data_input.map"\n\
# \n\
#   list_puce_fam: "+ self.path_user() + "/config/list_puce_fam.fam"\n\
# \n\
#   report: "+ self.path_user() + "/workflow/report/workflow.rst"\n\
# \n\
#   schema_config: "+ self.path_user() + "/workflow/schemas/config.schema.yaml"\n\
# \n\
#   config: "+ self.path_user() + "/config/config.yaml"\n\
# \n\
#   schema_samples: "+ self.path_user() + "/workflow/schemas/samples.schema.yaml"\n\
# \n\
#   raw_data: "+ self.path_user() + "/config/snp_data.tsv"\n\
# \n\
#   raw_list: + self.path_user() + "/workflow/schemas/list_puce_fam.schema.yaml" '
            )

    def init_snp_data(self):
        pass
        # TODO : faire un truc qui check si le snp_data.tsv contient tout les samples choisis
