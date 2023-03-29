rule roh_select:
    input:
        "../results/plink.hom"
    output:
        "../results/ROH_select.txt"
    shell:
        "python scripts/plink/select_patients.py"

rule summary:
    input:
        "../results/ROH_select.txt"
    output:
        "../results/summary.txt"
    threads: 5
    shell:
        """
        conda activate R_env
        python scripts/plink/define_mutation_age.py
        Rscript scripts/plink/Mutation_Age_estimation.R 1>../results/summary.txt
        """