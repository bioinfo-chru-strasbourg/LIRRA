rule clean_data:
    output:
        "../results/Full_data_clean.csv" 
    shell:
        "bash scripts/clean_data.sh"

rule pre_create_file:
    input:
        "../config/list_puce_fam.fam",
        "../results/Full_data_clean.csv"
    output:
        "../results/data_input.map",
        "../results/input_puce.fam"
    shell:
        "bash scripts/plink/file_plink.sh"

rule create_file_map_first:
    input: 
        "../results/data_input.map"
    output: 
        "../results/plink_with_zero.map",
    shell: 
        "python scripts/plink/map_generate.py --input {input} --output {output} "

rule create_file_map_second:
    input:
        "../results/plink_with_zero.map"
    output:
        "../results/plink.map"
    shell:
        "grep -v -w 0.0 {input} > {output}"

rule create_file_lgen:
    input:
        "../results/Full_data_clean.csv"
    output:
        "../results/plink.lgen"
    shell:
        "python scripts/plink/lgen_generate.py --input {input} --output {output} "

rule create_file_fam:
    input:
        "../results/input_puce.fam"
    output:
        "../results/plink.fam"
    shell:
        "python scripts/plink/fam_generate.py --input {input} --output {output}"


# rule create_file_fam:
#     input: 
#         "../results/input_puce.fam",
#         "../results/plink.map"
#         "../results/plink.lgen"
#     output: "../results/Full_data_clean.csv"
#     shell: "{input}"

# rule create_file_lgen:
#     input: 
#         "../results/plink.lgen"
#     output: "../results/Full_data_clean.csv"
#     shell: "{input}"