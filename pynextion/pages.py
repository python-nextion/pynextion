import serial
import sys
import time
from threading import Thread
import pynextion
from components import Component

class Page(object):
  def __init__(self, nextion,id):
    self.components=[]
    self.id=id
    self.name=None
    self.nextion=nextion

  @staticmethod
  def newPageByDefinition(nextion,pageDefinition):
    page=Page(nextion,pageDefinition['id'])
    page.name=pageDefinition['name']
    if pageDefinition['components'] is not None:
        for componentDefinition in pageDefinition['components']:
          page.components.append(Component.newComponentByDefinition(page,componentDefinition))
    return page
    
  
  def componentByName(self,name):
    result=None
    for component in self.components:
      if name == component.name:
        result=component
        break
    return result

  def hookText(self,id,value=None):
    component=Text(self,id,value)
    self.components.append(component)
    return control

  def show(self):
    self.nextion.setPage(self.id)
