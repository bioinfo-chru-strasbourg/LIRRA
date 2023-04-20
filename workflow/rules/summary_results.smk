rule create_output:
    input:
        config["path"]["ROH_select"],
        config["path"]["final_dating"],
        config["path"]["plink_hom"],
        config["path"]["ROH_select"]
    output:
        config["path"]["excel_output"],     
        config["path"]["custom_track"] ,    
        config["path"]["global_summary"] ,    
        config["path"]["full_results"] ,    

    threads:1
    shell:
        "python scripts/final_summary.py"
