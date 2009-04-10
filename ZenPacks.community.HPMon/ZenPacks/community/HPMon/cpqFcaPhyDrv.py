################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""cpqFcaPhyDrv

cpqFcaPhyDrv is an abstraction of a HP FCA Hard Disk.

$Id: cpqFcaPhyDrv.py,v 1.0 2009/03/10 14:45:24 egor Exp $"""

__version__ = "$Revision: 1.0 $"[11:-2]

from Globals import InitializeClass
from ZenPacks.community.HPMon.HPHardDisk import HPHardDisk

class cpqFcaPhyDrv(HPHardDisk):
    """cpqFcaPhyDrv object
    statusmap(statusDot, statusSeveriry, statusString)
    statusDot(0:'green', 1:'yellow', 2:'orange', 3:'red', 4:'grey')
    statusSeverity(0:'Clean', 1:'Debug', 2:'Info', 3:'Warning', 4:'Error', 5:'Critical')
    """

    portal_type = meta_type = 'cpqFcaPhyDrv'

    chassis = ""
    busNumber = 1
    external = False
    
    _properties = HPHardDisk._properties + (
                    {'id':'chassis', 'type':'string', 'mode':'w'},
                    {'id':'busNumber', 'type':'int', 'mode':'w'},
                    {'id':'external', 'type':'boolean', 'mode':'w'},
                )    

    statusmap = [(4, 3, 'other'),
                (4, 3, 'other'),
		(1, 3, 'Not Configured'),
		(0, 0, 'Ok'),
		(2, 4, 'Threshold Exceeded'),
		(2, 4, 'Predictive Failure'),
		(3, 5, 'Failed'),
		(3, 5, 'Unsupported Drive'),
		]

InitializeClass(cpqFcaPhyDrv)
