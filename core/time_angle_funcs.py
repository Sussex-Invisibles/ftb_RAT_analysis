####################################################
# Functions used in analysis of reflections data 
# for the December 2014 ftb data run.
#
# Author: Ed Leming
# Date  : 10/02/2014
####################################################
import rat
import ROOT
import numpy as np
import utils.DataQualityProc as dqp
import utils.calc as calc

def plot_time_vs_angle_QHS(fname, fibre_pos, fibre_name):
    """ Plot the number of Calibrated hits per event.

    :param fname: Path to the RAT DS file to plot.
    :return: The histogram plot
    """
    hit_time, theta_arr, phi_arr = np.array([]), np.array([]), np.array([])
    time_angle = ROOT.TH2D("Time_angle", "Angle vs hit time - %s" % fibre_name, 200, 0., 100., 450, -250., 200.)
    time_QHS = ROOT.TH2D("Time_QHS", "QHS vs hit time - %s" % fibre_name, 700, 0., 700., 500, -250., 250.)
    time_hist = ROOT.TH1D("All_event", "Hit times - %s" % fibre_name, 450, -250., 200.)
    for ds, run in rat.dsreader(fname):
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)
            if dqp.check_trig_type(ev.GetTrigType()) and ev.GetClockCount50() != 0:
                pmtInfo = rat.utility().GetPMTInfo()
                calibrated_pmts = ds.GetEV(iev).GetCalPMTs()
                for ipmt in range(0, calibrated_pmts.GetNormalCount()):
                    pmt_t = calibrated_pmts.GetNormalPMT(ipmt).GetTime()
                    QHS = calibrated_pmts.GetNormalPMT(ipmt).GetQHS()
                    pmtID = calibrated_pmts.GetNormalPMT(ipmt).GetID()
                    pmt_pos = pmtInfo.GetPosition(pmtID)
                    fibre_vec = ROOT.TVector3(fibre_pos.GetD("x"), fibre_pos.GetD("y"), fibre_pos.GetD("z"))
                    fibre_to_pmt = - pmt_pos + fibre_vec
                    angle = fibre_to_pmt.Angle(fibre_vec)*(180/np.pi)
                    #dot = fibre_to_pmt.Dot(fibre_vec)
                    #theta = np.arccos( dot / (fibre_to_pmt.Mag()*fibre_vec.Mag()) )*(180/np.pi)
                    #theta, phi = calc.fibre_pmt_theta_phi(fibre_pos, pmt_pos)
                    #hit_time = np.hstack( (hit_time, [pmt_t]) )                        
                    #theta_arr = np.hstack( (theta_arr, [theta])  )
                    #phi_arr = np.hstack( (theta_arr, [phi])  )
                    time_QHS.Fill(QHS, pmt_t)
                    time_angle.Fill(angle, pmt_t)
                    time_hist.Fill(pmt_t)
                    #time_phi.Fill(phi, pmt_t)
                #print angle, pmt_t, QHS 
                #print calibrated_pmts.GetNormalCount(), calibrated_pmts.GetAllCount(), QHS, pmt_t, theta, phi

    time_QHS.GetYaxis().SetTitle("Time (ns)")
    time_QHS.GetXaxis().SetTitle("QHS")
    time_angle.GetYaxis().SetTitle("Time (ns)")
    time_angle.GetXaxis().SetTitle("Angle (deg)")
    #time_phi.GetYaxis().SetTitle("Time (ns)")
    #time_phi.GetXaxis().SetTitle("Phi (deg)")
    return time_hist, time_angle, time_QHS

def plot_cone_PMT_data(fname, fibre_pos, max_angle, fibre_name):
    """ Consider a cone projected about the fibre injection position. Check
    which PMTs reside within this cone and store data PMT-wise over a whole
    run.

    :param fname: Path to the RAT DS file to evaluate.
    :param fibre_pos: Position of the active fibre. 
    :param max_angle: Maximum apperture of light cone to be considered.
    :param fibre_name: Name of the active fibre being considered.
    :return: An array of hit time historgrams for each pmt within the cone.
    """
    # Find PMT_IDs of all PMTs within projected cone. 
    pmt_count, ids = cone_to_PMT_IDs(fibre_pos, max_angle)
    # Make histograms and TGraphs
    hists, graphs = np.empty(pmt_count, dtype=object), np.empty(pmt_count, dtype=object)
    hist_count = 0
    hist_it = {}
    for i in range(len(ids)):
        if ids[i] == True:
            hists[hist_count] = ROOT.TH1D("PMT_%i" % (i), "Hit times at PMT_%i" % (i), 450, -250., 200.)
            hists[hist_count].GetXaxis().SetTitle("Time (ns)")
            graphs[hist_count] = ROOT.TGraph()
            graphs[hist_count].SetName("PMT_%i_ordered" % (i))
            graphs[hist_count].SetTitle("Hit times as a function of event at PMT_%i" %i)
            graphs[hist_count].GetXaxis().SetTitle("Event time (50Mhz)")
            graphs[hist_count].GetYaxis().SetTitle("Hit time (ns)")
            hist_it[i] = hist_count
            hist_count = hist_count + 1
    # Loop over run data 
    pmtInfo = rat.utility().GetPMTInfo()
    ipt = 0
    for ds, run in rat.dsreader(fname):
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)
            if dqp.check_trig_type(ev.GetTrigType()) and ev.GetClockCount50() != 0:
                calibrated_pmts = ds.GetEV(iev).GetCalPMTs()
                for ipmt in range(0, calibrated_pmts.GetNormalCount()):
                    pmtID = calibrated_pmts.GetNormalPMT(ipmt).GetID()
                    if ids[pmtID] == True:
                        pmt_t = calibrated_pmts.GetNormalPMT(ipmt).GetTime()         
                        clock = ev.GetClockCount50()
                        hists[hist_it[pmtID]].Fill(pmt_t)
                        if pmt_t > -250 and pmt_t < 200 and clock != 0:
                            graphs[hist_it[pmtID]].SetPoint(ipt,clock,pmt_t)
                            ipt = ipt + 1 
    return hists, graphs

