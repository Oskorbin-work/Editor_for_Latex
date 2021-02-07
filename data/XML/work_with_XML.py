import xml.etree.ElementTree as ET
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
root = ET.parse(os.path.join(ROOT_DIR,'conf.xml')).getroot()

def get_attr_XML(name):
    return root.find(name).text