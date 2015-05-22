##########################################################
# Script to read root files created by time_angle_analysis
# and generate plots of the temporal spread of PMT hits as 
# a function of angle from the central beam spot.
#
# Author: Ed Leming
# Date:   11/02/2015
##########################################################
import rat
import ROOT
import sys
import os
import time
import numpy as np
from core import time_angle_funcs as taf
from core import stability_funcs as sf
from AcquireTek import root_utils as rootu
from AcquireTek import calc_utils as calc

def convert_hists_to_xy(hists):
    ''' Convert root histogram into an x, y array.'''
    pmtIDs = identify_interesting_pmts(hists)
    n = hists[pmtIDs[0]].GetNbinsX()
    x, y = np.zeros(n), np.zeros((len(pmtIDs),n))
    for i, pmtID in enumerate(pmtIDs):
        for it, ent in enumerate(x):
            if it > 0 and it < len(pmtIDs): #Don't get underflow bin
                y[i, it] = hists[pmtID].GetBinContent(it)
                if i == 0: # Only need to do this once
                    x[it] = hists[pmtID].GetBinLowEdge(it)
    return x, y

def pulse_shape_calcs(hists, rootfile, savePath, c):
    ''' Run pulse shape calculations on each PMT pulse

    :param hists: Directory containing time spectra histograms of all pmts within
                  defined light cone. 
    :param savePath: Path to save directory
    '''
    x,y = convert_hists_to_xy(hists)

    riseHist, rise, riseErr = rootu.plot_rise(x,y,'Rise_time', scale=1.)
    riseHist.Write()
    rootu.print_hist(riseHist, "%s/rise_time.pdf" % savePath, c)
    time.sleep(5)

    fallHist, fall, fallErr = rootu.plot_fall(x,y,'Fall_time', scale=1.)
    fallHist.Write()
    rootu.print_hist(fallHist, "%s/fall_time.pdf" % savePath, c)
    time.sleep(5)

    widthHist, width, widthErr = rootu.plot_width(x,y,'Width', scale=1.)
    widthHist.Write()
    rootu.print_hist(widthHist, "%s/width.pdf" % savePath, c)
    time.sleep(5)

def identify_interesting_pmts(hists):
    ''' Find PMT spectra with significant hits in interesting range '''
    pmtIDs = hists.keys()
    interesting = []
    for pmtID in pmtIDs:
         peak_bin = hists[pmtID].GetMaximumBin()
         peak_pos = hists[pmtID].GetBinCenter(peak_bin)
         peak_counts = hists[pmtID].GetBinContent(peak_bin)
         if peak_pos > -200 and peak_pos < 150 and peak_counts > 100:
             interesting.append(pmtID)
    return interesting

def plot_interesting_pmts(hists, graphs, rootFile, savePath, can): 
    ''' Plot 'clean' time spectra from within direct cone.
    
    :param hist: Dictionary containing time spectra histograms of all pmts within
                 defined light cone.
    '''
    pmtIDs = identify_interesting_pmts(hists)
    s = ROOT.THStack("stack", "Stacked PMT responses from direct cone")
    for pmtID in pmtIDs:
        hists[pmtID].Draw("")
        hists[pmtID].GetXaxis().SetTitle("Time (ns)")
        s.Add(hists[pmtID])
        c1.Update()
        c1.Modified()
        c1.Print("%s/pmt_%d.png" % (savePath, pmtID))
        graphs[pmtID].Draw("ap")
        graphs[pmtID].GetXaxis().SetTitle("Time (50MHz)")
        graphs[pmtID].GetYaxis().SetTitle("PMT Hit time (ns)")
        graphs[pmtID].SetMarkerStyle(1)
        c1.Update()
        c1.Modified()
        c1.Print("%s/pmt_%d_ordered.png" % (savePath, pmtID))
    hist_sum = s.GetStack().Last()
    hist_sum.SetTitle("Summed PMT responses from direct cone")
    hist_sum.GetXaxis().SetTitle("Time (ns)")
    hist_sum.Draw()
    hist_sum.Write()
    rootu.print_hist(hist_sum, "%s/Summed_response.png" % savePath, can)
    can.SetLogy()
    rootu.print_hist(hist_sum, "%s/Summed_response_logy.png" % savePath, can)
    can.SetLogy(0)
    s.Delete()    

