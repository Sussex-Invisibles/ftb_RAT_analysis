import math
import ROOT

def solve_quad(a,b,c):
    """ Solves quadratic equations and returns the solutions (sol)
    """
    sol_1 = (-b+math.sqrt(b*b-4*a*c))/(2*a)
    sol_2 = (-b-math.sqrt(b*b-4*a*c))/(2*a)
    return sol_1, sol_2


def get_incident_photon(pos,direc,psup_radius = 8406.75):
    """ Calculates the position of the incident light (0 degrees) on the 
    opposite side of the psup. 8406.75 mm is the average psup radius.
    """
    a = math.pow(direc.X(),2)+math.pow(direc.Y(),2)+math.pow(direc.Z(),2)
    b = 2*(direc.X()*pos.X()+direc.Y()*pos.Y()+direc.Z()*pos.Z())
    c = math.pow(pos.X(),2)+math.pow(pos.Y(),2)+math.pow(pos.Z(),2)-math.pow(psup_radius,2)
    r_1, r_2 = solve_quad(a,b,c)
    if (math.fabs(r_1) > 10000):
        incident_photon = ROOT.TVector3(pos.X()+r_1*direc.X(),pos.Y()+r_1*direc.Y(),pos.Z()+r_1*direc.Z())
    elif (math.fabs(r_2) > 10000):
        incident_photon = ROOT.TVector3(pos.X()+r_2*direc.X(),pos.Y()+r_2*direc.Y(),pos.Z()+r_2*direc.Z())
    else:
        print "ERROR! No solution gives a position on the opposite side of the PSUP!"
        sys.exit(1)
    return incident_photon

def get_x_to_y(x,y):
    """ Calculates the vector from x to y
    """
    return ROOT.TVector3(y.X()-x.X(),y.Y()-x.Y(),y.Z()-x.Z())


def get_angle(a,b,c):
    """ Uses cosine rule to get angle oposite a
    """
    return math.acos((b.Mag()*b.Mag()+c.Mag()*c.Mag()-a.Mag()*a.Mag())/(2*b.Mag()*c.Mag()))

def get_pois(lamda,k):
    return math.pow(lamda,k)*math.exp(-lamda)/math.factorial(k)

def multiply_3vector(V,c):
    ''' Multiply TVectors by a constant because pyroot is stupid
    '''
    return ROOT.TVector3(V.X()*c,V.Y()*c,V.Z()*c)

def multiply_2vector(V,c):
    ''' Multiply TVectors by a constant because pyroot is stupid
    '''
    return ROOT.TVector2(V.X()*c,V.Y()*c)
