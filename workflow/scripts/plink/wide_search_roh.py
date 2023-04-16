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
    --homozyg-het infini, you can choose how many heterozygous calls
    --homozyg-window-snp 50
    --homozyg-window-het 1
    --homozyg-window-missing 5
    --homozyg-window-threshold 0.05
    """

    return "--homozyg-snp 50 --homozyg-kb 500 --homozyg-density 30 --homozyg-gap 5000 --homozyg-window-snp 25 --homozyg-window-het 1 --homozyg-window-missing 50  --homozyg-window-threshold 0.05"


if __name__ == "__main__":
    path_full = os.path.join(os.path.dirname(__file__))
    os.system(
        "docker run --rm -v "
        + change_path(path_full)
        + ":/data:rw plink:1.9 plink1.9 --noweb --bfile plink --homozyg "
        + homozyg_run()
    )
