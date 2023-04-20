import os
import polars as pl
import pandas as pd
import yaml


class OutputExcelSummary:
    def __init__(self) -> None:
        self.init_path_files()
        self.init_mutation_position()
        self.create_output()

    def init_path_files(self):
        self.path_roh_interest = os.path.join(
            os.path.dirname(__file__), "..", "..", "results", "ROH_select.tsv"
        )
        self.path_target = os.path.join(
            os.path.dirname(__file__), "..", "..", "config", "target_data.tsv"
        )
        self.path_plink_hom = os.path.join(
            os.path.dirname(__file__), "..", "..", "results", "plink.hom"
        )
        self.path_dating = os.path.join(
            os.path.dirname(__file__), "..", "..", "results", "dating.txt"
        )
        self.path_summary = os.path.join(
            os.path.dirname(__file__), "..", "..", "results"
        )
        self.target = pl.read_csv(self.path_target, separator="\t")
        self.plink_hom = pl.read_csv(self.path_plink_hom, separator="\t")
        self.roh_interest = pl.read_csv(
            self.path_roh_interest, separator="\t", has_header=False
        )

    def init_mutation_position(self):
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
            return str(prime_service["variant_informations"]["location_variant"])

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

        self.nb_roh_tot = [self.plink_hom.shape[0]]
        self.prepare_file()
        self.nb_roh_interest = [0]
        for row in range(len(self.data_work)):
            if "chr" + str(self.data_work[row][3]) == self.chr_interest:
                self.nb_roh_interest[0] = self.nb_roh_interest[0] + 1

        #     "Dating": dating
        #     "Confidence": dating
        nb_line = 0
        with open(self.path_dating, "r") as dating_file:
            for row in dating_file:
                if nb_line == 1:
                    self.dating_str = (
                        "independant "
                        + str(float(row.split("= ")[1].split(" generation")[0]) * 25)
                        + " years"
                    )
                    self.confidence_str = "independant " + str(
                        row.split("(")[1].split(")")[0]
                    )
                if nb_line == 2:
                    self.dating_str = (
                        self.dating_str
                        + " / correlated "
                        + str(float(row.split("= ")[1].split(" generation")[0]) * 25)
                        + " years"
                    )
                    self.confidence_str = (
                        self.confidence_str
                        + " / correlated "
                        + str(row.split("(")[1].split(")")[0])
                    )
                nb_line = nb_line + 1
        self.dating = [self.dating_str]
        self.confidence = [self.confidence_str]
        self.sample_find = (
            str(len(self.roh_interest["column_2"]))
            + "/"
            + str(len(self.target["Sample"]))
        )

    def prepare_file(self):
        data = pl.read_csv(self.path_plink_hom, skip_rows=1, has_header=False)
        self.data_work = []
        for row in data["column_1"]:
            self.data_work.append(str(row).split())

    def output_by_group(self):
        self.sample_id = self.roh_interest["column_2"].to_list()
        self.length_roh = self.roh_interest["column_9"].to_list()
        self.nb_snp = self.roh_interest["column_10"].to_list()
        self.density = self.roh_interest["column_11"].to_list()

    def output_view(self):
        self.chromstart = self.roh_interest["column_7"].to_list()
        self.chromend = self.roh_interest["column_8"].to_list()
        self.chrom = [self.chr_interest] * len(self.chromend)
        # print(self.chrom)
        self.name = self.roh_interest["column_2"].to_list()

    def create_output(self):
        self.output_global()
        self.output_by_group()
        self.output_view()
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

        output_by_group = pd.DataFrame(
            {
                "Sample ID": self.sample_id,
                "Length ROH": self.length_roh,
                "Nb SNP": self.nb_snp,
                "Density": self.density,
            },
        )

        writer = pd.ExcelWriter(
            f"{self.path_summary}/summary.xlsx",
            engine="xlsxwriter",
        )
        output_global.to_excel(writer, sheet_name="Global_summary", index=False)
        output_by_group.to_excel(writer, sheet_name="Focus in group", index=False)
        # output_focus_all_patients.to_excel(writer, sheet_name="All patients")
        # # TODO: Il faudrait avoir plusieurs output par groupe avec le nb de groupe dans la target
        writer.close()

        output_by_group.to_csv(
            f"{self.path_summary}/full_results.tsv", index=False, sep="\t"
        )
        output_global.to_csv(
            f"{self.path_summary}/global_summary.tsv", index=False, sep="\t"
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
