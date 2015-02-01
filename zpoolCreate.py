__author__ = 'echoecho'
## script vDevs dataDrives parityDrives sizeDrives

#!/usr/bin/python2.7
from random import shuffle
import subprocess
import sys
import os

# put this information into command line argv
poolName = "testest"
vDevs = 3
dataDrives = 1
parityDrives = 0
driveSize = "Virtual.*10.00GB"

#these are global variables that are needed for the script
zpoolDrives = ""
zpoolLayout = "zpool create " + poolName + " "
systemDrives=subprocess.check_output("format < /dev/null  | grep " + driveSize + " | awk '{ print $2 }'", shell=True).splitlines()

shuffle(systemDrives)

if (vDevs * (dataDrives + parityDrives) > len(systemDrives)):
   print "too big"
   print "systemDrives is ", len(systemDrives)
   print "requested drives is ", (vDevs * (dataDrives + parityDrives))
   sys.exit()

if parityDrives == 0:
        if (vDevs * (dataDrives + 1) > len(systemDrives)):
            print "too big"
            print "systemDrives is ", len(systemDrives)
            print "requested drives is ", (vDevs * (dataDrives + parityDrives))
            sys.exit()

        for i in range(0, vDevs):
                for j in range(0, dataDrives + 1):
                        zpoolDrives = zpoolDrives + systemDrives[0] + " "
                        systemDrives.pop(0)
                zpoolLayout = zpoolLayout + "mirror " + zpoolDrives
                zpoolDrives = ""
elif parityDrives < 4:
        if (vDevs * (dataDrives + parityDrives) > len(systemDrives)):
           print "too big"
           print "systemDrives is ", len(systemDrives)
           print "requested drives is ", (vDevs * (dataDrives + parityDrives))
           sys.exit()

        for i in range(0, vDevs):
                for j in range(0, dataDrives + parityDrives):
                        zpoolDrives = zpoolDrives + systemDrives[0] + " "
                        systemDrives.pop(0)
                zpoolLayout = zpoolLayout + "raidz" + str(parityDrives) + " " + zpoolDrives
                zpoolDrives = ""
else:
        print "Too many parity drives"
        sys.exit()

print zpoolLayout
os.system(zpoolLayout)
os.system("zpool status")