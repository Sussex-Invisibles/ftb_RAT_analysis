#!/usr/bin/env python
#
# functions to plot nhit (various definitions)
#
# Nhit could be the MC photoelectrons, the MC hits, the EV uncalibrated or the EV calibrated.
# All examples are included.
#
# Author S Langrock - 2014-04-22 <s.langrock@qmul.ac.uk> : New file.
####################################################################################################
import ROOT
import rat

def plot_mc_photoelectron_nhit(file_name):
    """ Plot the number of MC photoelectrons per event (or NumPE).

    :param file_name: Path to the RAT DS file to plot.
    :return: The histogram plot
    """
    h_num_pe = ROOT.TH1D( "hNumPE", "Number of photoelectrons per event", 2000, 0.0, 2000.0 )
    h_num_pe.SetDirectory(0)
    for ds, run in rat.dsreader(file_name):
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)
            h_num_pe.Fill(ds.GetMC().GetPhotoelectronCount())
    h_num_pe.GetYaxis().SetTitle( "Count per 1 pe bin" )
    h_num_pe.GetXaxis().SetTitle( "Number of photoelectrons per event" )
    h_num_pe.Draw()
    return h_num_pe

def plot_mc_hits_nhit(file_name):
    """ Plot the number of MC hits per event.

    :param file_name: Path to the RAT DS file to plot.
    :return: The histogram plot
    """
    h_num_hits = ROOT.TH1D( "hNumHits", "Number of MC hits per event", 2000, 0.0, 2000.0 )
    h_num_hits.SetDirectory(0)
    for ds, run in rat.dsreader(file_name):
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)
            for imc in range(0, ds.GetMCEVCount()):   #loop over triggered events
                h_num_hits.Fill(ds.GetMCEV(imc).GetMCHits().GetAllCount())  # All canbe changed to Normal, OWL, etc...
    h_num_hits.GetYaxis().SetTitle( "Count per 1 MC bin" )
    h_num_hits.GetXaxis().SetTitle( "Number of MC hits per event" )
    h_num_hits.Draw()
    return h_num_hits

def plot_uncalibrated_nhit(file_name):
    """ Plot the number of Uncalibrated hits per event.

    :param file_name: Path to the RAT DS file to plot.
    :return: The histogram plot
    """
    h_uncal_hits = ROOT.TH1D( "hUncalHits", "Number of Uncalibrated hits per event", 2000, 0.0, 2000.0 )
    h_uncal_hits.SetDirectory(0)
    for ds, run in rat.dsreader(file_name):
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)
            h_uncal_hits.Fill(ev.GetUncalPMTs().GetAllCount())
    h_uncal_hits.GetYaxis().SetTitle( "Count per 1 Uncalibrated hit bin" )
    h_uncal_hits.GetXaxis().SetTitle( "Number of Uncalibrated hits per event" )
    h_uncal_hits.Draw()
    return h_uncal_hits

def plot_calibrated_nhit(file_name):
    """ Plot the number of Calibrated hits per event.

    :param file_name: Path to the RAT DS file to plot.
    :return: The histogram plot
    """
    h_cal_hits = ROOT.TH1D( "hCalHits", "Number of Calibrated hits per event", 2000, 0.0, 2000.0 )
    h_cal_hits.SetDirectory(0)
    for ds, run in rat.dsreader(file_name):
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)
            h_cal_hits.Fill(ev.GetCalPMTs().GetAllCount())
    h_cal_hits.GetYaxis().SetTitle( "Count per 1 Calibrated hit bin" )
    h_cal_hits.GetXaxis().SetTitle( "Number of Calibrated hits per event" )
    h_cal_hits.Draw()
    return h_cal_hits

def plot_nhit(file_name):
    """ Plot all nhit numbers.

    :param file_name: Path to the RAT DS file to plot.
    """
    c1 = ROOT.TCanvas()
    num_pe = plot_mc_photoelectron_nhit(file_name)
    mc_hits = plot_mc_hits_nhit(file_name)
    uncalibrated = plot_uncalibrated_nhit(file_name)
    calibrated = plot_calibrated_nhit(file_name)
    c1.cd()
    num_pe.Draw()
    mc_hits.SetLineColor(8)
    mc_hits.Draw("same")
    uncalibrated.SetLineColor(4)
    uncalibrated.Draw("same")
    calibrated.SetLineColor(2)
    calibrated.Draw("same")
    t1 = ROOT.TLegend( 0.7 , 0.7 , 0.9 , 0.9 )
    t1.AddEntry(num_pe, "Photoelectrons", "l")
    t1.AddEntry(mc_hits, "MC Hits", "l")
    t1.AddEntry(uncalibrated, "Uncalibrated", "l")
    t1.AddEntry(calibrated, "Calibrated", "l")
    t1.SetFillColor(ROOT.kWhite)
    t1.Draw("same")
    #c1.Update()
    # All the objects have to be returned or they go out of scope and 
    # the memory will be collected by python
    return c1,num_pe,mc_hits,uncalibrated,calibrated,t1
