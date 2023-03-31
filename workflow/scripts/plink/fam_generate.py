import pandas as pd
import argparse


class FamFile:
    """This class are used for transform a raw data into fam file. It's use like input for PLINK1.9"""

    def __init__(self, file_name, output):
        self.file_name = file_name
        self.output = output
        self.data_transform()

    def data_transform(self):
        """We transform nan values into 0 like format for PLINK"""
        data = pd.read_csv(self.file_name, sep="\t")
        id_mother = []
        id_father = []
        for i in range(data.shape[0]):
            if str(data.iloc[i, 2]) == "nan":
                id_father.append(0)
            else:
                id_father.append(data.iloc[i, 2])

            if str(data.iloc[i, 3]) == "nan":
                id_mother.append(0)
            else:
                id_mother.append(data.iloc[i, 3])

        final_fam = pd.DataFrame(
            {
                "Family_id": data.iloc[:, 0],
                "Sample": data.iloc[:, 1],
                "Father_id": id_father,
                "Mother_id": id_mother,
                "Sex": data.iloc[:, 4],
                "Phenotype": data.iloc[:, 5],
            }
        )
        final_fam.to_csv(self.output, sep="\t", header=None, index=None)
        final_fam.to_csv(self.path_lgen(), sep="\t", index=None)

    def path_lgen(self):
        print(self.output)
        path_lgen = str(self.output).split("/")
        path_lgen = path_lgen[: len(path_lgen) - 1]
        path_lgen.append("puce_for_lgen.fam")
        print("/".join(path_lgen))
        return "/".join(path_lgen)

    __doc__ = """
    Input example:
    Family ID	Sample ID	Paternal ID	Maternal ID	Sex (1=M, 2=F)	Phenotype (1=unaffected, 2=affected)
    FAM1	sample1			2	2
    FAM2	sample2			1	2
    FAM3	sample3			2	2
    FAM3	sample4			1	2

    Output example (no header):
    FAM1	sample1 0   0   2   2
    FAM2	sample2 0   0   1   2
    FAM3	sample3 0   0   2   2
    FAM3	sample4 0   0   1   2
    """


def main():
    parser = argparse.ArgumentParser(
        prog="fam_generate.py", formatter_class=argparse.MetavarTypeHelpFormatter
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
        help="output file after script",
        type=str,
        required=True,
    )

    args = parser.parse_args()
    FamFile(args.input, args.output)


if __name__ == "__main__":
    main()
