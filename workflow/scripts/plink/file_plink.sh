###############prepare.fam
cut -f1,2,4,5,6,7 ../config/list_puce_fam.fam > ../results/input_puce.fam

###############prepare .map
cut -f4,2,5 ../results/Full_data_clean.tsv > ../results/tmp_data.map
grep Name ../results/tmp_data.map  > ../results/data_input.map && grep -v Name ../results/tmp_data.map |sort -k2,2V -k3,3n >> ../results/data_input.map