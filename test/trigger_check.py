##################################################                                                      # Master file to run stability analysis on Dec
# 2014 data set
#
# Author: Ed Leming
# Date:   20/01/2014
##################################################                                                         
import rat
import ROOT
from core import stability_funcs as sf
import time
import sys

if __name__ == "__main__":

    # Reset all roor stuff
    ROOT.gROOT.Reset()

    # Make canvas and TFile
    c1 = ROOT.TCanvas("c1","c1",600,400);
    run = "100Hz"
    r = sf.create_root_file("results/%s_triggers.root" % run)

    # File stuff
    file_name = "/home/el230/SNO+/rat_data_scripts/stability/%s/*.root" % (run)
    print file_name

    # Analysis begins
    utils = rat.utility()
    #print utils.GetTrigBits().DumpNames()
    sys.exit()

    trig_hist= sf.plot_trigger_int(file_name)
    trig_hist.Draw("")
    trig_hist.Write()
    c1.Update()
    
    print rat.dureader(fname).TrigBits
    