def cone_to_PMT_IDs(fibre_pos, max_angle):
    """ Create a dictionary containing PMT_ID for all PMTs. Those within the light cone 
    have values set to True. 

    :param fibre_pos: Three vector containing position of active fibre's injection pos.
    :param max_angle: Maximum allowed angle of light cone projected from fibre_pos. 
    :return ids: Dictionary containing each PMT_ID as keys. If PMT is within cone value = True, 
    otherwise value = False.
    """
    ids = {}
    count = 0
    pmt_info = ROOT.RAT.DU.Utility.Get().GetPMTInfo()
    for ent in range(pmt_info.GetCount()):
        pmt_pos = pmt_info.GetPosition(ent)
        fibre_vec = ROOT.TVector3(fibre_pos.GetD("x"), fibre_pos.GetD("y"), fibre_pos.GetD("z"))
        fibre_to_pmt = - pmt_pos + fibre_vec
        angle = fibre_to_pmt.Angle(fibre_vec)*(180/np.pi)
        if angle < max_angle:
            count = count + 1
            ids[ent] = True
        else:
            ids[ent] = False
    return count, ids

def fibre_to_pmt_angle(fibre_pos, pmt_pos):
    """ Calculate angle between fibre position and specific pmt. 

    :param fibre_pos: RATDB object containing position of active fibre's injection pos.
    :param pmt_pos: ROOT TVector3 from utils.PMTinfo().GetPosition(n).
    :return angle: Angle between the chord from fibre to pmt and fibre vector.
    """
    fibre_vec = ROOT.TVector3(fibre_pos.GetD("x"), fibre_pos.GetD("y"), fibre_pos.GetD("z"))
    fibre_to_pmt = - pmt_pos + fibre_vec
    return fibre_to_pmt.Angle(fibre_vec)*(180/np.pi)

def fibre_pos_to_angle(fibre_pos):
    """ Create a dictionary containing PMT_ID for all PMTs. Those with 

    :param fibre_pos: Three vector containing position of active fibre's injection pos.
    :return angles: A dictionary containing each PMT_ID as keys and their angle w.r.t the fibre
    injection position as values. 
    """
    angles = {}
    pmt_info = ROOT.RAT.DU.Utility.Get().GetPMTInfo()
    for ent in range(pmt_info.GetCount()):
        pmt_pos = pmt_info.GetPosition(ent)
        fibre_vec = ROOT.TVector3(fibre_pos.GetD("x"), fibre_pos.GetD("y"), fibre_pos.GetD("z"))
        fibre_to_pmt = - pmt_pos + fibre_vec
        angle = fibre_to_pmt.Angle(fibre_vec)*(180/np.pi)
        angles[ent] = angle
    return angles

def plot_hit_times(fname, fibre_name):
    """ Plot the hit times seen in a TELLIE events.

    :param fname: Path to the RAT DS file to plot.
    :return: The histogram plot
    """
    single_hist =  ROOT.TH1D("Single_event", "Hit times in a single event - %s" % fibre_name, 225, -250., 200.)
    time_hist = ROOT.TH1D("All_event", "Hit times - %s" % fibre_name, 450, -250., 200.)
    flag = False
    for ds, run in rat.dsreader(fname):
        for iev in range(0, ds.GetEVCount()):
            ev = ds.GetEV(iev)
            if dqp.check_trig_type(ev.GetTrigType()) and ev.GetClockCount50() != 0:
                pmtInfo = rat.utility().GetPMTInfo()
                calibrated_pmts = ds.GetEV(iev).GetCalPMTs()
                for ipmt in range(0, calibrated_pmts.GetNormalCount()):
                    pmt_t = calibrated_pmts.GetNormalPMT(ipmt).GetTime()
                    time_hist.Fill(pmt_t)
                    if flag == False and calibrated_pmts.GetNormalCount() > 100:
                        single_hist.Fill(pmt_t)
                if calibrated_pmts.GetNormalCount() > 100:
                    flag = True
                print pmt_t
    time_hist.GetYaxis().SetTitle("NHit")
    time_hist.GetXaxis().SetTitle("Time (ns)")
    single_hist.GetYaxis().SetTitle("NHit")
    single_hist.GetXaxis().SetTitle("Time (ns)")
    return time_hist, single_hist
