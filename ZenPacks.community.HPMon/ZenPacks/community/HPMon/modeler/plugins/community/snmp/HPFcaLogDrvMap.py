################################################################################
#
# This program is part of the HPMon Zenpack for Zenoss.
# Copyright (C) 2008 Egor Puzanov.
#
# This program can be used under the GNU General Public License version 2
# You can find full information here: http://www.zenoss.com/oss
#
################################################################################

__doc__="""HPFcaLogDrvMap

HPFcaLogDrvMap maps the cpqFcaLogDrvTable to disks objects

$Id: HPFcaLogDrvMap.py,v 1.0 2008/11/13 12:20:53 egor Exp $"""

__version__ = '$Revision: 1.0 $'[11:-2]

from Products.DataCollector.plugins.CollectorPlugin import GetTableMap
from HPHardDiskMap import HPHardDiskMap

class HPFcaLogDrvMap(HPHardDiskMap):
    """Map HP/Compaq insight manager FCA Logical Disk tables to model."""

    maptype = "HPFcaLogDrvMap"
    modname = "ZenPacks.community.HPMon.cpqFcaLogDrv"

    snmpGetTableMaps = (
        GetTableMap('cpqFcaLogDrvTable',
	            '.1.3.6.1.4.1.232.16.2.3.1.1',
		    {
		        '.1': 'chassis',
			'.2': 'snmpindex',
			'.3': 'diskType',
			'.4': 'status',
			'.9': 'size',
			'.12': 'stripesize',
			'.13': 'description',
		    }
	),
        GetTableMap('cpqSsChassisTable',
	            '.1.3.6.1.4.1.232.8.2.2.1.1',
		    {
			'.1': 'snmpindex',
			'.4': 'name',
		    }
	),
    )

    diskTypes = {1: 'other',
		2: 'RAID0',
		3: 'RAID1',
		4: 'RAID4',
		5: 'RAID5',
		6: 'RAID1E',
		7: 'RAID ADG',
		}

    def process(self, device, results, log):
        """collect snmp information from this device"""
        log.info('processing %s for device %s', self.name(), device.id)
        getdata, tabledata = results
	disktable = tabledata.get('cpqFcaLogDrvTable')
        chassismap = {}
	chassistable = tabledata.get('cpqSsChassisTable')
	for chassis in chassistable.values():
	    chassismap[chassis['snmpindex']] = chassis['name']
	external = 'community.snmp.HPSsChassisMap' in getattr(device, 'zCollectorPlugins', [])
	if not device.id in HPHardDiskMap.oms:
	    HPHardDiskMap.oms[device.id] = []
        for disk in disktable.values():
            try:
                om = self.objectMap(disk)
		om.snmpindex =  "%d.%d" % (om.chassis, om.snmpindex)
                om.id = self.prepId("LogicalDisk%s" % om.snmpindex).replace('.', '_')
		om.diskType = self.diskTypes.get(getattr(om, 'diskType', 1), '%s (%d)' %(self.diskTypes[1], om.diskType))
		om.stripesize = "%d" % (getattr(om, 'stripesize', 0) * 1024)
		om.size = "%d" % (getattr(om, 'size', 0) * 1048576)
		om.chassis = chassismap.get(om.chassis, '')
		om.external = external
            except AttributeError:
                continue
            HPHardDiskMap.oms[device.id].append(om)
	return
