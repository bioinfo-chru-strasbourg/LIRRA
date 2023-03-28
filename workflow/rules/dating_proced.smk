rule roh_select:
    input:
        "../results/plink.hom"
    output:
        "../results/ROH_select.txt"
    shell:
        "python scripts/plink/select_patients.py"