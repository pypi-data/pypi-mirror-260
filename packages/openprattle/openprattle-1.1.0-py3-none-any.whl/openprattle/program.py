import sys
import argparse

import openprattle
from openprattle import Openbabel_converter, HAVE_PYBEL, formats
import openprattle.log

def main():
    """
    Main entry point for the program.
    """
    # Get our args from the command line.
    parser = argparse.ArgumentParser(
#        description = DESCRIPTION,
#        epilog = EPILOG
    )
    
    parser.add_argument("input_file", help = "Input file to read and convert from. If not given, the file will be read from stdin. ", nargs = "?", default = "-")
    parser.add_argument("-i", "--input_format", help = "Input format. If not given, the input format is assumed based on the input file extension.")
    parser.add_argument("-o", "--output_format", help = "Output format. If not given, the input format is assumed based on the output file extension.")
    parser.add_argument("-O", "--output_file", help = "Output file to write to. If not given, the file will be written to stdout.", default = "-")
    parser.add_argument("-C", "--charge", help = "The molecular charge to set in the output format. Note that not all formats support a charge.", default = None, type = int)
    parser.add_argument("-M", "--multiplicity", help = "The multiplicity to set in the output format. Note that not all formats support a multiplicity", default = None, type = int)
    parser.add_argument("--gen3D", help = "Whether to optimise the input coordinates via a rapid force-field optimisation. This option is useful for converting 1D or 2D formats to 3D. The default (Auto) is to only optimise coordinates that are not already in 3 dimensions.", choices = ["True", "Auto", "False"])
    parser.add_argument("--backend", help = "Force the user of a particular backend", choices = ["Auto", "Pybel", "Obabel"])
    
    parser.add_argument("--bindings", help = "Determine whether the pybel bindings are available", action = "store_true")
    parser.add_argument("--readable", help = "List readable (input) formats", action = "store_true")
    parser.add_argument("--writable", help = "List writable (output) formats", action = "store_true")
    parser.add_argument("--json", help = "Dump the list of readable and/or writable formats in JSON, and dump warnings and errors in JSON", action = "store_true")
    parser.add_argument("-v", "--version", action = "version", version = str(openprattle.__version__))

    args = parser.parse_args()

    # First, setup logging.
    if args.json:
        openprattle.log.init_logger(True)

    if args.bindings:
        if HAVE_PYBEL:
            print(True)
        
        else:
            print(False)
        
        exit(0)
    
    elif args.readable or args.writable:
        format = formats(args.backend)

        if args.json:
            import json
            if args.readable:
                print(json.dumps(format.read()))
            
            if args.writable:
                print(json.dumps(format.write()))
            
        else:
            if args.readable:
                for key, value in format.read().items():
                    print("{:10} : {}".format(key, value))
                
            if args.writable:
                for key, value in format.write().items():
                    print("{:10} : {}".format(key, value))
        
        return


    # First, get our converter object
    converter = Openbabel_converter.from_file(
        input_file_path = args.input_file if args.input_file != "-" else None,
        input_file = sys.stdin if args.input_file == "-" else None,
        input_file_type = args.input_format,
        backend = args.backend
    )

    # Handle gen3D.
    if args.gen3D == "True":
        gen3D = True
    
    elif args.gen3D == "False":
        gen3D = False

    else:
        gen3D = None

    # Then convert.
    result = converter.convert(
        output_file = args.output_file if args.output_file != "-" else None,
        output_file_type = args.output_format,
        charge = args.charge,
        multiplicity = args.multiplicity,
        gen3D = gen3D
    )

    # If we're writing to stdout, print.
    # TODO: See if we can write directly to stdout from pybel.
    if args.output_file == "-":
        print(result, end = "")

    return 0