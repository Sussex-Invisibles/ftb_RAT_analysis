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
        run = 8911
        data_file = "%s%s/0.root" % (data_path, fibre)
        print data_file
        save_path = check_dir("%s/dark_count_plots/" % results_path)

	count = 0
        r = sf.create_root_file("%s%s.root" % (save_path, fibre))
			
        # Analysis begins
        # Create hit projections
        pmt_hits = sf.get_PMT_hits(data_file)
        tmp_title = "Total nHits: Fibre %s, Run %i" % (fibre, run)
        hitHist = psup_map.proj_pmts(pmt_hits, tmp_title)
        hitHist.Draw("colz")
        ROOT.gStyle.SetOptStat(0);
        c1.Update()
        c1.SetLogz()
        c1.Print("%s%s_%s.pdf" % (save_path, run, fibre))
        hitHist.Write()
        # Plot hits in direct cone                                                                                                                                           
        pmt_hits = sf.get_PMT_hits_cone(data_file, fibre_pos, 25.)
        tmp_title = "Cone nHits projected from Fibre %s: Run %s" % (fibre, run)
        hitHist = psup_map.proj_pmts(pmt_hits, tmp_title)
        hitHist.Draw("colz")
        ROOT.gStyle.SetOptStat(0);
        c1.SetLogz()
        c1.Update()
        c1.Print("%s%s_%s_direct.pdf" % (save_path, run, fibre))
        
        # Stability in direct cone
        mean_hit_graph, rms_graph, avg, stdev  = sf.track_mean_nHits_cone(data_file, 500, fibre_pos, 25.)
        mean_hit_graph.SetTitle("Cone nHit as a function of time: Fibre = %s, run = %i" % (fibre, run))
        mean_hit_graph.Draw("AP")
        mean_hit_graph.Write( "nHitVsTime" )
        c1.Update()
        c1.Print("%sDirect_nHitVsTime_%s.pdf" % (save_path, run))
        
        rms_graph.SetTitle("Cone RMS as a function of time: Freq = %s, run = %i" % (fibre, run))
        rms_graph.Draw("AP")
        rms_graph.Write( "RMSVsTime" )
        c1.Update()
        c1.Print("%sDirect_RMSVsTime_%s.pdf" % (save_path, run))
                

