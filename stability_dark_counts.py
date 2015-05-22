##################################################
# Script to test stability functions in 
# core.stability funcs. 
# 
# Author: Ed Leming
# Date:   25/02/15
##################################################
import rat
import ROOT
import core.stability_funcs as sf
import utils.db_access as dba
import utils.psup_map as psup_map
import time
import sys
import os
import numpy as np

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
    
	# Reset all roor stuff
	ROOT.gROOT.Reset()
	
	# Results and data paths
	results_path = "/home/el230/SNO+/ftbAnalysis/test/results/"
	data_path = "/epp/scratch/neutrino/el230/rat_data_scripts/reflections/"
	
	# Make canvas and TFile
	c1 = ROOT.TCanvas("c1","c1",600,400);
	
	# Load rat defualts for fibre pos stuff
	ROOT.RAT.DB.Get().LoadDefaults()
	ROOT.RAT.DB.Get().Load("pmt/airfill2.ratdb")
	ROOT.RAT.DB.Get().Load("geo/snoplus.geo")
	ROOT.RAT.DU.Utility.Get().BeginOfRun()
	fibre_pos = ROOT.RAT.DB.Get().GetLink("FIBRE", "FT035A")
        fibre_pos_reflec = ROOT.RAT.DB.Get().GetLink("FIBRE", "FT003A")
      
        # File stuff
        fibre = "FT055A"
        data_file = "%s%s/0.root" % (data_path, fibre)
        print data_file
        save_path = check_dir("%s/dark_count_plots/" % results_path)

	count = 0
        r = sf.create_root_file("%s%s.root" % (save_path, fibre))
			
        # Analysis begins
        # Plot hits in direct cone
        #pmt_hits = sf.get_PMT_hits_cone(data_file, fibre_pos, 20.)
        #hitHist = psup_map.proj_pmts(pmt_hits, fibre)
        #hitHist.Draw("colz")
        #ROOT.gStyle.SetOptStat(0);
        #c1.SetLogz()
        #c1.Update()
        #c1.Print("%s%s_cone.pdf" % (save_path, fibre))
        #hitHist.Write()
	
        # Plot hits in reflection cone
        #pmt_hits = sf.get_PMT_hits_cone(data_file, fibre_pos_reflec, 20.) 
        #hitHist = psup_map.proj_pmts(pmt_hits, runDict[run])
        #hitHist.Draw("colz")
        #ROOT.gStyle.SetOptStat(0);
        #c1.SetLogz()
        #c1.Update()
        #c1.Print("%s%s_%s_cone_reflec.pdf" % (hits_path, run, runDict[run]))

        # Stability in direct cone
        mean_hit_graph, rms_graph, avg, stdev  = sf.track_mean_nHits_cone(data_file, 600, fibre_pos, 20)
        mean_hit_graph.Draw("AP")
        mean_hit_graph.Write( "nHitVsTime" )
        #x_pos = time_graph.GetXaxis().GetBinUpEdge(10)
        #t = ROOT.TLatex(0.15, 0.85,"Mean = %1.2f +/- %1.2f" % (avg, stdev))
        #t.SetNDC(True)
        #t.Draw()
        c1.Update()
        c1.Print("%snHitVsTime_%s.pdf" % (save_path, fibre))

        rms_graph.Draw("AP")
        rms_graph.Write( "RMSVsTime" )
        c1.Update()
        c1.Print("%sRMSVsTime_%s.pdf" % (save_path, fibre))

        # Stability in reflection cone
        #stability_graph, time_graph, avg, stdev  = sf.track_mean_nHits_cone(data_file, 500, fibre_pos_reflec, 20)
        #time_graph.Draw("AP")
        #time_graph.Write( "nHitVsTime_%s_%s" % (run, runDict[run]) )
        #x_pos = time_graph.GetXaxis().GetBinUpEdge(10)
        #t = ROOT.TLatex(0.15, 0.85,"Mean = %1.2f +/- %1.2f" % (avg, stdev))
        #t.SetNDC(True)
        #t.Draw()
        #c1.Update()
        #c1.Print("%snHitVsTime_%s_%s_reflec.pdf" % (hits_path, run, runDict[run]))
