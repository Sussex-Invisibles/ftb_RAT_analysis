import rat
import ROOT
import numpy as np
import utils.DataQualityProc as dqp
import utils.calc as calc
import core.time_angle_funcs as taf
import core.common_funcs as cf
import os

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

    # Results and data paths
    results_path = "/epp/scratch/neutrino/el230/ftbAnalysis/reflections/"
    data_path = "/epp/scratch/neutrino/el230/rat_data_scripts/reflections/"

    # Make canvas and TFile
    cT = ROOT.TCanvas("cT","c",600,400);

    # Load rat defualts for fibre pos stuff
    ROOT.RAT.DB.Get().LoadDefaults()
    ROOT.RAT.DB.Get().Load("pmt/airfill2.ratdb")
    ROOT.RAT.DB.Get().Load("geo/snoplus.geo")
    ROOT.RAT.DU.Utility.Get().BeginOfRun()

    # Run analysis for each fibre
    fibre = "FT028A"
    # Results root file
    r = cf.create_root_file("./test/results/time_test.root")

    # Load fibre pos now to aviod doing it mutiple times in loops
    fibre_pos = ROOT.RAT.DB.Get().GetLink("FIBRE", fibre)

    data_file = "%s%s/0.root" % (data_path, fibre)
    print data_file
    time_plots_path = check_dir("%stime_angle_plots/" % results_path)
    
    time_hist, single_hist = taf.plot_hit_times(data_file, fibre)
    time_hist.Write()
    single_hist.Write()
    time_hist.Draw("")
    cT.Update()
