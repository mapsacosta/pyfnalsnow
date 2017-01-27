""" 
pyfnalsnow.Incident
"""

#########################################################################
### Declarations ########################################################
#########################################################################

from pyfnalsnow.ticket import tktStringBase

#########################################################################
### Configuration #######################################################
#########################################################################

state = {
    '1': 'Assigned',
    '2': 'Work In Progress',
    '6': 'Resolved',
    '7': 'Closed',
    '8': 'Cancelled'
}

#########################################################################
### Subroutines #########################################################
#########################################################################

def tktIsResolved(tkt):
    if tktState(tkt) >= 4: return True
    else:                  return False
