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
from utils import DataQualityProc as dqp

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

def get_PMT_hits_cone(fname, fibre_pos, max_angle, flag=5241):
    """Find how many times PMTs in a cone surrounding the light injection
    vector were hit during a run.

    :param fname: Name of a .root data file containing the run data.
    :param fibre_pos: Vector of fibre injection position, relative to the centre of the psup.
    :param max_angle: The angle of the cone to be projected. 
    :return pmt_hits: Dictionary containing number of hits at PMTs activated during run.
    """
    pmt_hits = {}
    pmtInfo = rat.utility().GetPMTInfo()
    for ds, run in rat.dsreader(fname):
        for iEV in range(ds.GetEVCount()):
            ev = ds.GetEV(iEV)
            if (ev.GetTrigType() != 32768):
                continue
            unCal_pmts = ev.GetUncalPMTs()
            for pmt in range(unCal_pmts.GetNormalCount()):
                uncal = unCal_pmts.GetPMT(pmt)
                pmtID = unCal_pmts.GetNormalPMT(pmt).GetID()
                pmt_pos = pmtInfo.GetPosition(pmtID)
                fibre_vec = ROOT.TVector3(fibre_pos.GetD("x"), fibre_pos.GetD("y"), fibre_pos.GetD("z"))
                fibre_to_pmt = - pmt_pos + fibre_vec
                angle = fibre_to_pmt.Angle(fibre_vec)*(180/np.pi)
                lcn = uncal.GetID()
                if angle <= max_angle:
                    if lcn != flag:
                        if lcn not in pmt_hits:
                            pmt_hits[lcn] = 1.
                        else:
                            pmt_hits[lcn] += 1.
    return pmt_hits

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

def calc_time_diff_50MHz(start, stop):
    """Retrun the time difference in seconds between two 50MHz clock readings
    
    :param start: Initial clock reading
    :param stop : Final clock reading
    return time differnce [s]
    """
    return (stop-start)*2e-8

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

def get_init_nHit(fname, n):
    """ Plot and return the average nHit at start of event.

    param:  fname: Path to the RAT DS file to evaluate
    param:  n: The number of nHits to average over
    return: mean_nHit: The mean nHit of the first n events 
    return: nHit_hist: A histogram of the nHit distribution
    """
    c, nHit = 0, []
    n_hits = ROOT.TH1D( "init_nHits", "Number of hits for first %i events" % (n), 500, 0.0, 500 )
    n_hits.GetYaxis().SetTitle( "Count per 1 Calibrated hit bin" )
    n_hits.GetXaxis().SetTitle( "Number of Calibrated hits per event" )
    for ds, run in rat.dsreader(fname):
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)
            if dqp.check_trig_type(ev.GetTrigType()) and c <= n:
                c = c + 1
                n_hits.Fill(ev.GetCalPMTs().GetAllCount())
                nHit.append(ev.GetCalPMTs().GetAllCount())
                if c == n:
                    return np.mean(nHit), np.std(nHit), n_hits

def calc_time_from_50MHz_array(times):
    """ Calculate the time offsets relative to the first timestamp in an array

    :param times: Array of raw 50MHz time stamps.
    :return offsets: An array of time offsets (in seconds) relative to the earliest 50MHz stamp.
    """
    offset = np.zeros(len(times))
    start = min(times)
    for i in range(len(times)):
        offset[i] = calc_time_diff_50MHz(start, times[i])
    return offset

