from argparse import ArgumentParser
from sys import argv
import sys

class arguments():
    def argsFunc():
        parser = ArgumentParser()
        parser.add_argument(
            "--old",
            "-o",
            type=str,
            help = "Old image with version. Example: mysql:1.2"
        )
        parser.add_argument(
            "--new",
            "-n",
            type=str,
            help = "New image with version. Example: mysql:1.3"
        )
        parser.add_argument(
            "-p",
            "--product",
            type=str,
            nargs= "+",
            help = "The product name. Example: MISA AMIS"
        )
        parser.add_argument(
            "--version",
            "-v",
            type=str,
            help = "The release version. Example: R1"
        )
        parser.add_argument(
            "--authen",
            "-a",
            type=str,
            help = "Path to credential file (JSON format). Example: smb_config.json"
        )        
        argsList = []
        args = vars(parser.parse_args())
        oldOmage = args["old"]
        newImage = args["new"]
        productName = args["product"]
        version = args["version"]
        authen = args["authen"]
        if args["product"]: productName = ' '.join(args["product"])
        # output = args["output"]
        
        argsList.append(oldOmage)
        argsList.append(newImage)
        argsList.append(productName)
        argsList.append(version)
        argsList.append(authen)
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
        if not authen:
            print("\nError: The SMB credential file required!\n")
            parser.print_help()
            sys.exit(1)            
        return argsList
    
