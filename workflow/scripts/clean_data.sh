head -n1 ../config/snp_data.tsv > ../results/Full_data_clean.tsv
grep rs ../config/snp_data.tsv >> ../results/Full_data_clean.tsv
# gunzip ../resources/global_map.map.gz
#create docker file for plink
bash docker/create_docker.sh