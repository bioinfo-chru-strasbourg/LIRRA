import argparse
import logging as log
import os
import sys

import lirra
from lirra.init_config import InitConfig
from lirra.commons import set_log_level


def main():
    parser = argparse.ArgumentParser(
        prog="lirra",
        formatter_class=argparse.MetavarTypeHelpFormatter,
    )
    parser.add_argument("--version", action="version")

    parser.add_argument(
        "-ROHs",
        "--ROH_software",
        type=str,
        required=True,
        choices=("plink", "hap-ibd"),
        help='Choose which software you want to find ROHs ["plink" or "hap-ibd"]',
    )
    # print(args.ROH_software)
    parser.add_argument(
        "-Ds",
        "--Dating_software",
        type=str,
        required=False,
        default="R_mutation",
        choices=("R_mutation", "Estimat"),
        help='Choose which software you want to dating variants ["R_mutation" or "Estimat"]',
    )

    parser.add_argument(
        "-n",
        "--ncores",
        type=int,
        required=False,
        default=6,
        help="Number of cores for multiprocessing [default: 6]",
    )
    parser.add_argument(
        "-Ic",
        "--Ignore_centromere",
        type=str,
        required=True,
        choices=("True", "False"),
        help="If you want ignore centromere choose True else False",
        # TODO: en voix de developpement pour detecter les proximités du centromere
    )
    parser.add_argument(
        "-Di",
        "--Data_input",
        type=str,
        required=True,
        choices=("VCF", "SNP"),
        help='Which type are your data ["VCF" or "SNP"]',
    )

    parser.add_argument(
        "-vf",
        "--variant_frequency",
        type=float,
        required=True,
        help="variant frequency if you know for dating_r_mutation",
    )

    parser.add_argument(
        "-l",
        "--location",
        type=str,
        required=True,
        help="variant frequency if you know for dating_r_mutation",
    )

    parser.add_argument(
        "-r",
        "--ram",
        type=int,
        required=True,
        help="alocation ram for run beagle",
    )

    parser.add_argument(
        "-cc",
        "--confidence_coefficient",
        type=float,
        required=False,
        default=0.95,
        help="The confidence coefficcient for r-dating-mutation",
    )

    parser.add_argument(
        "-cd",
        "--correction_dating",
        type=str,
        required=False,
        default="False",
        choices=("True", "False"),
        help="If you want activate correction option for dating r mutation",
    )

    parser.add_argument(
        "--Analysis_mode",
        type=str,
        required=False,
        default="by_gene",
        choices=("by_gene", "All"),
        help="You can change the analysis to detect ROH based on a specific location in the genome [by_gene, All]",
    )

    parser.add_argument(
        "--Analysis_output",
        "-Ao",
        type=str,
        required=False,
        default="founder_effect",
        choices=("founder_effect", "homozigosity"),
        help="You can change the analysis to detect ROH based on a specific location in the genome [founder_effect, homozigosity]",
    )
    # TODO : For select if you want a list of genes or just ROH include variant, upgrade for change required of location into False

    args = parser.parse_args()
    InitConfig(args)


if __name__ == "__main__":
    main()
