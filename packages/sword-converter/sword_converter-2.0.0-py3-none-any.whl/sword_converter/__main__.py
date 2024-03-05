import argparse

from sword_converter.converters.bible import Bible
from sword_converter.utils import metadata


def main():
    parser = argparse.ArgumentParser(description=metadata.summary)
    parser.add_argument("source", help="path to the zip file containing a sword module")
    parser.add_argument("module", help="name of the sword module to load")
    parser.add_argument("-f", "--format", choices=("json", "sqlite"), default="json",
                        help="file format of the output to be generated")
    parser.add_argument("-v", "--version", action="version", version=f"{metadata.name} {metadata.version}")

    args = parser.parse_args()

    bible = Bible(args.source, args.module)

    if args.format == "json":
        bible.to_json()
    elif args.format == "sqlite":
        bible.to_sqlite()


if __name__ == "__main__":
    main()
