import pandas as pd
import argparse
import os


class fam_file:
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
        path_lgen=str(self.output).split("/")
        path_lgen=path_lgen[:len(path_lgen)-1]
        path_lgen.append("puce_for_lgen.fam")
        print("/".join(path_lgen))
        return "/".join(path_lgen)

        


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
        help="output file",
        type=str,
        required=True,
    )

    args = parser.parse_args()
    # print(args.input)
    # print(args.output)
    # print(args.data_family)
    fam_file(args.input, args.output)


if __name__ == "__main__":
    main()
