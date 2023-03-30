import os
def change_path(path_full):
    #on peut recuperer seulement les 3 eme slash
    list_path=path_full.split("/")
    list_path=list_path[:len(list_path)-3]
    list_path.append("results")
    return "/".join(list_path)
    # print(list_path)
if __name__ == "__main__":
    path_full = os.path.join(
            os.path.dirname(__file__)
        )
    # print(change_path(path_full))
    # os.system("docker run --rm plink:1.9 plink1.9 --help')
    # print("docker run --rm -v " + change_path(path_full) +":/data:rw plink:1.9 plink1.9 --help")
    os.system("docker run --rm -v " + change_path(path_full) +":/data:rw plink:1.9 plink1.9 --noweb --lfile plink --recode")
    os.system("docker run --rm -v " + change_path(path_full) +":/data:rw plink:1.9 plink1.9 --noweb --file plink --genome --min 0 --max 1")
    os.system("docker run --rm -v " + change_path(path_full) +":/data:rw plink:1.9 plink1.9 --noweb --file plink --geno 0.01 --make-bed")
   # pour BBS5 
    os.system("docker run --rm -v " + change_path(path_full) +":/data:rw plink:1.9 plink1.9 --noweb --bfile plink --homozyg --homozyg-snp 250 --homozyg-kb 2500 --homozyg-gap 1000 --homozyg-window-het 1 --homozyg-window-missing 5 --homozyg-window-snp 50 --homozyg-window-threshold 0.05")
    #pour BBS3
    # os.system("docker run --rm -v " + change_path(path_full) +":/data:rw plink:1.9 plink1.9 --noweb --bfile plink --homozyg --homozyg-snp 300 --homozyg-kb 4000 ")