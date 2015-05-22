####################################################
# Does what is says... Used to test functions in
# core/stability_funcs before they get included in 
# main analysis scripts
#
# Author: Ed Leming
# Date:   03/02/2015
####################################################

from core import stability_funcs as sf
from utils import DataQualityProc as dqp
import ROOT
import rat
import sys
import time
import numpy as np

def plot_ticks_vs_events(fname):
    c, start_clock = 0, 0
    time, x, y, y_error = np.array([]), np.array([]), np.array([]), np.array([])
    for ds, run in rat.dsreader(fname):
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)
            if dqp.check_trig_type(ev.GetTrigType()) and ev.GetClockCount50() != 0:
                c = c + 1
                time = np.hstack( (time, [ev.GetClockCount50()]) )
                x = np.hstack( (x, [c]) )
    # Sort stuff
    order = np.argsort(time)
    time_sort = np.array(time)[order]
    x_sort = np.array(x)[order]
    graph = ROOT.TGraph(len(x), x, time)
    graph.SetTitle("Clock tick as a function of event number")
    graph.GetXaxis().SetTitle("Event number")
    graph.GetXaxis().SetTitleOffset(1.2)
    graph.GetYaxis().SetTitle("50MHz clock tick")
    graph.GetYaxis().SetTitleOffset(1.2)
    graph.SetMarkerStyle(33)
    graph = ROOT.TGraph(len(x), x, time_sort)
    sort_graph.SetTitle("Clock tick as a function of event number - SORTED")
    sort_graph.GetXaxis().SetTitle("Event number")
    sort_graph.GetXaxis().SetTitleOffset(1.2)
    sort_graph.GetYaxis().SetTitle("50MHz clock tick")
    sort_graph.GetYaxis().SetTitleOffset(1.2)
    sort_graph.SetMarkerStyle(33)
    return graph, sort_graph

if __name__ == "__main__":
    
    # Reset all roor stuff                                            
    ROOT.gROOT.Reset()

    #runDict = { 8843 : "1000Hz",
    #            8991 : "500Hz",
    #            9088 : "100Hz",
    #            9091 : "10Hz",
    #            9093 : "10Hz" }
    runDict = { 9093 : "10Hz" }

    # Results and data paths 
    results_path = "/epp/scratch/neutrino/el230/ftbAnalysis/stability/"
    data_path = "/epp/scratch/neutrino/el230/rat_data_scripts/stability/"

    # Make canvas and TFile 
    cT = ROOT.TCanvas("cT","cT",600,400);

    count = 0
    for run in runDict:
    
        # File stuff 
        r = sf.create_root_file("/home/el230/SNO+/ftbAnalysis/stability/test/results/clock_ticks.root")
        data_dir = "%s%s/" % (data_path, runDict[run])
        data_file = "%sR%s*.root" % (data_dir, run)

        graph, sort_graph = plot_ticks_vs_events(data_file)
        graph.Draw("AP")
        graph.SetName("%s_%s" % (runDict[run], run))
        graph.Write()
        sort_graph.Draw("AP")
        sort_graph.SerName("%s_%s_SORTED" % (runDict[run], run))
        sort_graph.Write()
        cT.Update()
        save_str = "/home/el230/SNO+/ftbAnalysis/stability/test/results/clock/R%s_%s.pdf" % (run, runDict[run]) 
        cT.Print(save_str)
        
