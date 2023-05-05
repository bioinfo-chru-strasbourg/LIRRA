import argparse
import os
import logging as log
import yaml


class RunDocker:
    def __init__(self, file_output):
        self.file_output = file_output
        self.open_config()
        self.montage = ["results", "resources"]

        if file_output == "vcf_unphased":
            self.run_variantconvert()

        elif file_output == "vcf_phased":
            self.run_beagle()

        elif file_output == "hap-ibd":
            self.run_hap_ibd()

    def open_config(self):
        with open(
            os.path.join(
                os.path.dirname(__file__), "..", "..", "..", "config", "config.yaml"
            ),
            "r",
        ) as file:
            prime_service = yaml.safe_load(file)
            self.ram = prime_service["params"]["ram"]
            self.vcf_unphased = prime_service["path"]["vcf_unphased"]
            self.fasta = prime_service["path"]["fasta_genome"]

    def run_beagle(self):
        os.system(
            f"docker run --rm -v {self.change_path(self.montage[0])}:/data:rw beagle:5.4 java -Xmx{self.ram}g -jar beagle.22Jul22.46e.jar gt=/data/vcf_unphased.vcf out=/data/vcf_phased map=/data/plink.map "
        )

    def run_variantconvert(self):
        self.check_genome_fasta()

        os.system(
            f"docker run --rm -v {self.change_path(self.montage[0])}:/data:rw -v {self.change_path(self.montage[1])}:/home1/BAS/DOCKER_STARK_MAIN_FOLDER/databases/genomes/current:ro variantconvert:1.2.2 convert -i /data/Full_data_clean.tsv -o /data/vcf_unphased.vcf -fi snp -fo vcf -c configs/hg19/snp.json"
        )

        vcf_unphased_autosomal = (
            self.change_path(self.montage[0]) + "/vcf_unphased_autosomal.vcf"
        )
        vcf_unphased_sort = self.change_path(self.montage[0]) + "/vcf_unphased_sort.vcf"
        os.system(
            f'grep -v -E "chrX|chrY" {self.vcf_unphased} > {vcf_unphased_autosomal} && grep "^#" {vcf_unphased_autosomal} > {vcf_unphased_sort} && grep -v "^#" {vcf_unphased_autosomal} | sort -k1,1V -k2,2n >> {vcf_unphased_sort}'
        )
        os.system(
            f"mv {self.vcf_unphased} {self.change_path(self.montage[0])}/vcf_unphased_raw.vcf"
        )
        os.system(f"mv {vcf_unphased_sort} {self.vcf_unphased}")
        """
        The file output contain chry and chrx, we remove them then we sort this vcf. 
        """

    def run_hap_ibd(self):
        os.system(
            f"docker run --rm -v {self.change_path(self.montage[0])}:/data:rw eliseverin/hap-ibd:1.0 java -jar hap-ibd.jar gt=/data/vcf_phased.vcf.gz map=/data/plink.map out=/data/hap-ibd min-seed=2.0 max-gap=1000 min-extend=1.0 min-output=2.0 min-markers=100 min-mac=1"
        )

    def change_path(self, directory: str):
        # if directory != "resources":
        #     log.debug("it's not the good directory name")
        #     raise ValueError(
        #         "Thanks to check directories name are the same like in github (results and resources)"
        #     )
        # elif directory != "results":
        #     log.debug("it's not the good directory name")
        #     raise ValueError(
        #         "Thanks to check directories name are the same like in github (results and resources)"
        #     )
        path_full = os.path.join(os.path.dirname(__file__))
        list_path = str(path_full).split("/")
        list_path = list_path[: len(list_path) - 3]
        list_path.append(str(directory))
        return "/".join(list_path)

    def check_genome_fasta(self):
        path_gz = os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "resources", "hg19.fa.gz"
        )
        path_resource = os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "resources", "hg19.fa"
        )
        if not os.path.exists(self.fasta):
            if os.path.exists(path_gz):
                os.system(f"gunzip {path_gz}")
            else:
                if os.path.exists(self.fasta):
                    try:
                        os.system(
                            f"wget https://hgdownload.soe.ucsc.edu/goldenPath/hg19/bigZips/hg19.fa.gz -P {path_resource}"
                        )
                        os.system(f"gunzip {path_gz}")

                    except:
                        log.critical(
                            "They are a problem with dl hg19.fa.gz check url exist (https://hgdownload.soe.ucsc.edu/goldenPath/hg19/bigZips/) or download with another link then put in resource directory"
                        )
                        exit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-fo", "--file_output", type=str)

    args = parser.parse_args()
    RunDocker(args.file_output)


if __name__ == "__main__":
    main()
