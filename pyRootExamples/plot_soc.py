#!/usr/bin/env python
#
# functions to plot soc centroid times
#
# The centroid times are calculated by the soc peak fitter proc 
# and the soc data itself by the soc data proc
#
# Author S Langrock - 2014-04-22 <s.langrock@qmul.ac.uk> : New file.
####################################################################################################
import ROOT
import rat

def plot_centroid(file_name):
    """ Plot the centroid hit time.

    :param file_name: Path to the RAT SOC file to plot.
    :return: The histogram plot
    """
    h_centroid = ROOT.TH1D( "hCentroid", "Centroid hit time", 500, 0.0, 500.0 )
    rsoc = ROOT.RAT.DU.SOCReader(file_name) 
    for isoc in range(0, rsoc.GetSOCCount()):
        soc = rsoc.GetSOC(isoc)
        pmt_ids = soc.GetSOCPMTIDs()
        for ipmt in range(0,pmt_ids.size()):
            h_centroid.Fill(soc.GetSOCPMT(pmt_ids[ipmt]).GetTimeCentroid())
    h_centroid.GetYaxis().SetTitle("Time [ns]")
    h_centroid.GetXaxis().SetTitle("Centroid hit time")
    h_centroid.Draw()
    return h_centroid
