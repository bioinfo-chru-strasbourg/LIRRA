###############clean .csv full data
    ##only for BBS5
head -n1 Full_Data_Table_Avril2019_230119.csv > Full_data_clean.csv
grep rs Full_Data_Table_Avril2019_230119.csv >> Full_data_clean.csv



    ##only for BBS3 !!!!!!!!!!!!!
head -n1 snp_data.csv > Full_data_clean.csv
grep rs snp_data.csv >> Full_data_clean.csv

###############clean .fam
cut -f1,2,4,5,6,7 Liste_puce_BBS3_6F.fam > input_puce.fam

###############clean .map
cut -f4,2,5 Full_data_clean.csv > tmp_data.map
grep Name tmp_data.map  > data_input.map && grep -v Name tmp_data.map |sort -k2,2V -k3,3n >> data_input.map
lancer le python
grep -v 0.0 plink_with_zero.map > plink.map
#bien trier

##############pour le vcf test de beagle
grep "#CHROM" test1_sort.vcf | cut -f2,1,3  > vcf_input.map
grep "chr" test1_sort.vcf |cut -f2,1,3  >> vcf_input.map

###############clean .lgen

ta$ h=$( )

fam
lgen
map
