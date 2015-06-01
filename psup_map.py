import sys
import ROOT
import rat
import math
import db_access
import calc

a = 1.0 / 5.5
b = a * math.sqrt( 3.0 ) / 2.0

A12a = ROOT.TVector2( a / 2.0, 0.0 )
A12b = ROOT.TVector2( 3.0 * a / 2.0, 0.0 )
A12c = ROOT.TVector2( 5.0 * a / 2.0, 0.0 )
A12d = ROOT.TVector2( 7.0 *a / 2.0, 0.0 )
A12e = ROOT.TVector2( 9.0 * a / 2.0, 0.0 )
A2a = ROOT.TVector2( 0.0, b )
A2b = ROOT.TVector2( 5.0 * a, b )
A17a = ROOT.TVector2( a / 2.0 , 2.0 * b )
A17b = ROOT.TVector2( 11.0 * a / 2.0 , 2.0 * b )
A51a = ROOT.TVector2( a, 3.0 * b )
A51b = ROOT.TVector2( 2.0 * a, 3.0 * b )
A51c = ROOT.TVector2( 3.0 * a, 3.0 * b )
A51d = ROOT.TVector2( 4.0 * a, 3.0 * b )
A51e = ROOT.TVector2( 5.0 * a, 3.0 * b )
A27 = ROOT.TVector2( 4.0 * a, b )
A46 = ROOT.TVector2( 3.0 * a, b )
A31 = ROOT.TVector2( 2.0 * a, b )
A6 = ROOT.TVector2( a, b )
A37 = ROOT.TVector2( 9.0 * a / 2.0 , 2.0 * b )
A33 = ROOT.TVector2( 3.0 * a / 2.0 , 2.0 * b )
A58 = ROOT.TVector2( 5.0 * a / 2.0 , 2.0 * b )
A54 = ROOT.TVector2( 7.0 * a / 2.0 , 2.0 * b )

def transform_coord(V1, V2, V3, A1, A2, A3, P):
    xV = V2 - V1
    yV = calc.multiply_3vector(( V3 - V1 ) + ( V3 - V2 ), 0.5)
    zV = xV.Cross( yV ).Unit()

    planeD = V1.Dot( zV )

    t = planeD / P.Dot( zV )

    localP = calc.multiply_3vector(P,t) - V1

    xA = A2 - A1
    yA = calc.multiply_2vector( ( A3 - A1 ) +( A3 - A2 ) ,0.5)

    convUnits = xA.Mod() / xV.Mag()

    result = calc.multiply_2vector(xA.Unit(),localP.Dot( xV.Unit() ) *convUnits)
    result = result + calc.multiply_2vector(yA.Unit(), localP.Dot( yV.Unit() )* convUnits) + A1
    return result

