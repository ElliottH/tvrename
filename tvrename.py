#!/usr/bin/env python
from __future__ import print_function

import os
import sys

import argparse
import re
import shutil

class Colour(object):
    """Utility class for colour printing messages"""
    RED = '\033[91m'
    WHITE = '\033[97m'
    END = '\033[0m'

    @staticmethod
    def print(colour, msg, end="\n"):
        """Print msg in colour"""
        print("%s%s%s" % (colour, msg, Colour.END), end=end)

    @staticmethod
    def red(msg, end="\n"):
        """Print msg in red"""
        Colour.print(Colour.RED, msg, end)

    @staticmethod
    def white(msg, end="\n"):
        """Print msg in white"""
        Colour.print(Colour.WHITE, msg, end)

class Renamer(object):
    """
    Takes files in the following forms:
    * Awesome.Show.S01E01.SOURCE.FMT-GRP.ext
    * awesome.show.101.source-grp.ext
    It can then either:
    * rename the file to S01E01.ext
    * move the file to Awesome Show/S01/S01E01.ext
    """


    # It's important to test with SE before ALT, because ALT may erroneously
    # match SE format series names that contain the year.
    SE_REGEX = re.compile(r"^(.+)\.S(\d+)E(\d+).+\.(...)$", re.IGNORECASE)
    ALT_REGEX = re.compile(r"^(.+)\.(\d+)\.[^-]+?-[^.]+\.(...)$")

    def __init__(self, args):
        self.args = args

    @staticmethod
    def find_candidates(directory, pattern):
        """Find subdirectories of directory that match pattern"""
        list_path = [i for i in os.listdir(directory) if
                     os.path.isdir(os.path.join(directory, i))]
        return [os.path.join(directory, j) for j in list_path if
                re.match(pattern, j,
                         re.IGNORECASE)]

    @staticmethod
    def ask_candidates(candidates):
        """Ask the user to pick from a list"""
        Colour.white("Candidates are:")
        for (idx, name) in enumerate(candidates):
            print("[%d] %s" % (idx + 1, name))

        while True:
            choice = raw_input("%sChoice? [1-%d/Q]%s " % (Colour.WHITE,
                                                          len(candidates),
                                                          Colour.END))
            if choice.lower() == "q" or choice == "":
                return None
            elif choice.isdigit():
                val = int(choice) - 1
                if val < len(candidates) and val >= 0:
                    return candidates[val]

            print("Invalid selection '%s'." % choice)




    def move(self, files, directory):
        """
        Move files to their proper place

        We look for a directory inside the given directory that matches the show
        name, and then a directory inside that that matches the season number.

        For example, if we have a show awesome.show.s02e02.HDTV.x264-GRP.mp4 we
        will try to find a directory matching r"awesome.+show.*" and then a
        directory S02 inside that. Something like "Awesome Show/S02/".
        """
        for (fname, info) in [(f, self.split_name(f)) for f in files]:
            if not info:
                print("Unable to parse %s" % fname)
            else:
                (name, season, episode, extension) = info
                new_name = "S%02dE%02d.%s" % (season, episode, extension)
                pattern = os.path.basename(name).replace('.', '.+') + '.*'
                result = self.find_candidates(directory, pattern)

                if len(result) == 0:
                    Colour.red("Couldn't determine destination for %s." %
                               os.path.basename(fname))
                    continue
                elif len(result) > 1:
                    Colour.white("Couldn't determine desination for %s." %
                                 os.path.basename(fname))
                    destination = self.ask_candidates(result)
                    if destination == None:
                        continue
                else:
                    destination = result[0]

                destination = os.path.join(destination, "S%02d" % season)
                if os.path.isdir(destination):
                    self.confirm_move(fname, os.path.join(destination, new_name))
                else:
                    print("No directory S%02d in %s" % (season, destination))

    def rename(self, files):
        """Rename files to their proper names"""
        for (fname, info) in [(f, self.split_name(f)) for f in files]:
            if not info:
                print("Unable to parse %s", fname)
            else:
                (name, season, episode, extension) = info
                new_name = "S%02dE%02d.%s" % (season, episode, extension)
                new_path = os.path.join(os.path.dirname(name), new_name)
                self.confirm_move(fname, new_path)

    def confirm_move(self, src, dest):
        """
        Move file from src to dest

        * If args.dry_run is True, then we don't actually do anythin.
        * If args.confirm is True, then we ask first.
        """
        if os.path.isfile(dest):
            Colour.red("Not moving %s to %s as file already exists" % (src, dest))
        elif os.path.isdir(dest):
            Colour.red("Not moving %s to %s as it is a directory" % (src, dest))
        else:
            if self.args.dry_run:
                Colour.white("(Not) ", end="")
            print("Moving %s to %s" % (src, dest))

            if self.args.dry_run:
                return
            elif self.args.confirm:
                ans = raw_input("%sOK? [Y/n/q] %s" % (Colour.WHITE, Colour.END))
                if ans.lower() == "q":
                    sys.exit(0)
                elif ans.lower() != "y" and ans != "":
                    print("Skipping %s..." % src)
                    return

            shutil.move(src, dest)


    def split_name(self, fname):
        """Split a file name, fname, into its consituent parts"""
        match = self.SE_REGEX.match(fname)
        if match:
            season, episode = int(match.group(2)), int(match.group(3))
            return (match.group(1), season, episode, match.groups()[-1])
        else:
            match = self.ALT_REGEX.match(fname)
            if match:
                digits = match.group(2)
                season, episode = int(digits[:-2]), int(digits[-2:])
                return (match.group(1), season, episode, match.groups()[-1])
            else:
                return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--dry-run', help='just print what would be done',
                        action='store_true', dest='dry_run')
    parser.add_argument('-c', '--confirm', help='confirm before doing',
                        action='store_true')
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()

    renamer = Renamer(args)
    if len(args.files) > 1:
        if not os.path.isdir(args.files[-1]):
            print('Last argument is not a directory')
            sys.exit(1)
        else:
            renamer.move(args.files[0:-1], args.files[-1])
    else:
        renamer.rename(args.files)

if __name__ == "__main__":
    main()

