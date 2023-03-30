import os
import yaml


def change_path(path_full):
    list_path = str(path_full).split("/")
    list_path = list_path[: len(list_path) - 3]
    list_path.append("results")
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
        if prime_service["params"]["ignore_centromere"]:
            return "--homozyg-snp 250 --homozyg-kb 2500 --homozyg-density 50 --homozyg-gap 1000 --homozyg-window-snp 50 --homozyg-window-het 1 --homozyg-window-missing 5  --homozyg-window-threshold 0.05"
        elif not prime_service["params"]["ignore_centromere"]:
            return "--homozyg-snp 300 --homozyg-kb 4000 --homozyg-density 50 --homozyg-gap 1000 --homozyg-window-snp 50 --homozyg-window-het 1 --homozyg-window-missing 5  --homozyg-window-threshold 0.05"


if __name__ == "__main__":
    path_full = os.path.join(os.path.dirname(__file__))
    os.system(
        "docker run --rm -v "
        + change_path(path_full)
        + ":/data:rw plink:1.9 plink1.9 --noweb --lfile plink --recode"
    )
    os.system(
        "docker run --rm -v "
        + change_path(path_full)
        + ":/data:rw plink:1.9 plink1.9 --noweb --file plink --genome --min 0 --max 1"
    )
    os.system(
        "docker run --rm -v "
        + change_path(path_full)
        + ":/data:rw plink:1.9 plink1.9 --noweb --file plink --geno 0.01 --make-bed"
    )
    os.system(
        "docker run --rm -v "
        + change_path(path_full)
        + ":/data:rw plink:1.9 plink1.9 --noweb --bfile plink --homozyg "
        + homozyg_run()
    )
