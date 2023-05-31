import os
import yaml
import logging as log


def change_path_results(path_full):
    list_path = str(path_full).split("/")
    list_path = list_path[: len(list_path) - 3]
    list_path.append("results")
    return "/".join(list_path)


def change_path_config(path_full):
    list_path = str(path_full).split("/")
    list_path = list_path[: len(list_path) - 3]
    list_path.append("config")
    return "/".join(list_path)


def homozyg_run():
    """
    DEF para in plink1.9 --homozyg method:
    --homozyg-snp 100
    --homozyg-kb 1000
    --homozyg-density 50
    --homozyg-gap 1000
    --homozyg-het infini, tou can choose how many heterozygous calls
    --homozyg-window-snp 50
    --homozyg-window-het 1
    --homozyg-window-missing 5
    --homozyg-window-threshold 0.05
    """
    with open(
        os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "config", "config.yaml"
        ),
        "r",
    ) as file:
        prime_service = yaml.safe_load(file)
        if prime_service["params"]["analysis_output"] == "founder_effect":
            if prime_service["params"]["ignore_centromere"] == "True":
                return "--homozyg-snp 250 --homozyg-kb 2500 --homozyg-density 50 --homozyg-gap 1000 --homozyg-window-snp 50 --homozyg-window-het 1 --homozyg-window-missing 5  --homozyg-window-threshold 0.05"
            elif prime_service["params"]["ignore_centromere"] == "False":
                return "--homozyg-snp 300 --homozyg-kb 4000 --homozyg-density 50 --homozyg-gap 1000 --homozyg-window-snp 50 --homozyg-window-het 1 --homozyg-window-missing 5  --homozyg-window-threshold 0.05"

        elif prime_service["params"]["analysis_output"] == "homozigosity":
            return "--homozyg-snp 250 --homozyg-kb 2500 --homozyg-density 50 --homozyg-gap 1000 --homozyg-window-snp 50 --homozyg-window-het 1 --homozyg-window-missing 5  --homozyg-window-threshold 0.05"


def recode_run():
    with open(
        os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "config", "config.yaml"
        ),
        "r",
    ) as file:
        prime_service = yaml.safe_load(file)
        if prime_service["params"]["analysis_output"] == "founder_effect":
            print(prime_service["params"]["Data_input"])
            if prime_service["params"]["Data_input"] == "SNP":
                return f"--lfile plink"

            elif prime_service["params"]["Data_input"] == "VCF":
                print("a faire")
                exit()

        elif prime_service["params"]["analysis_output"] == "homozigosity":
            os.system(
                f"cp {change_path_config(path_full)}/vcf_data.vcf.gz {change_path_results(path_full)}"
            )
            if prime_service["params"]["Data_input"] == "VCF":
                return f"--vcf vcf_data.vcf.gz"

            if prime_service["params"]["Data_input"] == "SNP":
                return f"--lfile plink"


if __name__ == "__main__":
    path_full = os.path.join(os.path.dirname(__file__))
    os.system(
        f"docker run --rm -v {change_path_results(path_full)}:/data:rw plink:1.9 plink1.9 --noweb {recode_run()} --recode"
    )
    print(
        f"docker run --rm -v {change_path_results(path_full)}:/data:rw plink:1.9 plink1.9 --noweb {recode_run()} --recode"
    )
    print(recode_run())
    os.system(
        "docker run --rm -v "
        + change_path_results(path_full)
        + ":/data:rw plink:1.9 plink1.9 --noweb --file plink --genome --min 0 --max 1"
    )
    os.system(
        "docker run --rm -v "
        + change_path_results(path_full)
        + ":/data:rw plink:1.9 plink1.9 --noweb --file plink --geno 0.01 --make-bed"
    )
    os.system(
        f"docker run --rm -v {change_path_results(path_full)}:/data:rw plink:1.9 plink1.9 --noweb --bfile plink --homozyg {homozyg_run()}"
    )
