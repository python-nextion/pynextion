import serial
import sys
import time
from threading import Thread

class Page(object):
  def __init__(self, nextion,id):
    self.nextion=nextion
    self.id=id
    self.controls=[]

  def hookText(self,id,value=None):
    control=Text(self,id,value)
    self.controls.append(control)
    return control

  def show(self):
    self.nextion.setPage(self.id)


class Control(object):

  def __init__(self,page,id):
    self.page=page
    self.id=id

class Text(Control):

  def __init__(self,page,id,value=None):
    super(Text, self).__init__(page,id)
    if value is not None:
      self.page.nextion.setText(self.id,value)

  def get(self):
    return self.page.nextion.getText(self.id)

  def set(self,value):
    self.page.nextion.setText(self.id,value)
    
class Nextion(object):

  ERRORS={
    "00": "Invalid instruction",
    "01": "Successful execution of instruction",
    "03": "Page ID invalid",
    "04": "Picture ID invalid",
    "05": "Font ID invalid",
    "11": "Baud rate setting invalid",
    "12": "Curve control ID number or channel number is invalid",
    "1a": "Variable name invalid",
    "1b": "Variable operation invalid"
  }

  MESSAGES={
    "65": "Touch event return data",
    "66": "Current page ID number returns"
  }

  RED   =63488	
  BLUE  =31	
  GRAY  =33840	
  BLACK =0	
  WHITE =65535	
  GREEN =2016	
  BROWN =48192
  YELLOW=65504

  def __init__(self,ser):
    self.pages = []
    self.debug = False
    self.ser = ser
    while True:
      try:
        self.setBkCmd(3)
        break
      except:
        print "Wait..."
        time.sleep(1)

  def hookPage(self,id):
    page=Page(self,id)
    self.pages.append(page)
    return page

  def setDebug(self,debug):
    self.debug=debug

  def setBkCmd(self,value):
    self.set('bkcmd',value)

  def setDim(self,value):
    self.set('dim',value)

  def setDim(self,value):
    self.set('dims',value)

  def setPage(self,value):
    s=self.nxWrite('page '+str(value))
    if s[0]!=0x01:
      raise ValueError(Nextion.getErrorMessage(s[0])+": page "+str(value))

  def getPage(self):
    self.ser.flushOutput()
    s=self.nxWrite('sendme')
    if s[0]==0x66:
        if s[1]==0xff: s[1]=0x00
        return s[1]

    raise ValueError(Nextion.getErrorMessage(0x00))

###############################

  def refresh(self,id="0"):
    s=self.nxWrite('ref %s' % id)
    if s[0]!=0x01:
      raise ValueError(Nextion.getErrorMessage(s[0]))

  def getText(self,id):
    s=self.nxWrite('get %s.txt' % id)
    if s[0]!=0x01:
      raise ValueError(Nextion.getErrorMessage(s[0]))

  def getValue(self,id):
    s=self.nxWrite('get %s.val' % id)
    if s[0]!=0x01:
      raise ValueError(Nextion.getErrorMessage(s[0]))

