rule roh_select:
    input:
        "../results/plink.hom"
    output:
        "../results/ROH_select.txt"
    shell:
        "python scripts/plink/select_patients.py"

rule summary_first:
    input:
        "../results/ROH_select.txt"
    output:
        "../results/summary.txt"
    threads: 1
    conda:
        "../envs/R_env.yaml"
    shell:
        """
        python scripts/plink/define_mutation_age.py
        Rscript scripts/plink/Mutation_Age_estimation.R 1>>{output}

        """