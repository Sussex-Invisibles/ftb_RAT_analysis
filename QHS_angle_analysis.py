##################################################
# Master script to run time_vs_angle analysis on
# Dec 2014 ftb data.
#
# Author: Ed Leming
# Date:   11/02/2015
##################################################
import rat
import ROOT
from core import stability_funcs as sf
from utils import db_access as dba
from utils import psup_map
import time
import sys
import os
import numpy as np

def read_fibre_runNo_file(fname):
        """Reads in 2D text file of FibreName\tRunNumber

        param: fname: Path to file to be read
        retun: dict of Fibre name and associated run number.
        """
        runDict = {}
        os.system("dos2unix %s" % fname) # Incase of any funny text characters
        with open(fname,'rU') as f:      # U for universal unpacking mode
                reader = csv.reader(f, delimiter="\t")
                for fibre, runNo in reader:
                        runDict[fibre] = int(runNo)
        return runDict

def check_dir(dname):
        """Check if directory exists, create it if it doesn't

        :param dname: Path to directory to be checked
        :retrun dname as passed.
        """
        direc = os.path.dirname(dname)
        try:
                os.stat(direc)
        except:
                os.mkdir(direc)
                print "Made directory %s...." % dname
        return dname

if __name__ == "__main__":

    # Reset all root stuff
    ROOT.gROOT.Reset()

    # Get dictionary containing all fibres and respective run numbers
    reflc_txt_path = "/home/el230/SNO+/rat_data_scripts/submission/input_files/reflections.txt"
    runDict = read_fibre_runNo_file(reflc_txt_path)

    # Results and data paths
    results_path = "/epp/scratch/neutrino/el230/ftbAnalysis/reflections/"
    data_path = "/epp/scratch/neutrino/el230/rat_data_scripts/reflections/"

    # Make canvas and TFile
    c1 = ROOT.TCanvas("c1","c1",600,400);

    # Run analysis for each fibre
    for fibre in runDict:
        r = sf.create_root_file("%s%s.root" % (results_path, runDict[run]), option = "UPDATE")

        # File stuff
        data_file = "%s%s_%s*.root" % (data_path, fibre, runDict[fibre])
        print data_file
        time_plots_path = check_dir("%s/time_plots/" % results_path)
        hits_path = check_dir("%s/hits_plots/" % results_path)
