####################################################
# Does what is says... Used to test functions in
# core/stability_funcs before they get included in 
# main analysis scripts
#
# Author: Ed Leming
# Date:   03/02/2015
####################################################

from core import stability_funcs as sf
import ROOT
import rat
import sys
import time
import numpy as np

if __name__ == "__main__":
    
    # Reset all roor stuff                                                                                                            
    ROOT.gROOT.Reset()

    #runDict = { 8843 : "1000Hz",
    #            8991 : "500Hz",
    #            9088 : "100Hz",
    #            9091 : "10Hz",
    #            9093 : "10Hz" }
    runDict = { 8843 : "1000Hz" }
    fibre = "FT044A"

    # Results and data paths 
    results_path = "/epp/scratch/neutrino/el230/ftbAnalysis/stability/"
    data_path = "/epp/scratch/neutrino/el230/rat_data_scripts/stability/"
    data_path = "/epp/scratch/neutrino/el230/rat_data_scripts/reflections/"
    # Make canvas and TFile 
    cT = ROOT.TCanvas("cT","cT",600,400);

    count = 0
    for run in runDict:
    
        r = sf.create_root_file("testStuff.root")
        # File stuff 
        data_dir = "%s%s/" % (data_path, runDict[run])
        data_file = "%sR%s*.root" % (data_dir, run)
        #
        data_file = "%s%s/*.root" % (data_path, fibre)

        pmts  = sf.get_PMT_hits(data_file)
        h,p = [],[]
        for pmt, hits in pmts.iteritems():
            p.append(pmt)
            h.append(hits)
            print pmt, hits
            
        print ""
        print h.index(max(h)), max(h)
        sh = np.argsort(h)
        print sh[1], p[sh[1]], h[sh[1]]
        print sh[-1], p[sh[-1]], h[sh[-1]]
        #event_graph_init, time_graph_init = sf.plot_turn_on(data_file, 2000)
        #event_graph_init.Write("Event_%s_%s" % (runDict[run], run))
        #time_graph_init.Write("Time_%s_%s" % (runDict[run], run))
