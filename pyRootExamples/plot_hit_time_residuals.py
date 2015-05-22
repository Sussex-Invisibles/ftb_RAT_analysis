#!/usr/bin/env python
#
# plot_hit_time_residuals_mc_position, plot_hit_time_residuals_fit_position, plot_hit_time_residuals
#
# EV Calibrated hit times are plotted minus transit times based on the MC position or the fitted position.
#
# Author P G Jones - 2014-04-19 <p.g.jones@qmul.ac.uk> : New file.
####################################################################################################
import ROOT
import rat

def plot_hit_time_residuals_mc_position(file_name):
    """ Plot the hit time residuals for the MC position.

    :param file_name: Path to the RAT DS file to plot.
    :return: The created histogram
    """
    hit_time_residuals = ROOT.TH1D( "hHitTimeResidualsMC", "Hit time residuals using the MC position", 1000, -500.0, 500.0 );
    hit_time_residuals.SetDirectory(0)
    light_path = rat.utility().GetLightPath()
    group_velocity = rat.utility().GetGroupVelocity()
    pmt_info = rat.utility().GetPMTInfo()
    for ds, run in rat.dsreader(file_name):
        event_position = ds.GetMC().GetMCParticle(0).GetPosition() # At least 1 is somewhat guaranteed
        for iev in range(0, ds.GetEVCount()):
            calibrated_pmts = ds.GetEV(iev).GetCalPMTs()
            for ipmt in range(0, calibrated_pmts.GetCount()):
                pmt_cal = calibrated_pmts.GetPMT(ipmt)
                scint_distance = ROOT.Double()
                av_distance = ROOT.Double()
                water_distance = ROOT.Double()
                light_path.CalcByPosition(event_position, pmt_info.GetPosition(pmt_cal.GetID()), 
                                          scint_distance, av_distance, water_distance)
                transit_time = group_velocity.CalcByDistance(scint_distance, av_distance, water_distance) # Assumes 400nm photon
                hit_time_residuals.Fill(pmt_cal.GetTime() - transit_time)

    hit_time_residuals.GetYaxis().SetTitle("Count per 1 ns bin")
    hit_time_residuals.GetXaxis().SetTitle("Hit time residuals [ns]")
    hit_time_residuals.Draw()
    return hit_time_residuals

def plot_hit_time_residuals_fit_position(file_name):
    """ Plot the hit time residuals for the fit position.

    :param file_name: Path to the RAT DS file to plot.
    :return: The created histogram
    """
    hit_time_residuals = ROOT.TH1D( "hHitTimeResidualsFit", "Hit time residuals using the fit position", 1000, -500.0, 500.0 );
    hit_time_residuals.SetDirectory(0)
    light_path = rat.utility().GetLightPath()
    group_velocity = rat.utility().GetGroupVelocity()
    pmt_info = rat.utility().GetPMTInfo()
    for ds, run in rat.dsreader(file_name):
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)
            if not ev.DefaultFitVertexExists() or not ev.GetDefaultFitVertex().ContainsPosition() or not ev.GetDefaultFitVertex().ValidPosition():
                continue #Didn't fit correctly
            event_position = ev.GetDefaultFitVertex().GetPosition();
            calibrated_pmts = ev.GetCalPMTs()
            for ipmt in range(0, calibrated_pmts.GetCount()):
                pmt_cal = calibrated_pmts.GetPMT(ipmt)
                scint_distance = ROOT.Double()
                av_distance = ROOT.Double()
                water_distance = ROOT.Double()
                light_path.CalcByPosition(event_position, pmt_info.GetPosition(pmt_cal.GetID()), 
                                          scint_distance, av_distance, water_distance)
                transit_time = group_velocity.CalcByDistance(scint_distance, av_distance, water_distance) # Assumes 400nm photon
                hit_time_residuals.Fill(pmt_cal.GetTime() - transit_time)

    hit_time_residuals.GetYaxis().SetTitle("Count per 1 ns bin")
    hit_time_residuals.GetXaxis().SetTitle("Hit time residuals [ns]")
    hit_time_residuals.Draw()
    return hit_time_residuals

def plot_hit_time_residuals(file_name):
    """ Plot all hit times from *file_name*

    :param file_name: Path to the RAT DS file to plot.
    :return: Tuple of the canvas and histograms
    """
    c1 = ROOT.TCanvas()
    mc = plot_hit_time_residuals_mc_position(file_name)
    fit = plot_hit_time_residuals_fit_position(file_name)
    mc.Draw("SAME")
    fit.SetLineColor(ROOT.kGreen + 2);
    fit.Draw("SAME");
    t1 = ROOT.TLegend(0.7, 0.7, 0.88, 0.88);
    t1.AddEntry(mc, "MC Position", "l");
    t1.AddEntry(fit, "Fit Position", "l");
    t1.SetLineColor(ROOT.kWhite)
    t1.SetFillColor(ROOT.kWhite)
    t1.Draw();
    c1.Update();
    return (c1, mc, fit, t1)
