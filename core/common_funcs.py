#####################################################
# Functions used in analysis of stability data taken
# for the ftb run in Dumber 2014. 
#
# Author: Ed Leming
# Date:   20/01/2015
#####################################################
import rat
import ROOT
import numpy as np
#from utils import DataQualityProc as dqp

def create_root_file(fname, option='RECREATE', title='ROOT file'):
    """Create new ROOT file capable of storing any kind of ROOT object. This file becomes the current directory.

    :param fname: Name of file for saving to disc. 
    :param option: Options for creation of file. Defaults to 'RECREATE'.
    :param file_title: Title of file. Defaults to 'ROOT file' 
    :return: root file object.  
     """
    hfile = ROOT.gROOT.FindObject( fname )
    if hfile:
        hfile.Close()
    ROOT.gBenchmark.Start( fname )
    return ROOT.TFile( fname, option, title )

def get_PMT_hits(fname, flag=5241):
    """Find how many times each PMT was hit during a run.

    :param file_name: Name of a .root data file containing the run data
    :return pmt_hits: Dictionary containing number of hits at PMTs activated during run
    """
    pmt_hits = {}
    for ds, run in rat.dsreader(fname):
        for iEV in range(ds.GetEVCount()):
            ev = ds.GetEV(iEV)
            if (ev.GetTrigType() != 32768):
                continue
            unCal_pmts = ev.GetUncalPMTs()
            for pmt in range(unCal_pmts.GetCount()):
                uncal = unCal_pmts.GetPMT(pmt)
                lcn = uncal.GetID()
                if lcn != flag:
                    if lcn not in pmt_hits:
                        pmt_hits[lcn] = 1.
                    else:
                        pmt_hits[lcn] += 1.
    return pmt_hits

def plot_total_nHit(fname):
    """ Plot the number of Calibrated hits per event.     
                                                   
    :param fname: Path to the RAT DS file to plot.                                                     
    :return: The histogram plot                         
    """
    h_cal_hits = ROOT.TH1D( "hCalHits", "Number of Calibrated hits per event", 2000, 0.0, 2000.0 )
    h_cal_hits.SetDirectory(0)
    for ds, run in rat.dsreader(fname):
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)
            h_cal_hits.Fill(ev.GetCalPMTs().GetAllCount())
    h_cal_hits.GetYaxis().SetTitle( "Count per 1 Calibrated hit bin" )
    h_cal_hits.GetXaxis().SetTitle( "Number of Calibrated hits per event" )
    h_cal_hits.Draw()
    return h_cal_hits

def two_axis_plot(p1, p2, save_path):
    """Plot two TGraphs on a single plot with two axes

    :param p1: TGraph object for plotting
    :param p2: TGraph object for plotting
    :param save_path: Path used to print plot as PDF 
    :return canvas: Canvas containing 2D plot
    """
    c2 = ROOT.TCanvas("c2", "c2",0,  0, 800, 600);
    pad1 = ROOT.TPad("pad1","",0,0,1,1);
    pad2 = ROOT.TPad("pad2","",0,0,1,1);
    pad2.SetFillStyle(4000);
    #Makes pad2 transparent                                                                                
    pad2.SetFrameFillStyle(0);
    pad1.Draw()
    pad1.cd()
    
    #mp = ROOT.TMultiGraph()
    #mp.SetTitle("TELLIE stability as a function of time")

    #Set-up p1
    p2.SetMarkerStyle(22)
    p2.SetMarkerColor(ROOT.kRed+2)
    p2.GetYaxis().SetTitleColor(ROOT.kRed+2)
    p2.GetYaxis().SetAxisColor(ROOT.kRed+2)
    p2.GetYaxis().SetLabelColor(ROOT.kRed+2)
    p2.Draw("APY+")
    #mp.Add(p1, "APY+")
    pad1.Update()

    pad2.Draw()
    pad2.cd()
    #mp.Add(p2, "AP")
    p1.Draw("AP")
    pad2.Update()

    c2.Print(save_path)

def plot_correlations(p1, p2): 
    """Plot correlations of y parameters from two passed plots

    :param p1: TGraph object
    :param p2: TGraph object
    :returns corr_plot: A TGraph object of parameter correlations
    """
    param1 = p1.GetY()
    param2 = p2.GetY()
    err1 = p1.GetEY() 
    err2 = p2.GetEY()

    #corr_graph = ROOT.TGraphErrors(p1.GetN(), param1, param2, np.zeros(p1.GetN()), np.zeros(p2.GetN()) )
    corr_graph = ROOT.TGraphErrors(p1.GetN(), param1, param2, err1, err2)
    corr_graph.SetTitle("Correlation plot of %s against %s" % (p1.GetYAxis().GetTitle(), p2.GetYAxis.GetTitle()) )
    tits_1 = p1.GetYaxis().GetTitle()
    tits_2 = p2.GetYaxis().GetTitle()
    corr_graph.GetXaxis().SetTitle(tits_1)
    corr_graph.GetYaxis().SetTitle(tits_2)
    corr_graph.GetXaxis().SetTitleOffset(1.2)
    corr_graph.GetYaxis().SetTitleOffset(1.2)
    corr_graph.SetMarkerStyle(33)
    return corr_graph
