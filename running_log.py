from all_runs import all_runs
from utilities import utilities
from constants import constants
from reader import reader

import os.path
import json
import argparse
import types

import pdb

def parseArgs():
    parser = argparse.ArgumentParser(description="Running log program.")
    parser.add_argument("-t", "--template", action='store_true', help="Generate template file")
    parser.add_argument("-lj", "--load_json", type=str, default="", nargs='*', help="Directory to load")

    parser.add_argument("-l", "--load_df", action='store_true', help="Load data frame existing data")

    parser.add_argument("-ns", "--dont_save_df", action='store_true', help="Do not save the resulting data frame")

    args = parser.parse_args()
    return args

class RunningLog():
    def __init__(self):
        self.allRuns = all_runs.AllRuns()

        #move to config file
        self.output_dir = "data/"
        self.raw_json_output_dir = os.path.join(self.output_dir, "raw")

        self.all_runs_output_dir = os.path.join(self.output_dir, "processed")
        self.pickled_df_filename = "df.%s"
        self.pickled_structures_filename = "df_struct.%s"

        self.df_fname = os.path.join(self.all_runs_output_dir, self.pickled_df_filename)
        self.df_struct_fname = os.path.join(self.all_runs_output_dir, self.pickled_structures_filename)

    def load_all_runs(self):
        if os.path.isfile(self.df_fname%"pkl"):
            self.allRuns.load_all_runs(self.df_fname%"pkl")

        if os.path.isfile(self.df_struct_fname%"pkl"):
            self.allRuns.load_all_runs_structures(self.df_struct_fname%"pkl")

    def save_all_runs(self, ext="pkl"):
        utilities.make_dir(self.all_runs_output_dir)
        utilities.rm_file(self.df_fname%ext)
        utilities.rm_file(self.df_struct_fname%ext)
        if ext=="pkl":
            self.allRuns.save_all_runs(self.df_fname%ext)
            self.allRuns.save_all_runs_structures(self.df_struct_fname%ext)
        elif ext=="csv":
            self.allRuns.save_all_runs_as_csv(self.df_fname%ext)
            self.allRuns.save_all_runs_structures_as_csv(self.df_struct_fname%ext)

    def load_files_in_directory(self, directory):
        loaded_files = self.allRuns.load_files_in_dir(directory, verbose=False)
        return loaded_files

    def generate_empty_json(self):
        fname_template = os.path.join(constants.TO_LOAD_FOLDER,
                                    constants.JSON_TEMPLATE_OUTPUT_NAME)
        fname = fname_template%"" 
        i=1
        while os.path.isfile(fname):
            suffix = "_%d"%i
            fname = fname_template%suffix
            i += 1
            
        utilities.make_dir(constants.TO_LOAD_FOLDER)
        with open(fname, "w") as json_file:
            json_file.write(constants.EMPTY_JSON)

        print "Generated: %s"%fname

    def load_files_to_load(self):
        directory = constants.TO_LOAD_FOLDER
        loaded_runs = self.load_files_in_directory(directory)

        utilities.make_dir(self.raw_json_output_dir)
        #for (fname, date) in loaded_files:
        for srun in loaded_runs:
            output_dir = os.path.join(self.raw_json_output_dir, str(srun.date.year))
            utilities.make_dir(output_dir)
            output_fname = str(srun.date.month) + ".json"
            oname = os.path.join(output_dir, output_fname)

            #append if exists
            if os.path.isfile(oname):
                #jsonFile = open(fname, 'r').read()
                #jsonFile = reader.read_file(fname)
                jsonFile = srun.orig_json_string
                outputJsonFile = reader.read_file(oname)
                outputJsonFileList = outputJsonFile[constants.blockNames.FileParams.list]
                if jsonFile in outputJsonFileList:
                    print "Json has already been inserted!"
                else:
                    outputJsonFileList.append(jsonFile)
                    #Better write and if correct, replace
                    with open(oname, "w") as json_file:
                        json_file.write(json.dumps(outputJsonFile, indent=4, separators=(',', ' : ')))
            #create if doesn't
            else:
                #jsonFile = reader.read_file(fname)
                jsonFile = srun.orig_json_string
                newdict = {}
                newdict[constants.blockNames.FileParams.list] = [jsonFile]
                with open(oname, "w") as json_file:
                    json_file.write(json.dumps(newdict, indent=4, separators=(',', ' : ')))
                print "Wrote new file:", oname


def main():
    args = parseArgs()

    rl = RunningLog()

    if args.template:
        print "Generating template\n"
        rl.generate_empty_json()

    if args.load_df:
        rl.load_all_runs()

    if args.load_json==[]:
        print "Loading files to load\n"
        rl.load_files_to_load()
    elif type(args.load_json) == list:
        for directory in args.load:
            print "Loading files in ", directory
            rl.load_files_in_directory(directory)
        print ""

    if args.load_df == True and args.dont_save_df != True:
        print "Saving all runs"
        rl.save_all_runs("pkl")
        rl.save_all_runs("csv")


if __name__ == "__main__":
    main()
