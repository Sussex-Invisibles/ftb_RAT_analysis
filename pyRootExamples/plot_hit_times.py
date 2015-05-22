#!/usr/bin/env python
#
# plot_mcphotoelectron_hit_times, plot_mchit_times, plot_calibrated_hit_times, plot_hit_times
#
# Hit times of the photoelectron, MCHit, uncalibrated and calibrated PMTs can be plotted. 
# Uncalibrated hit times are ADC counts and thus not easily compared.
#
# Author P G Jones - 2014-04-19 <p.g.jones@qmul.ac.uk> : New file.
####################################################################################################
import ROOT
import rat

def plot_mcphotoelectron_hit_times(file_name):
    """ Plot the MCPhotoeletron hit times in *file_name*
    
    :param file_name: Path to the RAT DS file to plot.
    :return: The created histogram
    """
    hit_times = ROOT.TH1D("hHitTimes", "Hit times of the of photoelectrons", 500, 0.0, 500.0)
    hit_times.SetDirectory(0)
    for ds, run in rat.dsreader(file_name):
        mc = ds.GetMC()
        for imcpmt in range(0, mc.GetMCPMTCount()):
            mcpmt = mc.GetMCPMT(imcpmt)
            for imcphotoelectron in range(0, mcpmt.GetMCPECount()):
                hit_times.Fill(mcpmt.GetMCPE(imcphotoelectron).GetCreationTime())
    
    hit_times.GetYaxis().SetTitle( "Count per 1 ns bin" )
    hit_times.GetXaxis().SetTitle( "Hit times [ns]" )
    hit_times.Draw()
    return hit_times

def plot_mchit_times(file_name):
    """ Plot the MCHit hit times in *file_name*
    
    :param file_name: Path to the RAT DS file to plot.
    :return: The created histogram
    """
    hit_times = ROOT.TH1D("hHitTimes", "Hit times of the MCHit per event", 500, 0.0, 500.0)
    hit_times.SetDirectory(0)
    for ds, run in rat.dsreader(file_name):
        for imcev in range(0, ds.GetMCEVCount()):
            mc_hits = ds.GetMCEV(imcev).GetMCHits()
            for imchit in range(0, mc_hits.GetAllCount()):
                hit_times.Fill(mc_hits.GetAllPMT(imchit).GetTime())

    hit_times.GetYaxis().SetTitle( "Count per 1 ns bin" )
    hit_times.GetXaxis().SetTitle( "Hit times [ns]" )
    hit_times.Draw()
    return hit_times

def plot_calibrated_hit_times(file_name):
    """ Plot the Calibrated PMT hit times in *file_name*
    
    :param file_name: Path to the RAT DS file to plot.
    :return: The created histogram
    """
    hit_times = ROOT.TH1D("hHitTimes", "Hit times for the calibrated PMTs", 500, 0.0, 500.0)
    hit_times.SetDirectory(0)
    for ds, run in rat.dsreader(file_name):
        for iev in range(0, ds.GetEVCount()):
            calibrated_pmts = ds.GetEV(iev).GetCalPMTs()
            for ipmt in range(0, calibrated_pmts.GetAllCount()):
                hit_times.Fill(calibrated_pmts.GetAllPMT(ipmt).GetTime())
    
    hit_times.GetYaxis().SetTitle( "Count per 1 ns bin" )
    hit_times.GetXaxis().SetTitle( "Hit times [ns]" )
    hit_times.Draw()
    return hit_times

def plot_hit_times(file_name):
    """ Plot all hit times from *file_name*

    :param file_name: Path to the RAT DS file to plot.
    :return: Tuple of the canvas and histograms
    """
    c1 = ROOT.TCanvas()
    pe = plot_mcphotoelectron_hit_times(file_name)
    mc = plot_mchit_times(file_name)
    calibrated = plot_calibrated_hit_times(file_name)
    pe.Draw()
    mc.SetLineColor(ROOT.kGreen + 2)
    mc.Draw("SAME")
    calibrated.SetLineColor(ROOT.kRed);
    calibrated.Draw("SAME");
    t1 = ROOT.TLegend(0.7, 0.7, 0.88, 0.88);
    t1.AddEntry(pe, "Photoelectrons", "l");
    t1.AddEntry(mc, "MC Hits", "l");
    t1.AddEntry(calibrated, "Calibrated", "l");
    t1.SetLineColor(ROOT.kWhite)
    t1.SetFillColor(ROOT.kWhite)
    t1.Draw();
    c1.Update();
    return (c1, pe, mc, calibrated, t1)
