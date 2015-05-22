#!/usr/bin/env python
#
# functions to select and plot track features 
#
#
#
# Author S Langrock - 2014-04-22 <s.langrock@qmul.ac.uk> : New file.
####################################################################################################
import ROOT
import rat

def plot_track_length(file_name):
    """ Plot the length of tracks that underwent reemission.
    see RAT/include/MCTrack.hh ESummaryFlag for other processes

    :param file_name: Path to the RAT root file to plot.
    :return: The histogram plot
    """
    ROOT.gStyle.SetOptStat(111111)  #to show overflow / underflow stats
    #process the summary flag
    flag = ROOT.RAT.DS.MCTrack.OpReemission
    h_track_length = ROOT.TH1D( "hTrackLengths", "MC track length", 600, 0, 6000 )
    for ds, run in rat.dsreader(file_name):
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)
            mc = ds.GetMC()
            for itrack in range(0, mc.GetMCTrackCount()):
                mctrack = mc.GetMCTrack(itrack)
                if mctrack.GetSummaryFlag(flag):
                    h_track_length.Fill(mctrack.GetLength())
    h_track_length.SetXTitle( "Track Length (mm)" )
    h_track_length.SetYTitle( "Counts per 10 mm" )
    h_track_length.Draw()
    return h_track_length

def plot_edep_step(file_name):
    """ Plot the energy deposited for neutron capture track steps.
    see RAT/include/MCTrackStep.hh for other possible track step processes

    :param file_name: Path to the RAT root file to plot.
    :return: The histogram plot
    """
    process = "nCapture"
    
    h_edep_step = ROOT.TH1D( "hEdepStep", "Energy deposited", 500, 0, 5 )
    for ds, run in rat.dsreader(file_name):
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)
            mc = ds.GetMC()
            for itrack in range(0, mc.GetMCTrackCount()):
                mctrack = mc.GetMCTrack(itrack)
                for istep in range(0, mctrack.GetMCTrackStepCount()):
                    mctrackstep = mctrack.GetMCTrackStep(istep)
                    #note: it is possible to get processes either by name (string) or by enum.
                    if mctrackstep.GetProcess() == process:
                        h_edep_step.Fill(mctrackstep.GetDepositedEnergy())
    h_edep_step.SetXTitle( "Energy deposited (MeV)" )
    h_edep_step.SetYTitle( "Counts per 10 keV" )
    h_edep_step.Draw()
    return h_edep_step

def plot_ke_step(file_name):
    """ Plot the final kinetic energy for Compton scattering track steps.
    see RAT/include/MCTrackStep.hh for other possible track step processes

    :param file_name: Path to the RAT root file to plot.
    :return: The histogram plot
    """
    process = ROOT.RAT.DS.MCTrackStep.compt
    h_ke_step = ROOT.TH1D( "hKEStep", "Kinetic energy", 500, 0, 0.5 )
    for ds, run in rat.dsreader(file_name):
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)
            mc = ds.GetMC()
            for itrack in range(0, mc.GetMCTrackCount()):
                mctrack = mc.GetMCTrack(itrack)
                for istep in range(0, mctrack.GetMCTrackStepCount()):
                    mctrackstep = mctrack.GetMCTrackStep(istep)
                    if mctrackstep.GetProcessEnum() == process:
                        h_ke_step.Fill(mctrackstep.GetKineticEnergy())
    h_ke_step.SetXTitle( "Energy (MeV)" )
    h_ke_step.SetYTitle( "Counts per 1keV" )
    h_ke_step.Draw()
    return h_ke_step
