if config["params"]["ROH_detect_software"] == "plink" :
    rule roh_select:
        input:
            config["path"]["plink_hom"]
        output:
            config["path"]["ROH_select"]
        shell:
            "python scripts/plink/select_patients.py"

elif config["params"]["ROH_detect_software"] == "hap-ibd" :
        rule roh_select:
        input:
            config["path"]["plink_hom"]
        output:
            config["path"]["ROH_select"]
        shell:
            "python scripts/plink/select_patients.py"


rule summary_first:
    input:
        config["path"]["ROH_select"]
    output:
        config["path"]["final_dating"]
    threads: 1
    conda:
        config["path"]["envs_R"]
    shell:
        """
        python scripts/plink/define_mutation_age.py
        Rscript scripts/plink/Mutation_Age_estimation.R 1>>{output}

        """