###############################

  def setText(self,id,value):
    s=self.nxWrite(id+'.txt="'+str(value)+'"')
    if s[0]!=0x01:
      raise ValueError(Nextion.getErrorMessage(s[0])+": id: "+id+" text:"+ value)

  def clear(self,color):
    s=self.nxWrite('cls %s' % color);
    if s[0]!=0x01:
      raise ValueError(Nextion.getErrorMessage(s[0]))

  def drawPicture(self,x,y,pic,w=None,h=None):
    if w is None or h is None:
      s=self.nxWrite('pic %s,%s,%s' % (x,y,pic))
    else:
      s=self.nxWrite('picq %s,%s,%s,%s,%s,%s' %(x,y,pic,w,h))
    if s[0]!=0x01:
      raise ValueError(Nextion.getErrorMessage(s[0]))

  def drawString(self,x1,y1,x2,y2,fontid,fontcolor,backcolor,xcenter,ycenter,sta,string):
    s=self.nxWrite('xstr %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (x1,y1,x2-x1,y2-y1,fontid,fontcolor,backcolor,xcenter,ycenter,sta,string))
    if s[0]!=0x01:
      raise ValueError(Nextion.getErrorMessage(s[0]))

  def drawLine(self,x1,y1,x2,y2,color):
    s=self.nxWrite('line %s,%s,%s,%s,%s' % (x1,y1,x2,y2,color))
    if s[0]!=0x01:
      raise ValueError(Nextion.getErrorMessage(s[0]))

  def drawRectangle(self,x1,y1,x2,y2,color):
    s=self.nxWrite('draw %s,%s,%s,%s,%s' % (x1,y1,x2,y2,color))
    if s[0]!=0x01:
      raise ValueError(Nextion.getErrorMessage(s[0]))

  def drawBox(self,x1,y1,x2,y2,color):
    s=self.nxWrite('fill %s,%s,%s,%s,%s' % (x1,y1,x2-x1,y2-y1,color))
    if s[0]!=0x01:
      raise ValueError(Nextion.getErrorMessage(s[0]))

  def drawCircle(self,x,y,r,color):
    s=self.nxWrite('cir %s,%s,%s,%s' % (x,y,r,color))
    if s[0]!=0x01:
      raise ValueError(Nextion.getErrorMessage(s[0]))

##############################
  def set(self,key,value):
    s=self.nxWrite(key+'='+str(value))
    if s[0]!=0x01:
      raise ValueError(Nextion.getErrorMessage(s[0])+": "+key+"="+str(value))
    

  @staticmethod
  def getErrorMessage(s):
     return Nextion.ERRORS[format(s, '02x')]

  def nxWrite(self,s):
    self.ser.write(s)
    self.ser.write(chr(255))
    self.ser.write(chr(255))
    self.ser.write(chr(255))
    return self.nxRead()

  def nxRead(self,cmax=0,timeout=0):
    s=[]
    done=False
    def _reader():
      count=0
      time_now = time.clock()
      while timeout==0 or (time.clock()-time_now)<timeout:
        r = self.ser.read()
        if r is None or r=="":
          continue

        c = ord(r)
        if c==0xff and len(s)==0:
          continue

        if c!=0x00:        
          if self.debug is True:
            print "\/ :"+str(c)+":"+str(len(s))+":"+str(count)

          s.append(c)
          if len(s)==cmax:
            return
          if c==0xff:
            count=count+1
            if count==3:
              if self.debug is True:
                print "!!"
              return
          else:
            count=0
          if self.debug is True:
            print "/\ :"+str(c)+":"+str(len(s))+":"+str(count)
      print "Timeout"

    t = Thread(target=_reader)
    t.start()
    t.join()
    return s 

if __name__ == "__main__":
  #ser=serial.Serial('/dev/ttyMCC',9600,timeout=0)
  ser=serial.Serial('/dev/tty.SLAB_USBtoUART',9600,timeout=0)
  ser.flushOutput()
  nextion=Nextion(ser)
  print 'Serial connected'
  #nextion.setDim(50)
  #for p in range(0,3):
  #  nextion.setPage(p)
  #  nextion.setText('t0',"Fede<3")
  #  print nextion.getPage()
  #nextion.setDim(100)

  pageBoatSpeed=nextion.hookPage(0)
  pageHeading=nextion.hookPage(1)
  pageWindSpeed=nextion.hookPage(2)

  txtBoatSpeedValue=pageBoatSpeed.hookText("t1")
  txtBoatSpeedAttr=pageBoatSpeed.hookText("t2")
  txtBoatSpeedUnit=pageBoatSpeed.hookText("t3")

  txtHeadingValue=pageBoatSpeed.hookText("t1")
  txtHeadingTrueMag=pageBoatSpeed.hookText("t3")

  txtWindSpeedValue=pageWindSpeed.hookText("t1")
  txtWindSpeedTrueApp=pageWindSpeed.hookText("t2")
  txtWindSpeedUnit=pageWindSpeed.hookText("t3")

  pageBoatSpeed.show()
  txtBoatSpeedValue.set(2.2)
  pageHeading.show()
  txtHeadingValue.set(300)
  pageWindSpeed.show()
  txtWindSpeedValue.set(3.75)

  nextion.clear(Nextion.RED)
  nextion.drawBox(0,0,100,100,Nextion.BLUE)
  nextion.drawRectangle(0,0,100,100,Nextion.YELLOW)
  nextion.drawLine(0,0,100,100,Nextion.GREEN)
  nextion.drawCircle(100,100,50,Nextion.BROWN)
  #nextion.drawString(0,0,400,200,2,4096,3072,1,1,1,"*")

  pageBoatSpeed.show()
  txtBoatSpeedValue.set("Fede<3")
