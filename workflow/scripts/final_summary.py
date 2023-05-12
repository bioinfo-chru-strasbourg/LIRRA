import os
import polars as pl
import pandas as pd
import yaml
import logging as log
from homozigosity_individual import HomozigosityIndividual


class OutputExcelSummary:
    def __init__(self) -> None:
        self.init_config()
        self.init_path_files()
        self.prepare_file()
        self.create_output()

    def init_path_files(self):
        self.path_roh_interest = os.path.join(
            os.path.dirname(__file__), "..", "..", "results", "ROH_select.tsv"
        )
        self.path_target = os.path.join(
            os.path.dirname(__file__), "..", "..", "config", "target_data.tsv"
        )
        if self.roh_software == "plink":
            self.path_data_hom = os.path.join(
                os.path.dirname(__file__), "..", "..", "results", "plink.hom"
            )
        elif self.roh_software == "hap-ibd":
            if not os.path.exists(self.path_hbd):
                os.system(f"gunzip {self.path_hbd_gz}")
                if not os.path.exists(self.path_hbd_gz):
                    log.critical("they are not hbd.gz or hbd in results")

            self.path_data_hom = self.path_hbd

        self.path_dating = os.path.join(
            os.path.dirname(__file__), "..", "..", "results", "dating.txt"
        )
        self.path_summary = os.path.join(
            os.path.dirname(__file__), "..", "..", "results"
        )
        self.target = pl.read_csv(self.path_target, separator="\t")
        if self.roh_software == "plink":
            self.plink_hom = pl.read_csv(self.path_data_hom, separator="\t")
            self.roh_interest = pl.read_csv(
                self.path_roh_interest, separator="\t", has_header=False
            )

        elif self.roh_software == "hap-ibd":
            self.hap_ibd_hom = pl.read_csv(self.path_hbd, separator="\t")
            self.roh_interest = pl.read_csv(
                self.path_roh_interest, separator="\t", has_header=False
            )

    def init_config(self):
        with open(
            os.path.join(
                os.path.dirname(__file__), "..", "..", "config", "config.yaml"
            ),
            "r",
        ) as file:
            prime_service = yaml.safe_load(file)
            self.chr_interest = str(
                prime_service["variant_informations"]["location_variant"]
            ).split(":")[0]
            self.roh_software = prime_service["params"]["ROH_detect_software"]
            self.path_hbd_gz = prime_service["path"]["hap-ibd_hbd_gz"]
            self.path_hbd = prime_service["path"]["hap-ibd_hbd"]

    def output_global(self):
        dict_output_global = {}
        self.group = list(set(self.target["Group"].to_list()))
        dict_output_global["Group"] = list(set(self.target["Group"].to_list()))
        self.sample_tot = [0] * len(dict_output_global["Group"])
        self.nb_same_fam = [0] * len(dict_output_global["Group"])
        all_fam = self.target["Family(pedigree)"].to_list()

        for row in self.target.iter_rows(named=True):
            index_group = dict_output_global["Group"].index(row["Group"])
            self.sample_tot[index_group] = self.sample_tot[index_group] + 1
            if all_fam.count(row["Family(pedigree)"]) != 1:
                self.nb_same_fam[index_group] = self.nb_same_fam[index_group] + 1
        log.debug(self.group)
        log.debug(self.sample_tot)
        log.debug(self.nb_same_fam)

        # Dating informations
        with open(self.path_dating, "r") as dating_file:
            nb_line = 0
            for row in dating_file:
                if nb_line == 1:
                    self.dating_str = (
                        "independant "
                        + str(float(row.split("= ")[1].split(" generation")[0]) * 25)
                        + " years"
                    )
                    self.confidence_str = f"independant [{float(row.split('(')[1].split(')')[0].split(',')[0])*25},{float(row.split('(')[1].split(')')[0].split(',')[1])*25}] years"

                if nb_line == 2:
                    self.dating_str = (
                        self.dating_str
                        + " / correlated "
                        + str(float(row.split("= ")[1].split(" generation")[0]) * 25)
                        + " years"
                    )
                    self.confidence_str = f"{self.confidence_str} /correlated [{float(row.split('(')[1].split(')')[0].split(',')[0])*25},{float(row.split('(')[1].split(')')[0].split(',')[1])*25}] years"
                nb_line = nb_line + 1
        self.dating = [self.dating_str]
        self.confidence = [self.confidence_str]

        if self.roh_software == "plink":
            self.nb_roh_tot = [self.plink_hom.shape[0]]
            self.nb_roh_interest = [0]
            for row in range(len(self.data_work)):
                if "chr" + str(self.data_work[row][3]) == self.chr_interest:
                    self.nb_roh_interest[0] = self.nb_roh_interest[0] + 1

            self.sample_find = (
                str(len(self.roh_interest["column_2"]))
                + "/"
                + str(len(self.target["Sample"]))
            )

        elif self.roh_software == "hap-ibd":
            self.nb_roh_tot = [self.hap_ibd_hom.shape[0]]
            self.nb_roh_interest = [0]
            for row in self.data_work.iter_rows(named=True):
                if row["column_5"] == self.chr_interest:
                    self.nb_roh_interest[0] = self.nb_roh_interest[0] + 1
            self.sample_find = (
                str(len(self.roh_interest["column_1"]))
                + "/"
                + str(len(self.target["Sample"]))
            )
        log.debug(self.nb_roh_tot)
        log.debug(self.nb_same_fam)
        log.debug(self.nb_roh_interest)
        log.debug(self.sample_find)

    def prepare_file(self):
        if self.roh_software == "plink":
            data = pl.read_csv(self.path_data_hom, skip_rows=1, has_header=False)
            self.data_work = []
            for row in data["column_1"]:
                self.data_work.append(str(row).split())
        elif self.roh_software == "hap-ibd":
            self.data_work = pl.read_csv(
                self.path_data_hom, has_header=False, separator="\t"
            )
            print(self.data_work)

    def output_by_group(self):
        if self.roh_software == "plink":
            self.sample_id = self.roh_interest["column_2"].to_list()
            self.length_roh = self.roh_interest["column_9"].to_list()
            self.nb_snp = self.roh_interest["column_10"].to_list()
            self.density = self.roh_interest["column_11"].to_list()
        elif self.roh_software == "hap-ibd":
            self.sample_id = self.roh_interest["column_1"].to_list()
            self.length_roh = self.roh_interest["column_8"].to_list()
            self.nb_snp = [""] * len(self.sample_id)
            self.density = [""] * len(self.sample_id)

    def output_view(self):
        if self.roh_software == "plink":
            self.chromstart = self.roh_interest["column_7"].to_list()
            self.chromend = self.roh_interest["column_8"].to_list()
            self.chrom = [self.chr_interest] * len(self.chromend)
            self.name = self.roh_interest["column_2"].to_list()
        elif self.roh_software == "hap-ibd":
            self.chromstart = self.roh_interest["column_6"].to_list()
            self.chromend = self.roh_interest["column_7"].to_list()
            self.chrom = [self.chr_interest] * len(self.chromend)
            self.name = self.roh_interest["column_1"].to_list()

    def create_output(self):
        self.output_global()
        self.output_by_group()
        self.output_view()
        if self.roh_software == "plink":
            output_by_group = pd.DataFrame(
                {
                    "Sample ID": self.sample_id,
                    "Length ROH (kb)": self.length_roh,
                    "Nb SNP": self.nb_snp,
                    "Density": self.density,
                },
            )
        elif self.roh_software == "hap-ibd":
            output_by_group = pd.DataFrame(
                {
                    "Sample ID": self.sample_id,
                    "Length ROH (cM)": self.length_roh,
                    "Nb SNP": self.nb_snp,
                    "Density": self.density,
                },
            )

        output_global = pd.DataFrame(
            {
                "Group": self.group,
                "Nb sample tot": self.sample_tot,
                "Nb sample in same family": self.nb_same_fam,
                "Nb ROH tot": self.nb_roh_tot,
                "Nb ROH interest": self.nb_roh_interest,
                "Dating": self.dating,
                "Confidence": self.confidence,
                "Nb sample find": [self.sample_find],
            }
        )

        homozigosity_output = HomozigosityIndividual()
        # print(homozigosity_output)

        writer = pd.ExcelWriter(
            f"{self.path_summary}/summary.xlsx",
            engine="xlsxwriter",
        )
        output_global.to_excel(writer, sheet_name="Global_summary", index=False)
        output_by_group.to_excel(writer, sheet_name="Focus in group", index=False)
        homozigosity_output.df_homo.to_excel(
            writer, sheet_name="homozigosity", index=False
        )
        # output_focus_all_patients.to_excel(writer, sheet_name="All patients")
        # # TODO: Il faudrait avoir plusieurs output par groupe avec le nb de groupe dans la target
        writer.close()

        output_by_group.to_csv(
            f"{self.path_summary}/full_results.tsv", index=False, sep="\t"
        )
        output_global.to_csv(
            f"{self.path_summary}/global_summary.tsv", index=False, sep="\t"
        )
        homozigosity_output.df_homo.to_csv(
            f"{self.path_summary}/homozigosity.tsv",
            index=False,
            sep="\t",
        )

        output_view = pd.DataFrame(
            {
                "#chrom": self.chrom,
                "chromStart": self.chromstart,
                "chromEnd": self.chromend,
                "name": self.name,
            }
        )

        output_view.to_csv(
            f"{self.path_summary}/custom_track.tsv", sep="\t", index=False
        )


if __name__ == "__main__":
    OutputExcelSummary()
    # print("hello")
    # lines=[]
    # with open(os.path.join(os.path.dirname(__file__),"..","..","..","results","summary.txt"),"a") as summary_file:
    #     pass

    # En cours voire avec Jean
