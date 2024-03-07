"""
PSCAD Automation Library
"""

import os
import mhi.common, mhi.pscad

from argparse import ArgumentParser, Namespace
from mhi.common.zipper import LibraryZipper
from mhi.pscad.buildtime import BUILD_TIME


def version(args: Namespace):
    print("MHI PSCAD Library v{} ({})".format(mhi.pscad.VERSION, BUILD_TIME))
    print("(c) Manitoba Hydro International Ltd.")
    print()
    print(mhi.common.version_msg())

def show_help(args: Namespace):
    chm = os.path.join(os.path.dirname(__file__), 'PSCAD_AL_doc.chm')
    os.startfile(chm)

def main():
    parser = ArgumentParser(prog='py -m mhi.pscad')
    parser.set_defaults(func=version)
    subparsers = parser.add_subparsers()

    updater = LibraryZipper('PSCAD', 'mhi.pscad', 'mhi.common')
    updater.add_subparser(subparsers)

    helper = subparsers.add_parser('help', help="Open the module's help file")
    helper.set_defaults(func=show_help)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