def track_mean_nHits(fname, sample_size, write_hist_flag=False):
    """ Plot the change in nHit over a run, relative to some calculated init_nHit.
    
    :param fname: Path to the RAT DS file to evaluate.
    :param sample_size: The number of events to be averaged to return a data point.
    :param write_hist_flag: Set to true to save each data point histo to file.
    :return TGraph of sampled nHit as a function of events
    :return TGraph of sampled nHit as a function of absolute time
    """
    sample_hist = ROOT.TH1F( "h_0", "", 500, 0.0, 500)
    start_clock = 0
    c, hist_count, nHits = 0, 0, np.array([])
    time, x, y = np.array([]), np.array([]), np.array([])
    y_stdError, y_stdDev, y_stdDevError = np.array([]), np.array([]), np.array([])
    for ds, run in rat.dsreader(fname):
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)
            if dqp.check_trig_type(ev.GetTrigType()) and ev.GetClockCount50() != 0:
                c = c + 1
                sample_hist.Fill(ev.GetCalPMTs().GetAllCount())
                nHits = np.hstack( (nHits, [ev.GetCalPMTs().GetAllCount()]) )
                #if start_clock == 0:
                #    start_clock = ev.GetClockCount50()
                if c % sample_size == 0:
                    #time = np.hstack( (time, [calc_time_diff_50MHz(start_clock, ev.GetClockCount50())]) )
                    time = np.hstack( (time, [ev.GetClockCount50()]) )
                    x = np.hstack( (x, [c]) )
                    y = np.hstack( (y, [np.mean(nHits)])  )
                    y_stdError = np.hstack( (y_stdError, [np.std(nHits) / np.sqrt(len(nHits))]) )
                    y_stdDev = np.hstack( (y_stdDev, [np.std(nHits)]) )
                    y_stdDevError = np.hstack( (y_stdDevError, [np.std(nHits) / np.sqrt(2*len(nHits)) ]) )
                    hist_count = hist_count + 1
                    if write_hist_flag:
                        sample_hist.Write()
                    sample_hist = ROOT.TH1F( "h_%i" % (hist_count), "", 500, 0.0, 500)
                    nHits = np.array([])
    # Find the first time stamp and use as start point.
    times =  calc_time_from_50MHz_array(time)
    # Plots
    Mgraph = ROOT.TGraphErrors(len(x), times, y, np.zeros(len(x)), y_stdError)
    Mgraph.SetTitle("Mean nHit as a function of time")
    Mgraph.GetXaxis().SetTitle("Time (s)")
    Mgraph.GetXaxis().SetTitleOffset(1.2)
    Mgraph.GetYaxis().SetTitle("nHit")
    Mgraph.GetYaxis().SetTitleOffset(1.2)
    Mgraph.SetMarkerStyle(33)

    Egraph = ROOT.TGraphErrors(len(x), times, y_stdDev, np.zeros(len(x)), y_stdDevError)
    Egraph.SetTitle("RMS spread on nHit as a function of time")
    Egraph.GetXaxis().SetTitle("Time (s)")
    Egraph.GetXaxis().SetTitleOffset(1.2)
    Egraph.GetYaxis().SetTitle("nHit RMS")
    Egraph.GetYaxis().SetTitleOffset(1.2)
    Egraph.SetMarkerStyle(33)

    w_mean, w_std = weighted_avg_and_std(y,y_stdError)
    return Mgraph, Egraph, w_mean, w_std

def plot_trigger_int(fname):
    """ Plot trigger type given for each event  

    :param fname: Path to the RAT DS file to plot.                                                     
    :return: The histogram plot
     """
    triggers = ROOT.TH1D( "eventTriggers", "Event triggers in run", 2000, 0.0, 2000.0)
    triggers.SetDirectory(0)
    for ds, run in rat.dsreader(fname):
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)
            triggers.Fill(ev.GetTrigType())
    triggers.GetYaxis().SetTitle( "Counts per trigger bin" )
    triggers.GetXaxis().SetTitle( "Trigger integer" )
    triggers.Draw()
    return triggers

def weighted_avg_and_std(values, weights):
    """Return the weighted average and standard deviation.

    values, weights -- Numpy ndarrays with the same shape.
    """
    average = np.average(values, weights=weights)
    variance = np.average((values-average)**2, weights=weights)  # Fast and numerically precise
    return average, np.sqrt(variance)
 
def two_axis_plot(p1, p2, title, save_path):
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
    p1.SetTitle(title)
    p2.SetTitle("")
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
    corr_graph.SetTitle("Correlations of TELLIE PIN readings and recorded nHits")
    tits_1 = p1.GetYaxis().GetTitle()
    tits_2 = p2.GetYaxis().GetTitle()
    corr_graph.GetXaxis().SetTitle(tits_1)
    corr_graph.GetYaxis().SetTitle(tits_2)
    corr_graph.GetXaxis().SetTitleOffset(1.2)
    corr_graph.GetYaxis().SetTitleOffset(1.2)
    corr_graph.SetMarkerStyle(33)
    return corr_graph

def calc_corr_coef(x_arr, y_arr):
    """Calculate the correlation coefficient of an (x,y) data set                                          
                                                                                                           
    param: x_array : Array containing the x data set                                                       
    param: y_array : Array containing the y data set                                                       
    return: correlation coefficient of the (x,y) data set                                                  
    """
    sxx, syy, sxy = 0, 0, 0
    x_hat, y_hat = np.mean(x_arr), np.mean(y_arr)
    for it, x in enumerate(x_arr):
        xi = (x - x_hat)
        yi = (y_arr[it] - y_hat)
        sxx = sxx + xi**2
        syy = syy + yi**2
        sxy = sxy + xi*yi
    return ( sxy / (np.sqrt(sxx) * np.sqrt(syy)) )

    
