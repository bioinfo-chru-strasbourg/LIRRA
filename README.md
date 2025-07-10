LIRRA is a pipeline designed to detect and date regions of homozygosity containing a desired variant within a sub-population.

This pipeline is adapted for rare autosomal and recessive genetic mutations. Two tools are available for ROH detection: PLINK v.1.9 and hap-ibd v.1.0. If a founder effect is detected in the mutation for 2 or more patients, the common haplotype is estimated using the Mutation_age_estimation.R script (<https://github.com/bahlolab/DatingRareMutations>) or a module whose formula was created by Birgit S Budde and Yasmin Namavar (<https://doi.org/10.1038/ng.204>).

Data can be loaded from SNP array data or VCF files.

LIRRA was developed by [EliseVerin](https://github.com/EliseVerin/).

# Installation

1) Setup an environment with Python >= 3.10. You can use the provided Conda .yml or the Python in the Dockerfile
2) Do the following commands:

```
git clone https://github.com/EliseVerin/LIRRA.git
cd LIRRA
pip install -e .
```

You can test the installation with this command

```
cd .tests/
python -s 
```

# Usage

```
lirra --help 
```

# Documentation

To start the pipeline, first fill in the target_data.tsv file found in the config folder and place the SNP Array chip data in it. The names of the patients in the group must be identical between the target_data.tsv and snp_data.tsv files. You can also place your raw snp chip output files in the config/Raw_data/Full_data.txt folder. LIRRA will automatically create the snp_data.tsv file if it doesn't exist.

Then you can run lirra for example :

```
lirra -ROHs plink -Ds R_mutation -Ic True -Di SNP -vf 2.22e-6 -l chr2:170338824 -r 35
```

Here I choose to use the plink application and date the founder effect with R_mutation, ignore the centromere, my input data is snp, the frequency of my variant is 2.22e-6, located on chromosome 2 at position 170338824 and allocate 35 GB RAM to LIRRA.

# Output

At the end you get an index of the inbreeding rate of each person in the group ("homozigosity.tsv"), a description of the group submitted ("global_summary.tsv"), the ROHs taken into account during dating (full_results.tsv") and a custom track genome browser type UCSC ("custom_track.tsv).
