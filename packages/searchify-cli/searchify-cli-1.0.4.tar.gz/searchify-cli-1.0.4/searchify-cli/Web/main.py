import sys
from Web.web_search import search
import argparse
from install import main

def main():
    parser = argparse.ArgumentParser(description="Search the web from the command line")
    parser.add_argument("query", type=str, help="The search query")
    parser.add_argument(
        "--no", type=int, default=1, help="The result number to display (default: 1)"
    )
    parser.add_argument(
        "--link", action="store_true", help="Include link in the search result"
    )
    parser.add_argument(
        "--title", action="store_true", help="Include title in the search result"
    )
    parser.add_argument("--copy", action="store_true", help="Copy link to clipboard")

    parser.add_argument("--all", action="store_true", help="Display top 10 results")

    args = parser.parse_args()

    search(args.query, args.no, args.link, args.title, args.copy, args.all)


if __name__ == "__main__":
    main()
