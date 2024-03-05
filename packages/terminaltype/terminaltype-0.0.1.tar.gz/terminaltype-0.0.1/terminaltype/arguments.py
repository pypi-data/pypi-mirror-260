import argparse
import sys
from terminaltype.history import print_history

def parse_args():
    parser = argparse.ArgumentParser(prog="typing_test",
                                     description="A simple terminal-based typing test",
                                     usage="typing_test [-h] [-w {english200,english1000,italian200,italian1000,spanish200,spanish1000}] [-t TIME] [-H]",
                                     add_help=True
                                     )

    parser.add_argument("-w", "--words", 
                        type=str, 
                        default="english200",
                        choices=["english200", "english1000","italian200", "italian1000", "spanish200", "spanish1000"],
                        required=False,
                        )

    parser.add_argument("-t", "--time",
                        type=int,
                        default=60,
                        required=False,
                        choices=range(10, 120),
                        metavar="[10,120]"
                        )
    
    parser.add_argument("-H", "--history",
                        action="store_true",
                        required=False,
                        help="Show the history"
                        )

    return parser.parse_args()

def get_args():
    args = parse_args()

    if args.history:
        print_history()
        sys.exit(0)

    return args.words, args.time
