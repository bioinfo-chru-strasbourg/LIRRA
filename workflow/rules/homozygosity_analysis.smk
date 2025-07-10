if config["params"]["ROH_detect_software"] == "plink" :
    rule run_plink:
        input: 
            config["path"]["raw_data_vcf"]
        output:
            config["path"]["plink_hom"]
        shell:
            "python scripts/plink/run_docker_plink.py"
    
    rule homozigosity_WES:
        input:
            config["path"]["plink_hom"]
        output:
            config["path"]["homozigosity"]
        shell:
            "python scripts/homozigosity_individual.py"



