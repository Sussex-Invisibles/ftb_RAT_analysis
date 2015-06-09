import ROOT
import rat
import sys
import math

crateGap = 10
xOffset = 10
yOffset = 10

#///           LCN = channel number + 32 * card number + 512 * crate number
def crateNumber(lcn):
    return int(lcn/512)

def cardNumber(lcn):
    return int((lcn-(512*crateNumber(lcn)))/32)


def channelNumber(lcn):
    return lcn-(32*cardNumber(lcn))-(512*crateNumber(lcn))

def drawCrates(fileName,hits,xbins=280,ybins=100):
    can = ROOT.TCanvas()
    h_proj = ROOT.TH2D("h_proj","NHits",xbins,0,1,ybins,0,1)
    for lcn in hits:
        crateNum = crateNumber(lcn)
        cardNum = cardNumber(lcn)
        channelNum = channelNumber(lcn)
        ybin = channelNum+yOffset
        xbin = cardNum+(crateNum*(16+crateGap))+xOffset
        if crateNum >= 9:
            ybin += 50
            xbin = cardNum+((crateNum-9)*(16+crateGap))+xOffset
        #16 cards per crate
        bin = h_proj.GetBin(xbin,ybin)
        h_proj.SetBinContent(bin,hits[lcn])
    h_proj.Draw("colz")
    fname = "../"+fileName+".pdf"
    can.Print(fname)

    


