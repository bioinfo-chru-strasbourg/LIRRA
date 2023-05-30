if config["params"]["ROH_detect_software"] == "plink" :
    rule roh_select_plink:
        input:
            config["path"]["plink_hom"]
        output:
            config["path"]["ROH_select"]
        shell:
            "python scripts/plink/select_patients_plink.py"

elif config["params"]["ROH_detect_software"] == "hap-ibd" :
    rule roh_select_hap_ibd:
        input:
            config["path"]["hap-ibd_hbd_gz"]
        output:
            config["path"]["ROH_select"]
        shell:
            "python scripts/hap-ibd/select_patients_hap_ibd.py"


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