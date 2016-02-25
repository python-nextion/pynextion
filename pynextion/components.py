import serial
import sys
import time
from threading import Thread
import pynextion

class Component(object):

  def __init__(self,page,id,name):
    self.page=page
    self.id=id
    self.name=name

  @staticmethod
  def newComponentByDefinition(page, componentDefinition):
    type=componentDefinition['type']
    id=componentDefinition['id']
    name=None
    name=componentDefinition['name']
    value=None
    try:
      value=componentDefinition['value']
    except KeyError:
      pass

    if "text" in type:
      return Text(page,id,name,value)
    elif "number" in type:
      return Number(page,id,name,value)
    elif "button" in type:
      return Button(page,id,name,value)
    elif "gauge" in type:
      return Gauge(page,id,name,value)
    elif "hotspot" in type:
      return HotSpot(page,id,name)
    elif "waveform" in type:
      return WaveForm(page,id,name)
    
    return None

class Text(Component):

  def __init__(self,page,id,name=None,value=None):
    super(Text, self).__init__(page,id,name)
    if value is not None:
      self.page.nextion.setText(self.id,value)

  def get(self):
    return self.page.nextion.getText(self.id)

  def set(self,value):
    self.page.nextion.setText(self.id,value)

class Number(Component):

  def __init__(self,page,id,name=None,value=None):
    super(Number, self).__init__(page,id,name)
    if value is not None:
      self.page.nextion.setValue(self.id,value)

  def get(self):
    return self.page.nextion.getValue(self.id)

  def set(self,value):
    self.page.nextion.setValue(self.id,value)

class Button(Component):

  def __init__(self,page,id,name=None,value=None):
    super(Button, self).__init__(page,id,name)
    if value is not None:
      self.page.nextion.setText(self.id,value)

  def get(self):
    return self.page.nextion.getText(self.id)

  def set(self,value):
    self.page.nextion.setText(self.id,value)

class HotSpot(Component):

  def __init__(self,page,id,name=None):
    super(HotSpot, self).__init__(page,id,name)

class WaveForm(Component):

  def __init__(self,page,id,name=None):
    super(WaveForm, self).__init__(page,id,name)

  def add(self,channel, value):
    print str(self.id)+":"+str(channel)+" => "+str(value)
    self.page.nextion.nxWrite("add " + self.id + "," + channel + "," + value)

class Gauge(Component):

  def __init__(self,page,id,name=None,value=None):
    super(Gauge, self).__init__(page,id,name)
    if value is not None:
      self.page.nextion.setValue(self.id,value)

  def get(self):
    return self.page.nextion.getValue(self.id)

  def set(self,value):
    self.page.nextion.setValue(self.id,value)
    
