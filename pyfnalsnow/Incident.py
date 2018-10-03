"""
pyfnalsnow.Incident - parse Incident objects.  These are pretty much the
"default"
"""

#########################################################################
### Declarations ########################################################
#########################################################################

import pyfnalsnow

from pyfnalsnow.ticket import tktStringAssignee
from pyfnalsnow.ticket import tktStringAudit
from pyfnalsnow.ticket import tktStringBase
from pyfnalsnow.ticket import tktStringBaseAudit
from pyfnalsnow.ticket import tktStringDebug
from pyfnalsnow.ticket import tktStringDescription
from pyfnalsnow.ticket import tktStringJournal
from pyfnalsnow.ticket import tktStringPrimary
from pyfnalsnow.ticket import tktStringRequestor
# from pyfnalsnow.ticket import tktStringResolution
from pyfnalsnow.ticket import tktStringShort
from pyfnalsnow.ticket import tktStringSummary

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

resolve_code = 'Other (must describe below)'

#########################################################################
### Subroutines #########################################################
#########################################################################

def tktFilter(status='open', **args):
    """
    Filter tickets.
    """

    extra = []
    if status.lower() == 'open':
        extra.append('incident_state<4')
        extra.append('stage!=complete')
        extra.append('stage!=Complete')
        extra.append('stage!=Request Cancelled')
    elif status.lower() == 'closed':
        extra.append('incident_state>=4')
    elif status.lower() == 'unresolved':
        extra.append('incident_state<6')

    if 'unassigned' in args:
        extra.append('assigned_to=NULL')

    if 'group' in args:
        group = pyfnalsnow.groupByName(args['group'])
        extra.append('assignment_group=%s' % group['sys_id'])

    if 'assigned' in args:
        user = pyfnalsnow.userByUsername(args['assigned'])
        extra.append('assigned_to=%s' % user['sys_id'])

    if 'submit' in args:
        user = pyfnalsnow.userByUsername(args['submit'])
        extra.append('sys_created_by=%s' % user['user_name'])

    search='^'.join(extra)

    return search

def tktIsResolved(tkt):
    if int(tkt['incident_state']) >= 4: return True
    else:                               return False

def tktPending(tkt, **kwargs):
    """
    Set an incident to status 'pending'.  This isn't *really* a thing for
    Incidents, though.

    kwargs:
      reason    String; default is 'Customer'
    """

    try:    reason = kwargs['reason']
    except: reason = 'Customer'

    new = { 'u_pending_reason': reason }
    return pyfnalsnow.tktUpdate(tkt['number'], new)

def tktStringResolution(tkt):
    """
    """
    extra = {}
    ret = []
    ret.append("Resolution")
    resolvedBy = pyfnalsnow.userLinkName(tkt['resolved_by'])
    ret.extend(pyfnalsnow.ticket.formatTextField('Resolved By', resolvedBy,  **extra))
    ret.extend(pyfnalsnow.ticket.formatTextField('Date', tkt['resolved_at'], **extra))
    ret.append('')
    ret.extend(pyfnalsnow.ticket.formatText(tkt['close_notes']), **extra)
    ret.append('')

    return ret

def tktResolve(tkt, update, **kwargs):
    """
    Resolve an incident.  Set the state to 6, the resolution code to
    something known, and the text and user fields come from the 'update'
    hash.
    """

    new = {
        'close_code': resolve_code,
        'close_notes': update['text'],
        'incident_state': 6,
        'resolved_by': update['user']
    }

    return pyfnalsnow.tktUpdate(tkt['number'], new)
