#!/usr/bin/python
import json
import time
import serial
import time
import math
import sys
from threading import Thread
import pynextion

nextionApp=None

class NextionApp:

    def __init__(self,device):
        ser=serial.Serial(device,9600,timeout=0)
        ser.flushOutput()
        pages=[
		{ 'id':'0', 'name':'boatSpeed',
			'components':[
				{'id':'t1','type':'text','name':'boatSpeedValue'},
				{'id':'t2','type':'text','name':'boatSpeedAttr'},
				{'id':'t3','type':'text','name':'boatSpeedUnit'},
				{'id':'b0','type':'button','name':'buttonPrev'},
				{'id':'b1','type':'button','name':'puttonNext'},
			]
		},
		{ 'id':'1', 'name':'boatHeading',
			'components':[
                		{'id':'t1','type':'text','name':'boatHeadingValue'},
                        	{'id':'t3','type':'text','name':'boatHeadingTrueMag'},
                                {'id':'b0','type':'button','name':'buttonPrev'},
                                {'id':'b1','type':'button','name':'puttonNext'},
                        ]
                },
		{ 'id':'2', 'name':'windSpeed',
			'components':[
                		{'id':'t1','type':'text','name':'windSpeedValue'},
                        	{'id':'t2','type':'text','name':'windSpeedTrueApp'},
                        	{'id':'t3','type':'text','name':'windSpeedUnit'},
                                {'id':'b0','type':'button','name':'buttonPrev'},
                                {'id':'b1','type':'button','name':'puttonNext'},
                        ]
                },
		{ 'id':'3','name':'windDir',
			'components':[
				{'id':'z0','type':'gauge','name':'windAngleValue'},
                                {'id':'b0','type':'button','name':'buttonPrev'},
                                {'id':'b1','type':'button','name':'puttonNext'},
                        ]
		}
	]
        self.nextion=pynextion.Nextion(ser,pages)
        print 'Serial connected'

    def update(self):
	print "Getting initial page id"
        pageId=self.nextion.getPage()
        print "Page id:"+str(pageId)
        s="n/a"

        if pageId==0:
            #try:
                speedThroughWater=3.2
                value=float(speedThroughWater)*1.94
                s="%.2f" % value
		self.nextion.pageByName('boatSpeed').componentByName('boatSpeedValue').set(s)
            #except:
            #    pass

        elif pageId==1:
            try:
                headingTrue=303.2
                value=float(headingTrue)
                s="%.0f" % value
		self.nextion.pageByName('boatHeading').componentByName('boatHeadingValue').set(s)
            except:
                pass

        elif pageId==2:
            try:
                windSpeedTrue=10.11
                value=float(windSpeedTrue)*1.94
                s="%.1f" % value
		self.nextion.pageByName('windSpeed').componentByName('windSpeedValue').set(s)
            except:
                pass
        elif pageId==3:
            try:
                windAngleValue=45
                value=float(windAngleValue)+90
		if value>360: value-=90
                s="%.0f" % value
		self.nextion.pageByName('windDir').componentByName('windAngleValue').set(s)
            except:
                pass
        


        print s
        #self.nextion.setText('t1',s)

    def run(self):
	if nextionApp is not None:
	    nextionApp.update()
	pass


if __name__ == "__main__":

    nextionApp=NextionApp("/dev/tty.SLAB_USBtoUART")
    nextionApp.run()
