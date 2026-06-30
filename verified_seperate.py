import os,shutil
from glob import glob
from xml.etree import ElementTree
from lxml import etree
# from libs.constants import DEFAULT_ENCODING
# from libs.ustr import ustr


# ENCODE_METHOD = DEFAULT_ENCODING
folder_path = "/home/vadmin/Desktop/28_/validated_data"
xmls = glob(os.path.join(folder_path, "Annotations", "*.xml"))

print(len(xmls))

os.makedirs(os.path.join(folder_path,"verified"),exist_ok=True)
os.makedirs(os.path.join(folder_path,"verified","Annotations"),exist_ok=True)
os.makedirs(os.path.join(folder_path,"verified","JPEGImages"),exist_ok=True)

for item in xmls:

    print(item)
    
    parser = etree.XMLParser()
    
    xml_tree = ElementTree.parse(item, parser=parser).getroot()
    
    try:
        verified = xml_tree.attrib['verified']
        
        if verified == 'yes':
            shutil.move(item, os.path.join(folder_path, "verified", "Annotations", os.path.basename(item)))
            img_src_name = os.path.join(folder_path, "JPEGImages", os.path.basename(item)[:-4] + ".jpg")
            img_dst_name = os.path.join(folder_path, "verified", "JPEGImages", os.path.basename(item)[:-4] + ".jpg")
            print(img_src_name, img_dst_name)

            shutil.move(img_src_name, img_dst_name)
            
        else:
            pass
        
    except:
        pass
            
    
        
    
