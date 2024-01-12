from argparse import ArgumentParser
from sys import argv
import sys

class arguments():
    def argsFunc():
        parser = ArgumentParser()
        parser.add_argument(
            "--old-image",
            "-o",
            type=str,
            help = "Old image with version. Example: mysql:1.2"
        )
        parser.add_argument(
            "--new-image",
            "-n",
            type=str,
            help = "New image with version. Example: mysql:1.3"
        )
        # parser.add_argument(
        #     "--version",
        #     "-v",
        #     type=str,
        #     help = "The release version. Example: R1"
        # )
        parser.add_argument(
            "-p",
            "--product-name",
            type=str,
            nargs= "+",
            help = "The product name. Example: MISA AMIS"
        )
        # parser.add_argument(
        #     "--output",
        #     "-o",
        #     default = "result",
        #     type=str,
        #     help = "The location file to write the report output to (default: \\\\storage1\\DU_LIEU_CHUYEN_RA_NGOAI\\Compare_file)"
        # )
        argsList = []
        args = vars(parser.parse_args())
        oldOmage = args["old-image"]
        newImage = args["new-image"]
        # version = args["version"]
        productName = args["product-name"]
        if args["product-name"]: productName = ' '.join(args["product-name"])
        # output = args["output"]
        
        argsList.append(oldOmage)
        argsList.append(newImage)
        # argsList.append(version)
        argsList.append(productName)
        # argsList.append(output)

        if len(argv) < 1:
            parser.print_help()
            sys.exit(1)

        if not oldOmage and not newImage:
            print("\nError: The path to the source code of the current and release version required!\n")
            parser.print_help()
            sys.exit(1)
        if not newImage:
            print("\nError: The path to the source code for release required!\n")
            parser.print_help()
            sys.exit(1)
        # if not version:
        #     print("\nError: The release version required!\n")
        #     parser.print_help()
        #     sys.exit(1)
        if not productName:
            print("\nError: The product name required!\n")
            parser.print_help()
            sys.exit(1)
        return argsList
    