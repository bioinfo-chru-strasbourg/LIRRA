rule clean_data:
    output:
        config["path"]["data_clean"] 
    threads:8
    shell:
        "bash scripts/clean_data.sh"

rule pre_create_file:
    input:
        config["path"]["list_puce_fam"],
        config["path"]["data_clean"]
    output:
        config["path"]["input_map"],
        config["path"]["input_fam"]
    shell:
        "bash scripts/plink/file_plink.sh"

rule create_file_map_first:
    input: 
        config["path"]["input_map"]
    output: 
        config["path"]["plink_zero"]
    shell: 
        "python scripts/plink/map_generate.py --input {input} --output {output} "

rule create_file_map_second:
    input:
        config["path"]["plink_zero"]
    output:
        config["path"]["plink_map"]
    shell:
        "grep -v -w 0.0 {input} > {output}"

rule create_file_lgen:
    input:
        config["path"]["data_clean"]
    output:
        config["path"]["plink_lgen"]
    shell:
        "python scripts/plink/lgen_generate.py --input {input} --output {output} "

rule create_file_fam:
    input:
        config["path"]["input_fam"]
    output:
        config["path"]["plink_fam"]
    shell:
        "python scripts/plink/fam_generate.py --input {input} --output {output}"

rule find_ROH:
    input:
        config["path"]["plink_map"],
        config["path"]["plink_fam"],
        config["path"]["plink_lgen"]
    output:
        config["path"]["plink_hom"]
    shell:
        "python scripts/plink/run_docker.py"
