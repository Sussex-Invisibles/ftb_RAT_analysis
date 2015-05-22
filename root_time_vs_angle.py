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

def get_y_slice(hist2D, binx):
    Nbins = Time_angle.GetNbinsY()
    binWidth = hist2D.GetYaxis().GetBinWidth(0)
    firstBin = hist2D.GetYaxis().GetBinUpEdge(0)
    lastBin = hist2D.GetYaxis().GetBinUpEdge(Nbins)
    hist = ROOT.TH1D("Slice_%1.1fdeg" % (binx*binWidth), "Slice_%1.1fdeg" % (binx*binWidth), Nbins, firstBin, lastBin )

    bin_array = np.arange(firstBin, lastBin, binWidth)
    #print bin_array
    #print Nbins, firstBin, lastBin
    for i in range(Nbins): 
        hist.SetBinContent(i, hist2D.GetBinContent(binx, i))
    return hist

def fit_landau(hist):
    lan_fit = ROOT.TF1("Lan_fit", "[0]*TMath::Landau(x, [1], [2])", -100, -20)
    lan_fit.SetParameters(hist.GetMaximum(),-50, 10)
    lan_fit.SetLineColor(2)
    hist.Fit(lan_fit, "RQ")
    pars_buff =  lan_fit.GetParameters()
    pars_err_buff = lan_fit.GetParErrors()
    pars_buff.SetSize(3); pars_err_buff.SetSize(3)
    
    return np.array(pars_buff,copy=True), np.array(pars_err_buff,copy=True)

def plot_mpv(x, y, x_err, y_err, fibre):
    graph = ROOT.TGraphErrors(len(x), x.astype('float'), y.astype('float'), x_err.astype('float'), y_err.astype('float'))
    graph.SetTitle("MPV vs angle w.r.t fibre-to-pmt vector - %s" % fibre)
    graph.GetXaxis().SetTitle("Angle (deg)")
    graph.GetYaxis().SetTitle("MPV time (ns)")
    graph.SetMarkerStyle(33)
    return graph
    
if __name__ == "__main__":

    # Reset all root stuff
    ROOT.gROOT.Reset()
    
    # Make canvas and TFile
    c1 = ROOT.TCanvas("c1","c1",600,400);

    # Set optstat
    ROOT.gStyle.SetOptStat(0)

    # Open file and read
    fibre = "FT044A"
    dataPath = "/epp/scratch/neutrino/el230/ftbAnalysis/reflections/"
    fname = "%s%s_timeAngle.root" % (dataPath, fibre)

    f = ROOT.TFile(fname)
    Time_angle = f.Get("Time_angle")
    Time_angle.Draw("colz")
    c1.SetLogz()
    c1.Update()
    #time.sleep(1)

    NbinsX = Time_angle.GetNbinsX()
    NbinsY = Time_angle.GetNbinsY()

    #ROOT.gStyle.SetOptStat(1111)
    #stats = c1.GetPrimitive("stats")
    #stats.SetTextColor(1)

    noCuts = 20
    hists, x, fitRes, fitResErr = [], np.zeros(noCuts), np.zeros(shape=(noCuts,3)), np.zeros(shape=(noCuts,3))
    for i in range(noCuts):
        hists.append(get_y_slice(Time_angle, i))
        pars, par_errs = fit_landau(hists[i])
        fitRes[i] = pars
        fitResErr[i] = par_errs
        x[i] = i*Time_angle.GetYaxis().GetBinWidth(0)
        
        hists[i].Draw("")
        c1.Update()
        c1.Print("results/time_angle_slices/%s_%1.1fdeg.png" % (fibre, x[i]))
        time.sleep(0.1)

    mpv_plot = plot_mpv(x, fitRes[:,1], np.zeros(len(x)), fitResErr[:,1], fibre)
    mpv_plot.Draw("ap")
    c1.Update()
    c1.Print("results/time_angle_slices/%s_mvp.png" % (fibre))
    time.sleep(5)
    
