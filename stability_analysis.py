##################################################
# Master file to run stability analysis on Dec 
# 2014 ftb data sets.
# 
# Author: Ed Leming
# Date:   20/01/2014
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
   # runDict = { 8991 : "500Hz" }

    # Results and data paths
    results_path = "/epp/scratch/neutrino/el230/ftbAnalysis/stability/"
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
    fibre = "FT035A"

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
        print data_file
        time_plots_path = check_dir("%s/time_plots/" % results_path)
	hits_path = check_dir("%s/hits_plots/" % results_path)

        # Analysis begins
        #init_nHit, init_nHit_error, init_nHit_hist = sf.get_init_nHit(data_file, 100)
        #init_nHit_hist.Draw("")
        #init_nHit_hist.Write()
        #c1.Update()

        #nHit_hist = sf.plot_total_nHit(file_name)
        #nHit_hist.Draw("")
        #nHit_hist.Write()
        #c1.Update()
	
	# Check initial hits
	event_graph_init, time_graph_init = sf.plot_turn_on(data_file, 2000)
        event_graph_init.Write("Event_%s_%s" % (runDict[run], run))
	event_graph_init.Draw("AP")
	c1.Update()
	c1.Print("%sinitnHitVsEvent_%s_%s.pdf" % (time_plots_path, run, runDict[run]))
        time_graph_init.Write("Time_%s_%s" % (runDict[run], run))
	time_graph_init.Draw("AP")
	c1.Update()
	c1.Print("%sinitnHitVsTime_%s_%s.pdf" % (time_plots_path, run, runDict[run]))

	# Create hit projections
	pmt_hits = sf.get_PMT_hits(data_file)
	tmp_title = "NHits for Fibre FT035A - run %s" % (run)
        hitHist = psup_map.proj_pmts(pmt_hits, tmp_title)
        hitHist.Draw("colz")
        ROOT.gStyle.SetOptStat(0);
        c1.Update()
	c1.SetLogz()
        c1.Print("%s%s_%s.pdf" % (hits_path, run, runDict[run]))
        hitHist.Write()

	mean_hit_graph, rms_graph, avg, stdev  = sf.track_mean_nHits(data_file, 500)
	mean_hit_graph.SetTitle("Mean nHit as a function of time: Freq = %s, run = %i" % (runDict[run], run))
	mean_hit_graph.GetYaxis().SetRangeUser(55., 85.)
        mean_hit_graph.Draw("AP")
        mean_hit_graph.Write( "nHitVsTime" )
        c1.Update()
        c1.Print("%snHitVsTime_%s.pdf" % (time_plots_path, run))

	rms_graph.SetTitle("RMS spread on nHit as a function of time: Freq = %s, run = %i" % (runDict[run], run))
	rms_graph.GetYaxis().SetRangeUser(10., 20.)
        rms_graph.Draw("AP")
        rms_graph.Write( "RMSVsTime" )
        c1.Update()
        c1.Print("%sRMSVsTime_%s.pdf" % (time_plots_path, run))

        if run == 8991: # only this run has a reasonable number of PIN readings
            db = dba.get_tellie_cauch_db()
            shots = dba.get_cauch_number_of_shots(db, run)
            rate = dba.get_cauch_pulse_rate(db, run)
            pin = dba.get_cauch_PIN_reading(db, run)

            mean_graph, rms_graph, avg, stdev  = sf.track_mean_nHits(data_file, shots[0])
	    n_points = mean_graph.GetN()
            x_buff = mean_graph.GetX()
	    x_buff.SetSize( n_points ) # Gotta do this as GetX() returns a buffer object
	    x = np.array(x_buff, copy=True)

	    PIN_graph = ROOT.TGraphErrors(n_points, x, pin, np.zeros(n_points), np.zeros(n_points))
            PIN_graph.SetTitle("Change in PIN reading as a function of events")
            PIN_graph.GetXaxis().SetTitle(mean_graph.GetXaxis().GetTitle())
            PIN_graph.GetXaxis().SetTitleOffset(1.2)
            PIN_graph.GetYaxis().SetTitle("PIN reading (16 bit)")
            PIN_graph.GetYaxis().SetTitleOffset(1.35)
            PIN_graph.SetMarkerStyle(33)
            PIN_graph.Write( "PINVsTime_%s_%s" % (run, runDict[run]) )
            PIN_check_path = check_dir("%sPIN_plots/" % results_path)
	    sf.two_axis_plot(mean_graph, PIN_graph, "NHit and PIN readings as a function of time", "%sPINVsTime_%s_%s.pdf" % (PIN_check_path, run, runDict[run]) )

	    #print PIN_graph.GetYaxis().GetTitle()
	    #print time_graph.GetYaxis().GetTitle()
            corr_graph = sf.plot_correlations(PIN_graph, mean_graph)
            corr_graph.Write( "PINVsnHit_CORR__%s_%s" % (run, runDict[run]) )
            corr_graph.Draw("AP")
	    PIN_buff = PIN_graph.GetY()
	    PIN_buff.SetSize(PIN_graph.GetN())
	    PIN = np.array(PIN_buff, copy=True)
	    nHit_buff = mean_graph.GetY()
	    nHit_buff.SetSize(n_points)
	    nHit = np.array(nHit_buff, copy=True)
            t  = ROOT.TLatex(0.13, 0.85, "r = %1.3f" % ( sf.calc_corr_coef(nHit, PIN)) )
	    t.SetNDC(True)
            t.Draw()
	    c1.Print("%sCORRELATION_%s_%s.pdf" % (PIN_check_path, run, runDict[run]) )
