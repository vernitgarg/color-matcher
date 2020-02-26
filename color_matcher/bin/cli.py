#!/usr/bin/env python

__author__ = "Christopher Hahne"
__email__ = "info@christopherhahne.de"
__license__ = """
    Copyright (c) 2020 Christopher Hahne <info@christopherhahne.de>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import getopt
import sys, os

from color_matcher import __version__
from color_matcher.top_level import ColorMatcher
from color_matcher.io_handler import *


def usage():

    print("Usage: color_matcher <options>\n")
    print("Options:")
    print("-s <path>,     --src=<path>       Specify source image file or folder of source files to process")
    print("-r <filepath>, --ref=<filepath>   Specify target image file")
    print("-m <method>,   --method=<method>  Provide color transfer method, e.g. 'hist' or 'mvgd'")
    print("-w ,           --win              Select files from window")
    print("")
    print("-h,            --help             Print this help message")
    print("")

    sys.exit()


def parse_options(argv):

    try:
        opts, args = getopt.getopt(argv, "hs:r:m:w", ["help", "src=", "ref=", "method="])
    except getopt.GetoptError as e:
        print(e)
        sys.exit(2)

    cfg = dict()

    # default settings (use test data images for MKL conversion)
    cfg['src_path'] = '' #os.path.join('..', 'test', 'data', 'scotland_house.png')
    cfg['ref_path'] = '' #os.path.join('..', 'test', 'data', 'scotland_plain.png')
    cfg['win'] = None

    if opts:
        for (opt, arg) in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit()
            if opt in ("-s", "--src"):
                cfg['src_path'] = arg
            if opt in ("-r", "--ref"):
                cfg['ref_path'] = arg
            if opt in ("-m", "--method"):
                cfg['method'] = arg
            if opt in ("-w", "--win"):
                cfg['win'] = True

    # create dictionary containing all parameters for the light field
    return cfg


def main():

    # program info
    print("\ncolor_matcher v%s \n" % __version__)

    # parse options
    cfg = parse_options(sys.argv[1:])

    # select files from window
    if cfg['win']:
        cfg['src_path'] = select_file(cfg['src_path'], 'Select source image')
        cfg['ref_path'] = select_file(cfg['ref_path'], 'Select reference image')

    # select light field image(s) considering provided folder or file
    if os.path.isdir(cfg['src_path']):
        filenames = [f for f in os.listdir(cfg['src_path']) if f.lower().endswith(FILE_EXTS)]
    elif not os.path.isfile(cfg['src_path']) or not os.path.isfile(cfg['ref_path']):
        print('File not found \n')
        sys.exit()
    else:
        filenames = [cfg['src_path']]

    # cancel if file paths not provided
    if not cfg['src_path'] or not cfg['ref_path']:
        print('Canceled due to missing image file path')
        sys.exit()

    # file handling
    output_path = os.path.join(os.path.dirname(cfg['src_path']), 'color_match_results')
    try:
        os.makedirs(output_path, 0o755)
    except OSError:
        pass

    ref = load_img_file(cfg['ref_path'])

    for f in filenames:
        src = load_img_file(f)
        res = ColorMatcher(src=src, ref=ref, ).main()
        save_img_file(res, file_path=os.path.join(output_path, os.path.basename(cfg['src_path'])))


if __name__ == "__main__":

    sys.exit(main())
