import xml.etree.ElementTree as ET
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_attr_XML(name):
    root_conf = ET.parse(os.path.join(ROOT_DIR, 'conf.xml')).getroot()
    return root_conf.find(name).text

def get_osnova_XML(name):
    root_osnova = ET.parse(os.path.join(ROOT_DIR, 'osnova.xml')).getroot()
    return root_osnova.find(name).text

def change_val_XML(name_file_XML, val,new_val):
     root_change = ET.parse(os.path.join(ROOT_DIR, name_file_XML +'.xml'))
     for t in root_change.iterfind(val):
         t.text = new_val
     root_change.write(os.path.join(ROOT_DIR, name_file_XML +'.xml'),encoding="UTF-8",xml_declaration=True)