def plot_turn_on(fname, noEvents):
    """ Plot the change in nHit over a run, relative to some calculated init_nHit.

    :param fname: Path to the RAT DS file to evaluate
    """
    hist = ROOT.TH1F( "h_0", "", 50, 0.0, 50)
    nHits, time, event = np.array([]), np.array([]), np.array([])
    count, start_clock = 0, 0
    for ds, run in rat.dsreader(fname):
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)
            if dqp.check_trig_type(ev.GetTrigType()) and ev.GetClockCount50() != 0 and count < noEvents:
                if start_clock == 0:
                    start_clock = ev.GetClockCount50()
                nHits = np.hstack( (nHits, [ev.GetCalPMTs().GetAllCount()]) )
                time = np.hstack( (time, [calc_time_diff_50MHz(start_clock, ev.GetClockCount50())]) )
                event = np.hstack( (event, [count]) )
                count = count + 1
    
    graph = ROOT.TGraph(len(event), event, nHits)
    graph.SetTitle("Change in nHit for first %i events" % (noEvents))
    graph.GetXaxis().SetTitle("No. events")
    graph.GetXaxis().SetTitleOffset(1.2)
    graph.GetYaxis().SetTitle("nHit")
    graph.GetYaxis().SetTitleOffset(1.2)
    graph.SetMarkerStyle(33)
    Tgraph = ROOT.TGraph(len(time), time, nHits)
    Tgraph.SetTitle("Change in nHit for first %i events" % (noEvents))
    Tgraph.GetXaxis().SetTitle("Time (s)")
    Tgraph.GetXaxis().SetTitleOffset(1.2)
    Tgraph.GetYaxis().SetTitle("nHit")
    Tgraph.GetYaxis().SetTitleOffset(1.2)
    Tgraph.SetMarkerStyle(33)
    return graph, Tgraph

def track_mean_nHits_cone(fname, sample_size, fibre_pos, max_angle):
    """ Plot the change in nHit over a run, relative to some calculated init_nHit.

    :param fname: Path to the RAT DS file to evaluate.
    :param sample_size: The number of events to be averaged to return a data point.
    :param write_hist_flag: Set to true to save each data point histo to file.
    :return TGraph of sampled nHit as a function of events
    :return TGraph of sampled nHit as a function of absolute time
    """
    pmtInfo = rat.utility().GetPMTInfo()
    start_clock = 0
    c, hist_count, nHits = 0, 0, np.array([])
    time, x, y = np.array([]), np.array([]), np.array([])
    y_stdError, y_stdDev, y_stdDevError = np.array([]), np.array([]), np.array([])
    for ds, run in rat.dsreader(fname):
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)
            if dqp.check_trig_type(ev.GetTrigType()) and ev.GetClockCount50() != 0:
                c = c + 1
                pmt_count = 0
                calibrated_pmts = ds.GetEV(iev).GetCalPMTs()
                # Only accept PMT hits within cone
                for ipmt in range(0, calibrated_pmts.GetNormalCount()):
                    pmt_t = calibrated_pmts.GetNormalPMT(ipmt).GetTime()
                    QHS = calibrated_pmts.GetNormalPMT(ipmt).GetQHS()
                    pmtID = calibrated_pmts.GetNormalPMT(ipmt).GetID()
                    pmt_pos = pmtInfo.GetPosition(pmtID)
                    fibre_vec = ROOT.TVector3(fibre_pos.GetD("x"), fibre_pos.GetD("y"), fibre_pos.GetD("z"))
                    fibre_to_pmt = - pmt_pos + fibre_vec
                    angle = fibre_to_pmt.Angle(fibre_vec)*(180/np.pi)
                    if angle <= max_angle:
                        pmt_count = pmt_count + 1
                nHits = np.hstack( (nHits, [pmt_count]) )
                if c % sample_size == 0:
                    #time = np.hstack( (time, [calc_time_diff_50MHz(start_clock, ev.GetClockCount50())]) )
                    time = np.hstack( (time, [ev.GetClockCount50()]) )
                    x = np.hstack( (x, [c]) )
                    y = np.hstack( (y, [np.mean(nHits)])  )
                    y_stdError = np.hstack( (y_stdError, [np.std(nHits) / np.sqrt(len(nHits))]) )
                    y_stdDev = np.hstack( (y_stdDev, [np.std(nHits)]) )
                    y_stdDevError = np.hstack( (y_stdDevError, [np.std(nHits) / np.sqrt(2*len(nHits)) ]) )
                    hist_count = hist_count + 1

    # Find the first time stamp and use as start point.
    times =  calc_time_from_50MHz_array(time)
    # Plots
    Mgraph = ROOT.TGraphErrors(len(x), times, y, np.zeros(len(x)), y_stdError)
    Mgraph.SetTitle("Mean nHit as a function of time")
    Mgraph.GetXaxis().SetTitle("Time (s)")
    Mgraph.GetXaxis().SetTitleOffset(1.2)
    Mgraph.GetYaxis().SetTitle("nHit")
    Mgraph.GetYaxis().SetTitleOffset(1.2)
    Mgraph.SetMarkerStyle(33)

    Egraph = ROOT.TGraphErrors(len(x), times, y_stdDev, np.zeros(len(x)), y_stdDevError)
    Egraph.SetTitle("RMS spread on nHit as a function of time")
    Egraph.GetXaxis().SetTitle("Time (s)")
    Egraph.GetXaxis().SetTitleOffset(1.2)
    Egraph.GetYaxis().SetTitle("RMS nHit")
    Egraph.GetYaxis().SetTitleOffset(1.2)
    Egraph.SetMarkerStyle(33)

    w_mean, w_std = weighted_avg_and_std(y,y_stdError)
    return Mgraph, Egraph, w_mean, w_std