def plot_slices(hists, slice_width, fibre_pos):
    """ Plot individual pmt time spectra within angular slices. 

    :param hist: Dictionary containing time spectra histograms of all pmts within 
                 defined light cone. Keys are pmtID ints.
    :param slice_width: Angular with of slices of interest. 
    """
    pmt_info = rat.utility().GetPMTInfo()
    # Find max angle
    max_angle = 0
    pmtIDs = hists.keys()
    for pmtID in pmtIDs:
        angle = taf.fibre_to_pmt_angle(fibre_pos, pmt_info.GetPosition(pmtID))
        if angle > max_angle:
            max_angle = angle
    print max_angle

    # Step between 0 and max_angle in slices of slice_width
    # create a plot of all pmt time spectra within each slice
    ROOT.gStyle.SetPalette(1) 
    cuts = np.arange(0., max_angle+slice_width, slice_width)
    for i, cut in enumerate(cuts): 
        tmpHists = []
        if i > 0:
            low_range = cuts[i-1]
            hi_range = cuts[i]
            s = ROOT.THStack("stack", "Slice: %1.1f - %1.1f deg" % (low_range, hi_range))            
            count = 0
            for pmtID in pmtIDs:
                angle = taf.fibre_to_pmt_angle(fibre_pos, pmt_info.GetPosition(pmtID))
                if angle > low_range and angle < hi_range:
                    #print pmtID
                    count = count + 1
                    hists[pmtID].SetLineColor(count)
                    s.Add(hists[pmtID])
            print "Drawing..."
            s.Draw("nostack")
            s.GetHistogram().GetXaxis().SetTitle("Time (ns)")
            #s.Write()
            #c1.BuildLegend(0.5, 0.2, 0.88, 0.88)
            c1.Update()
            c1.Modified()
            c1.Print("./results/slices/Slice_%1.1f.png" % low_range)
            s.Delete()
            #time.sleep(1)

    
if __name__ == "__main__":

    # Reset all root stuff
    ROOT.gROOT.Reset()
    
    # Make canvas and TFile
    c1 = ROOT.TCanvas("c1","c1",600,400);

    # Set optstat
    #ROOT.gStyle.SetOptStat(0)

    # Open file and read
    fibre = "FT044A"
    dataPath = "./results/reflections/"
    fname = "%s%s_pmts.root" % (dataPath, fibre)

    # Create root file. 
    #r = sf.create_root_file("./results/slices_%s.root" % (fibre))

    # Load rat defualts for fibre pos stuff
    ROOT.RAT.DB.Get().LoadDefaults()
    ROOT.RAT.DB.Get().Load("pmt/airfill2.ratdb")
    ROOT.RAT.DB.Get().Load("geo/snoplus.geo")
    ROOT.RAT.DU.Utility.Get().BeginOfRun()
    
    fibre_pos = ROOT.RAT.DB.Get().GetLink("FIBRE", fibre)
    pmt_info = rat.utility().GetPMTInfo()

    f = ROOT.TFile(fname); 
    hists, graphs = {}, {}
    for key in f.GetListOfKeys():
        pmt_no = int(''.join(x for x in key.GetName() if x.isdigit()))
        if len(key.GetName().split("_")) == 2:
            hists[pmt_no] = f.Get(key.GetName())
            graph_name = "%s_ordered" % key.GetName()
            print key.GetName(), graph_name
            graphs[pmt_no] = f.Get(graph_name)
    #plot_slices(hists, 1., fibre_pos)    

    savePath = "./results/pmt_plots/%s/" % fibre        
    r1 = sf.create_root_file("%s/pmts.root" % (savePath))
    plot_interesting_pmts(hists, graphs, r1, savePath, c1)

    #x,y = convert_hists_to_xy(hists)
    #calc.plot_eg_pulses(x,y,10, scale=1, show=True)

    #savePath = "./results/pmt_plots/%s/analysis/" % fibre
    #r2 = sf.create_root_file("%s/results.root" % (savePath))
    #pulse_shape_calcs(hists, r2, savePath, c1)
