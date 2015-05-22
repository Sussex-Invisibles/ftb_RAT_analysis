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
	
	runDict = { 8843 : "1000Hz",
		    8991 : "500Hz",
		    9088 : "100Hz",
		    9091 : "10Hz",
		    9093 : "10Hz" }
	#runDict = { 8991 : "500Hz" }

	# Results and data paths
        results_path = check_dir("/epp/scratch/neutrino/el230/ftbAnalysis/stability/cones/")
	#results_path = "/home/el230/SNO+/ftbAnalysis/test/results/"
	data_path = "/epp/scratch/neutrino/el230/rat_data_scripts/stability/"
	
	# Make canvas and TFile
	c1 = ROOT.TCanvas("c1","c1",600,400);
	
	# Load rat defualts for fibre pos stuff
	ROOT.RAT.DB.Get().LoadDefaults()
	ROOT.RAT.DB.Get().Load("pmt/airfill2.ratdb")
	ROOT.RAT.DB.Get().Load("geo/snoplus.geo")
	ROOT.RAT.DU.Utility.Get().BeginOfRun()
	fibre_pos = ROOT.RAT.DB.Get().GetLink("FIBRE", "FT035A")
        fibre_pos_reflec = ROOT.RAT.DB.Get().GetLink("FIBRE", "FT003A")

	count = 0
	for run in runDict:
		# Create or open ROOT file for results.
		if runDict.values().count(runDict[run]) == 1:
			r = sf.create_root_file("%s%s.root" % (results_path, runDict[run]))
		elif runDict.values().count(runDict[run]) != 1 and runDict.values().index(runDict[run]) == count:
			r = sf.create_root_file("%s%s.root" % (results_path, runDict[run]))
		else: 
			r = sf.create_root_file("%s%s.root" % (results_path, runDict[run]), option = "UPDATE")
			print "Updating file..."
	    
		# File stuff
		data_dir = "%s%s/" % (data_path, runDict[run])
		data_file = "%sR%s*.root" % (data_dir, run)
		#data_file = "%sR%s_0.root" % (data_dir, run)
		print data_file
		time_plots_path = check_dir("%s/time_plots/" % results_path)
		hits_path = check_dir("%s/cone_hits_plots/" % results_path)
			
                # Plot hits in direct cone
                pmt_hits = sf.get_PMT_hits_cone(data_file, fibre_pos, 25.) 
                tmp_tits = tmp_title = "NHits for Fibre FT035A direct cone - run %s" % (run)
                hitHist = psup_map.proj_pmts(pmt_hits, tmp_tits)
                hitHist.Draw("colz")
                ROOT.gStyle.SetOptStat(0);
                c1.SetLogz()
                c1.Update()
                c1.Print("%s%s_%s_direct.pdf" % (hits_path, run, runDict[run]))

                # Stability in direct cone
                mean_hit_graph, rms_graph, avg, stdev  = sf.track_mean_nHits_cone(data_file, 500, fibre_pos, 25.)
                mean_hit_graph.SetTitle("Cone nHit as a function of time: Freq = %s, run = %i" % (runDict[run], run))
                mean_hit_graph.Draw("AP")
                mean_hit_graph.Write( "nHitVsTime" )
                c1.Update()
                c1.Print("%sDirect_nHitVsTime_%s.pdf" % (time_plots_path, run))

                rms_graph.SetTitle("Cone RMS as a function of time: Freq = %s, run = %i" % (runDict[run], run))
                rms_graph.Draw("AP")
                rms_graph.Write( "RMSVsTime" )
                c1.Update()
                c1.Print("%sDirect_RMSVsTime_%s.pdf" % (time_plots_path, run))


                # Plot hits in reflected cone
                pmt_hits = sf.get_PMT_hits_cone(data_file, fibre_pos_reflec, 25.)
                tmp_tits = tmp_title = "NHits for Fibre FT035A reflected cone - run %s" % (run)
                hitHist = psup_map.proj_pmts(pmt_hits, tmp_tits)
                hitHist.Draw("colz")
                ROOT.gStyle.SetOptStat(0);
                c1.SetLogz()
                c1.Update()
                c1.Print("%s%s_%s_reflec.pdf" % (hits_path, run, runDict[run]))

                # Stability in reflected cone
                mean_hit_graph, rms_graph, avg, stdev  = sf.track_mean_nHits_cone(data_file, 500, fibre_pos_reflec, 25.)
                mean_hit_graph.SetTitle("Cone nHit as a function of time: Freq = %s, run = %i" % (runDict[run], run))
                mean_hit_graph.Draw("AP")
                mean_hit_graph.Write( "nHitVsTime" )
                c1.Update()
                c1.Print("%sReflected_nHitVsTime_%s.pdf" % (time_plots_path, run))

                rms_graph.SetTitle("Cone RMS as a function of time: Freq = %s, run = %i" % (runDict[run], run))
                rms_graph.Draw("AP")
                rms_graph.Write( "RMSVsTime" )
                c1.Update()
                c1.Print("%sReflected_RMSVsTime_%s.pdf" % (time_plots_path, run))
