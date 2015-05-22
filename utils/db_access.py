#import yaml # Needs installing, not part of the standard python library
import ROOT
import sys
import os
import rat
import couchdb
import numpy as np
#from minify_json import json_minify # Available from https://github.com/getify/JSON.minify
 
#def LoadRatDB( fileName ):
#    """ Load a ratdb file and return a dictionary of the contents."""
#    ratDBFile = open( fileName, "r" )
#    dataDict = yaml.load( json_minify( ratDBFile.read(), False ) )
#    ratDBFile.close()
#    return dataDict

def get_rat_db():
    ROOT.RAT.Log.Init("/dev/null")
    db = ROOT.RAT.DB.Get()
    if not db:
        print "Error loading db!"
        sys.exit(1)
    glg4data = os.getenv("GLG4DATA")
    #db.LoadDefaults()
    return db

def get_pmt_position(x,y,z,lcn):
    return ROOT.TVector3(x[lcn],y[lcn],z[lcn])
  
  
def load_pmt_positions(db):
    """ Load PMT positions
    """
    #db.LoadFile("/home/j/jw/jw419/snoplus/muon_valid/rat/data/pmt/airfill2.ratdb")
    pmt_info = db.GetLink("PMTINFO")
    return pmt_info.GetDArray("x"),pmt_info.GetDArray("y"),pmt_info.GetDArray("z")
    
def get_fibre_data(db,fibre):
    return db.GetLink("FIBRE",fibre)

def get_fibre_position(db,fibre):
    """ Load LED positions
    """
    fibre_data = get_fibre_data(db,fibre)
    return ROOT.TVector3(fibre_data.GetD("x"),fibre_data.GetD("y"),fibre_data.GetD("z"))
    

def get_fibre_direction(db,fibre):
    """ Load LED directions
    """
    fibre_data = get_fibre_data(db,fibre)
    return ROOT.TVector3(fibre_data.GetD("u"),fibre_data.GetD("v"),fibre_data.GetD("w"))
    
def get_tellie_cauch_db():
    """ Get tellie cauch_db pointer
    """
    server = couchdb.Server("http://couch.snopl.us")
    server.resource.credentials = ("snoplus", "PureTe->Dirac!=True")
    cauch_db = server["telliedb"]
    return cauch_db

def get_cauch_rows(cauch_db, run_no):
    """ Get cauch_db data for specific run
    """
    return cauch_db.view("_design/runs/_view/run_by_number", key=run_no, include_docs=True)

def get_cauch_PIN_reading(cauch_db, run_no):
    """ Get cauch_db data for specific run                                                
    """
    pin = np.array([])
    rows = cauch_db.view("_design/runs/_view/run_by_number", key=run_no, include_docs=True)
    for row in rows:
        sub_run_info = row.doc["sub_run_info"]
        for sub in sub_run_info:
            pin = np.hstack( (pin, [sub["pin_readout"]]) )
    return pin

def get_cauch_pulse_rate(cauch_db, run_no):
    """ Get cauch_db data for specific run  
    """
    pulse_rate = np.array([])
    rows = cauch_db.view("_design/runs/_view/run_by_number", key=run_no, include_docs=True)
    for row in rows:
        sub_run_info = row.doc["sub_run_info"]
        for sub in sub_run_info:
            pulse_rate = np.hstack( (pulse_rate, [sub["pulse_rate"]]) )
    return pulse_rate

def get_cauch_number_of_shots(cauch_db, run_no):
    """ Get cauch_db data for specific run 
    """
    noShots = np.array([])
    rows = cauch_db.view("_design/runs/_view/run_by_number", key=run_no, include_docs=True)
    for row in rows:
        sub_run_info = row.doc["sub_run_info"]
        for sub in sub_run_info:
            noShots = np.hstack( (noShots, [sub["number_of_shots"]]) )
    return noShots

def get_cauch_pulse_width(cauch_db, run_no):
    """ Get cauch_db data for specific run                                                                                                  
    """
    pulse_width = np.array([])
    rows = cauch_db.view("_design/runs/_view/run_by_number", key=run_no, include_docs=True)
    for row in rows:
        sub_run_info = row.doc["sub_run_info"]
        for sub in sub_run_info:
            pulse_width = np.hstack( (pulse_width, [sub["pulse_width"]]) )
    return pulse_width
