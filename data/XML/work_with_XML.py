# -----------------------------------------------------------
# Work with XML-file
# -----------------------------------------------------------
import xml.etree.ElementTree as ET
# -----------------------------------------------------------
# Other library
# -----------------------------------------------------------
import os
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_attr_XML(name):
    try:
        root_conf = ET.parse(os.path.join(ROOT_DIR, 'conf.xml')).getroot()
    except Exception:
        return "conf.xml має помилки або не існує "
    if root_conf.find(name) is not None:
        return root_conf.find(name).text
    else:
        return " Тег " + name + " не існує в файлі conf.xml"

def get_osnova_XML(name):
    try:
        root_osnova = ET.parse(os.path.join(ROOT_DIR, 'osnova.xml')).getroot()
    except Exception:
        return "conf.xml має помилки"
    if root_osnova.find(name).text is not None:
        return root_osnova.find(name).text
    else:
        return " Тег " + name + " не існує в osnova.xml"

def get_hot_keyboard_XML(name):
    try:
        root_osnova = ET.parse(os.path.join(ROOT_DIR, 'hot_keyboard.xml')).getroot()
    except Exception:
        return "conf.xml має помилки не існує"
    if root_osnova.find(name).text is not None:
        return root_osnova.find(name).text
    else:
        return " Тег " + name + " не існує в hot_keyboard.xml"

def change_val_XML(name_file_XML, val,new_val):
     root_change = ET.parse(os.path.join(ROOT_DIR, name_file_XML +'.xml'))
     for t in root_change.iterfind(val):
         t.text = new_val
     root_change.write(os.path.join(ROOT_DIR, name_file_XML +'.xml'),encoding="UTF-8",xml_declaration=True)