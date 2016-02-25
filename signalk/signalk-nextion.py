#!/usr/bin/python
import websocket
import json
import time
import serial
import time
import math
import sys
from threading import Thread
import pynextion

#url="ws://localhost:3000/signalk/v1/stream?stream=delta"
#url="ws://demo.signalk.org/signalk/v1/stream?stream=delta"
#self_uuid="urn:mrn:signalk:uuid:c0d79334-4e25-4245-8892-54e8ccc8021d"

signalkRepeater=None

class SignalKRepeater:

    def __init__(self,device,url,uuid):
	self.model={}
	self.url=url
	self.uuid=uuid
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
				{'id':'t0','type':'text','name':'windSpeedValue'},
				{'id':'t1','type':'text','name':'boatSpeedValue'},
				{'id':'t2','type':'text','name':'boatHeadingValue'},
                                {'id':'z0','type':'gauge','name':'windAngleValue'},
                                {'id':'m0','type':'hotspot','name':'hotspotPrev'},
                                {'id':'m1','type':'hotspot','name':'hotspotNext'},
                        ]
                },
		{ 'id':'4','name':'depth',
                        'components':[
                                {'id':'t1','type':'text','name':'depthValue'},
                                {'id':'s0','type':'waveform','name':'depthWaveForm'},
                                {'id':'b0','type':'button','name':'buttonPrev'},
                                {'id':'b1','type':'button','name':'puttonNext'},
                        ]
                }
        ]
        self.nextion=pynextion.Nextion(ser,pages)
        print 'Serial connected'

    @staticmethod
    def on_message(ws, message):
        #print str(message)
        if signalkRepeater is not None:
            signalkRepeater.onMessage(message)

    @staticmethod
    def on_error(ws, error):
        print error

    @staticmethod
    def on_close(ws):
        print "### closed ###"

    @staticmethod
    def on_open(ws):
        print "### open ###"  

    def onMessage(self,message):
        jsonMessage=json.loads(message)
        try:
            context=jsonMessage['context']
            updates=jsonMessage['updates']
            for update in updates:
                values=update['values']
                for value in values:
                    path=value['path']
                    key=context+"."+path
                    if "navigation.position" in path:
                        self.model.update({key+".latitude":value['value']['latitude']})
                        self.model.update({key+".longitude":value['value']['longitude']})
                    else:
                        value=value['value']
                        self.model.update({key:value})
            self.update()
        except:
            e = sys.exc_info()[0]
            print "-->"+str(e)+"<--"

    def update(self):
	print "Getting initial page id"
        pageId=self.nextion.getPage()
        print "Page id:"+str(pageId)

        if pageId==0:
                speedThroughWater=self.model['vessels.'+self.uuid+'.navigation.speedThroughWater']
                value=float(speedThroughWater)*1.94
                s="%.2f" % value
		self.nextion.pageByName('boatSpeed').componentByName('boatSpeedValue').set(s)

        elif pageId==1:
                headingTrue=self.model['vessels.'+self.uuid+'.navigation.headingTrue']
                value=float(headingTrue)
                s="%.0f" % value
		self.nextion.pageByName('boatHeading').componentByName('boatHeadingValue').set(s)

        elif pageId==2:
                windSpeedTrue=self.model['vessels.'+self.uuid+'.environment.wind.speedTrue']
                value=float(windSpeedTrue)*1.94
                s="%.1f" % value
		self.nextion.pageByName('windSpeed').componentByName('windSpeedValue').set(s)
        elif pageId==3:
		speedThroughWater=round(float(self.model['vessels.'+self.uuid+'.navigation.speedThroughWater'])*1.94,1)
		headingTrue=round(float(self.model['vessels.'+self.uuid+'.navigation.headingTrue']),0)
                windSpeedValue=round(float(self.model['vessels.'+self.uuid+'.environment.wind.speedApparent'])*1.94,1)
                windAngleValue=float(self.model['vessels.'+self.uuid+'.environment.wind.angleApparent'])*57.2958
		windAngleValue+=90
		if windAngleValue<0: windAngleValue+=360
		windAngleValue=int(round(windAngleValue,0))
		self.nextion.pageByName('windDir').componentByName('windSpeedValue').set(windSpeedValue)
		self.nextion.pageByName('windDir').componentByName('windAngleValue').set(windAngleValue)
		print "_______"
		print str(self.nextion.pageByName('windDir').componentByName('boatSpeedValue').id)
		self.nextion.pageByName('windDir').componentByName('boatSpeedValue').set(boatSpeedValue)
		print "-------"
		#self.nextion.pageByName('windDir').componentByName('boatHeadingValue').set(boatHeadingValue)
	elif pageId==4:
		depthValue=round(float(self.model['vessels.'+self.uuid+'.environment.depth.belowTransducer']),1)
		self.nextion.pageByName('depth').componentByName('depthValue').set(depthValue)
		depthValue=int(round(depthValue,0))
		self.nextion.pageByName('depth').componentByName('depthWaveForm').add(0,depthValue)
        

    def run(self):
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(self.url,
                                on_message = self.on_message,
                                on_error = self.on_error,
                                on_close = self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()


if __name__ == "__main__":

    signalkRepeater=SignalKRepeater("/dev/tty.SLAB_USBtoUART","ws://web.uniparthenope.it:3000/signalk/v1/stream?stream=delta","urn:mrn:signalk:uuid:821b52be-bfdc-11e5-9912-ba0be0483c18")
    signalkRepeater.run()
