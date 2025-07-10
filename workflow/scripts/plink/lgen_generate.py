import pandas as pd
import re
import os
import argparse
import logging as log


class LgenFile:
    """This class are used for transform a raw datas into fam file. It's use like input for PLINK1.9"""

    def __init__(self, input: str, output: str, list_puce: str):
        self.input = input
        self.output = output
        self.list_puce = list_puce
        self.temporary_data = {}
        self.column_top_alleles = []
        self.data_temporary()

        self.famid_data = []
        self.sample_data = []
        self.snp_data = []
        self.all1_data = []
        self.all2_data = []
        self.generate_lgen()
        self.create_file_lgen()

    def data_temporary(self):
        """For decrease calcul time we create a dataframe temporary with many less columns. We split columns with
        xx.Top Alleles name for keep sample id and after"""
        data = pd.read_csv(self.input, sep="\t", index_col=0)
        self.temporary_data = data.iloc[:, 0]

        for i in range(data.shape[1]):
            # We keep only columns with Top Alleles informations
            string = data.columns[i]

            found_allele = re.search("Top Alleles", string)

            if found_allele != None:
                # keep top allele from raw and split them
                split_allele = string.split(".")
                self.column_top_alleles.append(split_allele[0])

                # update data_workflow for work behind
                data_workflow_add = data.iloc[:, i]
                self.temporary_data = pd.concat(
                    [self.temporary_data, data_workflow_add], axis=1, join="inner"
                )

    """
    Columns format ouput from dataframe temporary
    snpID  samplID_TopAllele1  samplID_TopAllele2  samplID_TopAllele3
    rs001          AG                  GG                  CT
    rs002          CC                  AA                  CT
    rs003          GA                  GA                  --
    """

    def generate_lgen(self):
        """We work with dataframe temporary, each values are dispatched and transform on list informations"""
        for y in range(self.temporary_data.shape[0]):
            self.sp_id_generate()
            for x in range(self.temporary_data.shape[1] - 1):
                self.snp_id_generate(y)
            for x in range(self.temporary_data.shape[1]):
                self.all_alleles_generate(y, x)

        self.fam_id_generate()

        """Control lenght for each columns of lfile"""
        log.info(len(self.all2_data), "alleles length")
        log.info(len(self.sample_data), "sample id length")
        log.info(len(self.snp_data), "snp length")
        log.info(len(self.famid_data), "fam length")

    def fam_id_generate(self):
        """puce liste should contains sample id with own family id. Each couple are add into dictionary then use for
        to fill lgen file"""
        puce_liste = pd.read_csv(self.list_puce, sep="\t")
        family_sample_columns = {}
        for i in range(puce_liste.shape[0]):
            family_sample_columns[puce_liste.iloc[i, 1]] = puce_liste.iloc[i, 0]

        for i in range(len(self.sample_data)):
            sample = self.sample_data[i]
            self.famid_data.append(family_sample_columns.get(sample))

    def sp_id_generate(self):
        for i in range(len(self.column_top_alleles)):
            self.sample_data.append(self.column_top_alleles[i])

    def snp_id_generate(self, y: int):
        self.snp_data.append(self.temporary_data.iloc[y, 0])

    def all_alleles_generate(self, y: int, x: int):
        """We split genoptype into 2 collumns. One allele for one column and if this allele are = '-' it's change into 0"""
        if x == 0:
            pass
        else:
            gt_data = self.temporary_data.iloc[y, x]
            if gt_data == "--":
                self.all1_data.append(0)
                self.all2_data.append(0)
            else:
                try:
                    self.all1_data.append(gt_data[0])
                except TypeError as e:
                    self.temporary_data.to_csv(
                        "/home1/HUB/bin/data/lirra_tmp_data.tsv",
                        sep="\t",
                        index=True,
                        na_rep="NA_debug",
                    )
                    print(
                        "Column names of temporary_data:", self.temporary_data.columns
                    )
                    print("gt_data", gt_data)
                    print("y", y)
                    print("x", x)
                    raise e
                self.all2_data.append(gt_data[1])

    def create_file_lgen(self):
        output_dir = os.path.dirname(self.output)  # recupere le chemin
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        df_lgen = pd.DataFrame(
            {
                "Family ID": self.famid_data,
                "Sample": self.sample_data,
                "snp_ID": self.snp_data,
                "Allele 1": self.all1_data,
                "Allele2": self.all2_data,
            }
        )
        df_lgen.to_csv(self.output, sep="\t", header=None, index=None)


def main():
    parser = argparse.ArgumentParser(
        prog="lgen_generate.py", formatter_class=argparse.MetavarTypeHelpFormatter
    )

    parser.add_argument(
        "-i",
        "--input",
        help="input file after rule clean_data ",
        type=str,
        required=True,
    )

    parser.add_argument(
        "-o",
        "--output",
        help="output file contains cM informations",
        type=str,
        required=True,
    )

    parser.add_argument(
        "-df",
        "--data_family",
        help="data family come from your data",
        type=str,
        required=False,
        default=os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "config", "list_puce_fam.fam"
        ),
    )

    args = parser.parse_args()
    LgenFile(args.input, args.output, args.data_family)


if __name__ == "__main__":
    main()
