#import yaml # Needs installing, not part of the standard python library
import ROOT
import sys
import os
import rat
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
    db.LoadDefaults()
    return db

def get_pmt_position(x,y,z,lcn):
    return ROOT.TVector3(x[lcn],y[lcn],z[lcn])
  
  
def load_pmt_positions(db):
    """ Load PMT positions
    """
    db.LoadFile("/home/j/jw/jw419/snoplus/muon_valid/rat/data/pmt/airfill2.ratdb")
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
    