def icos_project(pmtPos):
    pointOnSphere = ROOT.TVector3( pmtPos.X(), pmtPos.Y(), pmtPos.Z() )
    pointOnSphere = pointOnSphere.Unit()
    pointOnSphere.RotateX( -45.0 )
    #From http://www.rwgrayprojects.com/rbfnotes/polyhed/PolyhedraData/Icosahedralsahedron/Icosahedralsahedron.pdf
      
    t = ( 1.0 + math.sqrt( 5.0 ) ) / 2.0
    V2 = ROOT.TVector3( t * t, 0.0, t * t * t ).Unit()
    V6 = ROOT.TVector3( -t * t, 0.0, t * t * t ).Unit()
    V12 = ROOT.TVector3( 0.0, t * t * t, t * t ).Unit()
    V17 = ROOT.TVector3( 0.0, -t * t * t, t * t ).Unit()
    V27 = ROOT.TVector3( t * t * t, t * t, 0.0 ).Unit()
    V31 = ROOT.TVector3( -t * t * t, t * t, 0.0 ).Unit()
    V33 = ROOT.TVector3( -t * t * t, -t * t, 0.0 ).Unit()
    V37 = ROOT.TVector3( t * t * t, -t * t, 0.0 ).Unit()
    V46 = ROOT.TVector3( 0.0, t * t * t, -t * t ).Unit()
    V51 = ROOT.TVector3( 0.0, -t * t * t, -t * t ).Unit()
    V54 = ROOT.TVector3( t * t, 0.0, -t * t * t ).Unit()
    V58 = ROOT.TVector3( -t * t, 0.0, -t * t * t ).Unit()
    #Faces {{ 2, 6, 17}, { 2, 12, 6}, { 2, 17, 37}, { 2, 37, 27}, { 2, 27, 12}, {37, 54, 27},
    #{27, 54, 46}, {27, 46, 12}, {12, 46, 31}, {12, 31, 6}, { 6, 31, 33}, { 6, 33, 17},
    #{17, 33, 51}, {17, 51, 37}, {37, 51, 54}, {58, 54, 51}, {58, 46, 54}, {58, 31, 46},
    #{58, 33, 31}, {58, 51, 33}}
    IcosahedralCentres = []
    const = 1./3.
    C1 = calc.multiply_3vector(( V2 + V6 + V17 ),const )
    IcosahedralCentres.append(C1)
    C2 = calc.multiply_3vector( ( V2 + V12 + V6 ), const )
    IcosahedralCentres.append(C2)
    C3 = calc.multiply_3vector( ( V2 + V17 + V37 ) , const )
    IcosahedralCentres.append(C3)
    C4 = calc.multiply_3vector( ( V2 + V37 + V27 ) , const )
    IcosahedralCentres.append(C4)
    C5 = calc.multiply_3vector( ( V2 + V27 + V12 ) , const )
    IcosahedralCentres.append(C5)
    C6 = calc.multiply_3vector( ( V37 + V54 + V27 ) , const )
    IcosahedralCentres.append(C6)

    C7 = calc.multiply_3vector( ( V27 + V54 + V46 ) , const )
    IcosahedralCentres.append(C7)
    C8 = calc.multiply_3vector( ( V27 + V46 + V12 ) , const )
    IcosahedralCentres.append(C8)
    C9 = calc.multiply_3vector( ( V12 + V46 + V31 ) , const )
    IcosahedralCentres.append(C9)
    C10 = calc.multiply_3vector( ( V12 + V31 + V6 ) , const )
    IcosahedralCentres.append(C10)
    C11 = calc.multiply_3vector( ( V6 + V31 + V33 ) , const )
    IcosahedralCentres.append(C11)
    C12 = calc.multiply_3vector( ( V6 + V33 + V17 ) , const )
    IcosahedralCentres.append(C12)

    C13 = calc.multiply_3vector( ( V17 + V33 + V51 ) , const )
    IcosahedralCentres.append(C13)
    C14 = calc.multiply_3vector( ( V17 + V51 + V37 ) , const )
    IcosahedralCentres.append(C14)
    C15 = calc.multiply_3vector( ( V37 + V51 + V54 ) , const )
    IcosahedralCentres.append(C15)
    C16 = calc.multiply_3vector( ( V58 + V54 + V51 ) , const )
    IcosahedralCentres.append(C16)
    C17 = calc.multiply_3vector( ( V58 + V46 + V54 ) , const )
    IcosahedralCentres.append(C17)
    C18 = calc.multiply_3vector( ( V58 + V31 + V46 ) , const )
    IcosahedralCentres.append(C18)

    C19 = calc.multiply_3vector( ( V58 + V33 + V31 ) , const )
    IcosahedralCentres.append(C19)
    C20 = calc.multiply_3vector( ( V58 + V51 + V33 ) , const )
    IcosahedralCentres.append(C20)

    distFromCentre = []
    for entry in IcosahedralCentres:
        distFromCentre.append( ( entry - pointOnSphere ).Mag() )
    face = distFromCentre.index(min(distFromCentre)) + 1
    if face == 1:#{ 2, 6, 17}
        resultPosition = transform_coord( V2, V6, V17, A2a, A6, A17a, pointOnSphere )
    elif face == 2:#{ 2, 12, 6}
        resultPosition = transform_coord( V2, V12, V6, A2a, A12a, A6, pointOnSphere )
    elif face == 3:#{ 2, 17, 37}
        resultPosition = transform_coord( V2, V17, V37, A2b, A17b, A37, pointOnSphere )
    elif face == 4:#{ 2, 37, 27}
        resultPosition = transform_coord( V2, V37, V27, A2b, A37, A27, pointOnSphere )
    elif face == 5:#{ 2, 27, 12}
        resultPosition = transform_coord( V2, V27, V12, A2b, A27, A12e, pointOnSphere )
    elif face == 6:#{37, 54, 27}
        resultPosition = transform_coord( V37, V54, V27, A37, A54, A27, pointOnSphere )
    elif face == 7:#{27, 54, 46}
        resultPosition = transform_coord( V27, V54, V46, A27, A54, A46, pointOnSphere )
    elif face == 8:#{27, 46, 12}
        resultPosition = transform_coord( V27, V46, V12, A27, A46, A12d, pointOnSphere )
    elif face == 9:#{12, 46, 31}
        resultPosition = transform_coord( V12, V46, V31, A12c, A46, A31, pointOnSphere )
    elif face == 10:#{12, 31, 6}
        resultPosition = transform_coord( V12, V31, V6, A12b, A31, A6, pointOnSphere )
    elif face == 11:#{ 6, 31, 33}
        resultPosition = transform_coord( V6, V31, V33, A6, A31, A33, pointOnSphere )
    elif face == 12:#{ 6, 33, 17} 
        resultPosition = transform_coord( V6, V33, V17, A6, A33, A17a, pointOnSphere )
    elif face == 13:#{17, 33, 51}
        resultPosition = transform_coord( V17, V33, V51, A17a, A33, A51a, pointOnSphere )
    elif face == 14:#{17, 51, 37}
        resultPosition = transform_coord( V17, V51, V37, A17b, A51e, A37, pointOnSphere )
    elif face == 15:#{37, 51, 54}
        resultPosition = transform_coord( V37, V51, V54, A37, A51d, A54, pointOnSphere )
    elif face == 16:#{58, 54, 51}
        resultPosition = transform_coord( V58, V54, V51, A58, A54, A51c, pointOnSphere )
    elif face == 17:#{58, 46, 54}
        resultPosition = transform_coord( V58, V46, V54, A58, A46, A54, pointOnSphere )
    elif face == 18:#{58, 31, 46}
        resultPosition = transform_coord( V58, V31, V46, A58, A31, A46, pointOnSphere )
    elif face == 19:#{58, 33, 31}
        resultPosition = transform_coord( V58, V33, V31, A58, A33, A31, pointOnSphere )
    elif face == 20:#{58, 51, 33}
        resultPosition = transform_coord( V58, V51, V33, A58, A51b, A33, pointOnSphere )
    else:
        print "Error cant resolve PMT position!"
        sys.exit(1)
    return ROOT.TVector2(resultPosition.X(),2*resultPosition.Y())

def proj_pmts(run, pmt_hits, xbins = 300, ybins = 300):
    can = ROOT.TCanvas()
    h_proj = ROOT.TH2D("h_proj","NHits",xbins,0,1,ybins,0,1)
    db = db_access.get_rat_db()
    l_pmtx, l_pmty, l_pmtz = db_access.load_pmt_positions(db)
    for lcn in pmt_hits:
        if (l_pmtx[lcn] == 0 and l_pmty[lcn] == 0 and l_pmtz[lcn] == 0):
            print "Error!!! PMT", lcn, "is located at 0, 0, 0??"
            continue
        pmt_pos = ROOT.TVector3(l_pmtx[lcn],l_pmty[lcn],l_pmtz[lcn])
        proj = icos_project(pmt_pos)
        xbin = int((1-proj.X())*xbins)
        ybin = int((1-proj.Y())*ybins)
        bin = h_proj.GetBin(xbin,ybin)
        h_proj.SetBinContent(bin,pmt_hits[lcn])
    h_proj.Draw("colz")
    fname = "../"+run+".pdf"
    can.Print(fname)
    return h_proj

