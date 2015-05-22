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
from utils import psup_map

if __name__ == "__main__":
    
    # Reset all roor stuff                                                                                                            
    ROOT.gROOT.Reset()

    #runDict = { 8843 : "1000Hz",
    #            8991 : "500Hz",
    #            9088 : "100Hz",
    #            9091 : "10Hz",
    #            9093 : "10Hz" }
    runDict = { 8843 : "1000Hz" }

    # Results and data paths 
    results_path = "/epp/scratch/neutrino/el230/ftbAnalysis/stability/"
    data_path = "/epp/scratch/neutrino/el230/rat_data_scripts/stability/"

    # Make canvas and TFile 
    ROOT.gStyle.SetOptStat(0);
    cT = ROOT.TCanvas("cT","cT",600,400);

    ROOT.RAT.DB.Get().LoadDefaults()
    ROOT.RAT.DB.Get().Load("pmt/airfill2.ratdb")
    ROOT.RAT.DB.Get().Load("geo/snoplus.geo")
    ROOT.RAT.DU.Utility.Get().BeginOfRun()

    count = 0
    for run in runDict:
    
        r = sf.create_root_file("testStuff.root")
        # File stuff 
        data_dir = "%s%s/" % (data_path, runDict[run])
        data_file = "%sR%s*.root" % (data_dir, run)


        seg = rat.utility().GetSegmentor()
        seg.Calculate()
        pmt_info = rat.utility().GetPMTInfo()
        print pmt_info.GetCount()
        for n in range(1,5):
            seg.SetNumberOfDivisions(n)
            segIDs = seg.GetSegmentIDs()
            pmt_hits = {}
            for i in range(int(segIDs.size())):
                pmt_hits[i] = (int(segIDs[i]) + 1)*1000
            hitHist = psup_map.proj_pmts(pmt_hits)
            hitHist.Draw("colz")
            cT.Update()
            cT.Print("./test/results/segmentor/Secs_%i.pdf" % n)
