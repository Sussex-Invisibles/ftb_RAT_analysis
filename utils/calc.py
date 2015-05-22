import math
import ROOT
import numpy as np

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

#def fibre_pmt_theta_phi(fibre_pos, pmt_pos):
#    """ Calculate the theta and phi angle between emission an detection positions
#    
#    :param fibre_pos (RAT::DBLink object): Position of TELLIE fibre active in event.
#    :param pmt_pos (ROOT.TVector3): Position of active PMT. 
#    :return theta (float): Theta angle between fibre and pmt in degrees.
#    :return phi (float): Phi angle between fibre and pmt in degrees.
#    """
#    f_x, f_y, f_z = fibre_pos.GetD("x"), fibre_pos.GetD("y"), fibre_pos.GetD("z")
#    p_x, p_y, p_z = pmt_pos[0], pmt_pos[1], pmt_pos[2]
#    x, y, z = (p_x - f_x), (p_y - f_z), (p_z - f_z)
#    r = np.sqrt( x**2 + y**2 + z**2)
#    theta = np.arctan( y/x ) * 180/np.pi
#    phi = np.arctan( np.sqrt(x**2 + y**2)/z) * 180/np.pi
#    return theta, phi

def fibre_pmt_theta_phi(fibre_pos, pmt_pos):
    """ Calculate the theta and phi angle between emission an detection positions

    :param fibre_pos (RAT::DBLink object): Position of TELLIE fibre active in event.
    :param pmt_pos (ROOT.TVector3): Position of active PMT.
    :return theta (float): Theta angle between fibre and pmt in degrees.
    :return phi (float): Phi angle between fibre and pmt in degrees.
    """
    fibre_3vec = ROOT.TVector3(fibre_pos.GetD("x"), fibre_pos.GetD("y"), fibre_pos.GetD("z"))
    final_vec = pmt_pos - fibre_3vec 
    return final_vec.Theta()*(180/np.pi), final_vec.Phi()*(180/np.pi)

def time_diff_50MHz(start, stop):
    """Retrun the time difference in seconds between two 50MHz clock readings

    :param start: Initial clock reading
    :param stop : Final clock reading
    :return time differnce [s]
    """
    return (stop-start)*2e-8

def weighted_avg_and_std(values, weights):
    """Return the weighted average and standard deviation.

    :param values (list): List of values to be averaged
    :param weights (list): List of wieght to be considered in average
    :return average (float): Weighted average of values and weights
    :return stdev (float): Weighted standard deviation of values and weights
    """
    average = np.average(values, weights=weights)
    variance = np.average((values-average)**2, weights=weights)  # Fast and numerically precise
    return average, np.sqrt(variance)

def corr_coef(x_arr, y_arr):
    """Calculate the correlation coefficient of an (x,y) data set

    :param x_array (list): Array containing the x data set
    :param y_array (list): Array containing the y data set
    :return: correlation coefficient of the (x,y) data set
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
