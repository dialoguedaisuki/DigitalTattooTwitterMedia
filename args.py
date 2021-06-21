import sys
import argparse


def args():
    # get args
    parser = argparse.ArgumentParser(
        description='search words(space separated),environment name')
    parser.add_argument('-w', '--words', metavar='words', type=str,
                        help='search words(space separated)', default="")
    parser.add_argument('-e', '--env', metavar='env', type=str,
                        help='environment name', default="")
    parser.add_argument('-l', '--list', metavar='list',
                        type=str, help="list slud id", default="")
    args = parser.parse_args()
    print(args)
    if args.env == "":
        print("No Argument")
        sys.exit()
    search_words = args.words
    print("search_words is " + str(search_words))
    envName = args.env
    slugid = args.list
    return search_words, envName, slugid
