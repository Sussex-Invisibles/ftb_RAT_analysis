##################################################
# Master script to run time_vs_angle analysis on
# Dec 2014 ftb data.
#
# Author: Ed Leming
# Date:   11/02/2015
##################################################
import rat
import ROOT
import core.time_angle_funcs as taf
import core.common_funcs as cf
import utils.db_access as dba
import utils.psup_map as pmap
import time
import sys
import os
import numpy as np
import csv

def check_n_subruns(fibre, direc):
    c = 0
    for i in range(20):
        fname = "%s%s/%i.root" % (direc, fibre, i)
        if os.path.isfile(fname):
            c = c + 1
    return c

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
    #unDict = {'FT044A': 8909}
    #runDict = {'FT072A': 8964}
    #print runDict 
    #raise

    # Results and data paths
    results_path = "/epp/scratch/neutrino/el230/ftbAnalysis/reflections/"
    data_path = "/epp/scratch/neutrino/el230/rat_data_scripts/reflections/"

    # Make canvas and TFile
    c1 = ROOT.TCanvas("c1","c1",600,400);

    # Load rat defualts for fibre pos stuff
    ROOT.RAT.DB.Get().LoadDefaults()
    ROOT.RAT.DB.Get().Load("pmt/airfill2.ratdb")
    ROOT.RAT.DB.Get().Load("geo/snoplus.geo")
    ROOT.RAT.DU.Utility.Get().BeginOfRun()

    # Run analysis for each fibre
    for fibre in runDict:
	    # Results root file
	    r = cf.create_root_file("%s%s_timeAngle.root" % (results_path, fibre))
	    
	    # Load fibre pos now to aviod doing it mutiple times in loops
	    fibre_pos = ROOT.RAT.DB.Get().GetLink("FIBRE", fibre)
	    
	    # File stuff
	    #for i in range(check_n_subruns(fibre, data_path)):
            #data_file = "%s%s/0.root" % (data_path, fibre)
            data_file = "%s%s/*.root" % (data_path, fibre)
	    print data_file
	    time_plots_path = check_dir("%stime_angle_plots/" % results_path)
	    
	    time_hist, time_angle, time_QHS = taf.plot_time_vs_angle_QHS(data_file, fibre_pos, fibre)
	    ROOT.gStyle.SetOptStat(0)
            time_hist.Write()
            time_hist.Draw("")
            c1.Update()
            c1.Print("%s%s_time.png" % (time_plots_path, fibre))
            time_angle.Write()
            time_QHS.Write()
	    time_angle.Draw("colz")
            c1.SetLogz()
	    c1.Update()
            c1.Print("%s%s_angle.png" % (time_plots_path, fibre))
            time_QHS.Draw("colz")
            c1.Update()
            c1.Print("%s%s_QHS.png" % (time_plots_path, fibre))
