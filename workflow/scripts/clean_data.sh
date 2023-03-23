head -n1 ../config/snp_data.csv > ../results/Full_data_clean.csv
grep rs ../config/snp_data.csv >> ../results/Full_data_clean.csv
gunzip ../resources/global_map.map.gz