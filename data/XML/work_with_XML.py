import xml.etree.ElementTree as ET
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
root_conf = ET.parse(os.path.join(ROOT_DIR,'conf.xml')).getroot()
root_osnova = ET.parse(os.path.join(ROOT_DIR,'osnova.xml')).getroot()
def get_attr_XML(name):
    return root_conf.find(name).text

def get_osnova_XML(name):
    return root_osnova.find(name).text