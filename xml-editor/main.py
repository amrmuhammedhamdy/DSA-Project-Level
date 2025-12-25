#!/usr/bin/env python3
import argparse
from operations import compressor, decompressor, minifier, parser, formatter, converter, fixer

def main():
    parser_cli = argparse.ArgumentParser(description="XML_Editor")
    parser_cli.add_argument("command", choices=["verify", "format", "json", "mini","compress","decompress"])
    parser_cli.add_argument("-i", "--input", required=True)
    parser_cli.add_argument("-o", "--output", required=False)
    parser_cli.add_argument("-f", "--fix", action="store_true")
    args = parser_cli.parse_args()

    if args.command == "verify":
        parser.verify(args.input, args.output if args.fix else None)
    elif args.command == "format":
        formatter.format_xml(args.input, args.output)
    elif args.command == "json":
        converter.xml_to_json(args.input, args.output)
    elif args.command == "mini":
        minifier.minify(args.input, args.output)
    elif args.command == "compress":
        compressor.compress(args.input, args.output)
    elif args.command == "decompress":
        decompressor.decompress(args.input, args.output)

if __name__ == "__main__":
    main()
