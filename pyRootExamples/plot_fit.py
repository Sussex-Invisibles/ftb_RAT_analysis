#!/usr/bin/env python
#
# functions to plot aspects of the fit, e.g. positions & energy
#
#
#
# Author S Langrock - 2014-04-22 <s.langrock@qmul.ac.uk> : New file.
####################################################################################################
import ROOT
import rat

def plot_fit_energy(file_name):
    """ Plot the fitted energy.

    :param file_name: Path to the RAT DS file to plot.
    :return: The histogram plot
    """
    h_fit_energy = ROOT.TH1D( "hFitEnergy", "Fit energy", 500, 0.0, 5.0 )
    h_fit_energy.SetDirectory(0)
    for ds, run in rat.dsreader(file_name):
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)
            if not ev.DefaultFitVertexExists() or not ev.GetDefaultFitVertex().ContainsEnergy() or not ev.GetDefaultFitVertex().ValidEnergy():
                continue  #didn't fit succesfully
            h_fit_energy.Fill(ev.GetDefaultFitVertex().GetEnergy())
    h_fit_energy.GetYaxis().SetTitle( "Count per 10keV bin ")
    h_fit_energy.GetXaxis().SetTitle( "Fitted energy [MeV] ")
    h_fit_energy.Draw()
    return h_fit_energy

def plot_fit_radius(file_name):
    """ Plot the fitted radial position.

    :param file_name: Path to the RAT DS file to plot.
    :return: The histogram plot
    """
    h_fit_radius = ROOT.TH1D( "hFitRadius", "Fit radius", 800, 0.0, 8000.0 )
    h_fit_radius.SetDirectory(0)
    for ds, run in rat.dsreader(file_name):
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)
            if not ev.DefaultFitVertexExists() or not ev.GetDefaultFitVertex().ContainsEnergy() or not ev.GetDefaultFitVertex().ValidEnergy():
                continue  #didn't fit succesfully
            h_fit_radius.Fill(ev.GetDefaultFitVertex().GetPosition().Mag())
    h_fit_radius.GetYaxis().SetTitle( "Count per 10mm bin ")
    h_fit_radius.GetXaxis().SetTitle( "Fitted radius [mm] ")
    h_fit_radius.Draw()
    return h_fit_radius

def plot_fit_time(file_name):
    """ Plot the fitted time.

    :param file_name: Path to the RAT DS file to plot.
    :return: The histogram plot
    """
    h_fit_time = ROOT.TH1D( "hFitTime", "Fit time", 100, 0.0, 400.0 )
    h_fit_time.SetDirectory(0)
    for ds, run in rat.dsreader(file_name):
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)
            if not ev.DefaultFitVertexExists() or not ev.GetDefaultFitVertex().ContainsTime() or not ev.GetDefaultFitVertex().ValidTime():
                continue  #didn't fit succesfully
            h_fit_time.Fill(ev.GetDefaultFitVertex().GetTime())
    h_fit_time.GetYaxis().SetTitle( "Count per 4ns bin ")
    h_fit_time.GetXaxis().SetTitle( "Fitted time [ns] ")
    h_fit_time.Draw()
    return h_fit_time

def plot_fit_direction_phi(file_name):
    """ Plot the fitted direction phi.

    :param file_name: Path to the RAT DS file to plot.
    :return: The histogram plot
    """
    h_fit_direction_phi = ROOT.TH1D( "hFitDirectionPhi", "Fit direction (phi)", 180, -180, 180 )
    h_fit_direction_phi.SetDirectory(0)
    for ds, run in rat.dsreader(file_name):
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)
            if not ev.DefaultFitVertexExists() or not ev.GetDefaultFitVertex().ContainsDirection() or not ev.GetDefaultFitVertex().ValidDirection():
                continue  #didn't fit succesfully
            h_fit_direction_phi.Fill(ev.GetDefaultFitVertex().GetDirection().Phi() * ROOT.TMath.RadToDeg())
    h_fit_direction_phi.GetYaxis().SetTitle( "Count per 2 degree bin ")
    h_fit_direction_phi.GetXaxis().SetTitle( "Fitted phi direction [#circ] ")
    h_fit_direction_phi.Draw()
    return h_fit_direction_phi

def plot_fit_direction_theta(file_name):
    """ Plot the fitted direction theta.

    :param file_name: Path to the RAT DS file to plot.
    :return: The histogram plot
    """
    h_fit_direction_theta = ROOT.TH1D( "hFitDirectionTheta", "Fit direction (theta)", 180, -180, 180 )
    h_fit_direction_theta.SetDirectory(0)
    for ds, run in rat.dsreader(file_name):
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)
            if not ev.DefaultFitVertexExists() or not ev.GetDefaultFitVertex().ContainsDirection() or not ev.GetDefaultFitVertex().ValidDirection():
                continue  #didn't fit succesfully
            h_fit_direction_theta.Fill(ev.GetDefaultFitVertex().GetDirection().Theta() * ROOT.TMath.RadToDeg())
    h_fit_direction_theta.GetYaxis().SetTitle( "Count per 2 degree bin ")
    h_fit_direction_theta.GetXaxis().SetTitle( "Fitted theta direction [#circ] ")
    h_fit_direction_theta.Draw()
    return h_fit_direction_theta
                             
