import os
import shutil
import xmltodict

from dicttoxml import dicttoxml
from xml.dom.minidom import parseString

part = "/home/vadmin/Desktop/15_06_2026/15_june_chintak_sir/102_jpg"


segregate_characters_path = os.path.join(f'{part}', 'segregate_characters')
verbose = True

# if not os.path.exists(os.path.join(part, 'confuse')):
#     raise Exception('Could not find "confuse" directory!!')

# confused_characters = [f.split('_')[0] for f in os.listdir(os.path.join(part, 'confuse'))]
# confused_characters = list(set(confused_characters))

def custom_item_func(parent):
    return parent

def is_overlapping(pt1_x1, pt1_y1, pt1_x2, pt1_y2, pt2_x1, pt2_y1, pt2_x2, pt2_y2, overlapping_th):
    """
        function to check overlapping of rectangles
    """
    overlapping_x1 = max(pt1_x1, pt2_x1)
    overlapping_y1 = max(pt1_y1, pt2_y1)
    overlapping_x2 = min(pt1_x2, pt2_x2)
    overlapping_y2 = min(pt1_y2, pt2_y2)
    overlapping_area = max(0, overlapping_x2 - overlapping_x1 + 1) * \
        max(0, overlapping_y2 - overlapping_y1 + 1)

    if overlapping_area <= 1:
        # print("not overlapped")
        return False

    rect1_area = max(0, pt1_x2 - pt1_x1 + 1) * max(0, pt1_y2 - pt1_y1 + 1)
    rect2_area = max(0, pt2_x2 - pt2_x1 + 1) * max(0, pt2_y2 - pt2_y1 + 1)

    min_area_rect = min(rect1_area, rect2_area)

    if overlapping_area >= int(overlapping_th * min_area_rect):
        # print("overlapped")
        return True
        
    return False

characters_dict = dict()
for root, _, files in os.walk(segregate_characters_path):
    for f in files:
        img_name = f.split('_Unspecified_')[0]
        if not img_name in characters_dict:
            characters_dict[img_name] = list()

        char_info = {
            'name' : root.split(os.sep)[-1],
            'pose' : f.split('_')[-7],
            'truncated' : f.split('_')[-6],
            'difficult' : f.split('_')[-5],
            'bndbox' : {
                'xmin' : f.split('_')[-4],
                'ymin' : f.split('_')[-3],
                'xmax' : f.split('_')[-2],
                'ymax' : f.split('_')[-1].split('.')[0],
            }
        }

        characters_dict[img_name].append(char_info)

imgs_path = os.path.join(part, 'JPEGImages')
xmls_path = os.path.join(part, 'Annotations')

imgs = [os.path.join(imgs_path, f) for f in os.listdir(imgs_path)]
xmls = [os.path.join(xmls_path, f) for f in os.listdir(xmls_path)]

imgs.sort()
xmls.sort()

os.makedirs(os.path.join(part, 'validated_data', 'JPEGImages'), exist_ok=True)
os.makedirs(os.path.join(part, 'validated_data', 'Annotations'), exist_ok=True)
os.makedirs(os.path.join(part, 'doubtful_data', 'JPEGImages'), exist_ok=True)
os.makedirs(os.path.join(part, 'doubtful_data', 'Annotations'), exist_ok=True)



# for _, (img, xml) in enumerate(zip(imgs, xmls), 1):
for xml in xmls:
    img = xml.replace("Annotations", "JPEGImages", 1)[:-4] + ".jpg"

    try:
        
        img_name = img.split(os.sep)[-1].split('.jpg')[0]

        with open(xml) as f:
            xml_dict = xmltodict.parse(f.read())['annotation']

        xml_dict['object'] = list()
        if img_name in characters_dict:
            if len(characters_dict[img_name]) == 0:
                print(img)
            for char in characters_dict[img_name]:

                if char["name"].lower()  in ["incorrect"]:
                    print(img)
                    # doubtful = True

                xml_dict['object'].append(char)

        new_xml = dicttoxml(xml_dict, custom_root='annotation', attr_type = False, item_func = custom_item_func)

        new_xml = new_xml.decode('utf-8')
        new_xml = new_xml.replace('<object><object>', '<object>').replace('</object></object>', '</object>')
        new_xml = new_xml.encode()

        dom = parseString(new_xml)
        xml_str = dom.toprettyxml()

        new_img_path = os.path.join(part, 'validated_data', 'JPEGImages', img.split(os.sep)[-1])
        new_xml_path = os.path.join(part, 'validated_data', 'Annotations', xml.split(os.sep)[-1])

        doubtful = False
        # if len(xml_dict['object']) < 8 or len(xml_dict['object']) > 10:
        # if len(xml_dict['object']) >= 0 :
        #     doubtful = True
        #     if verbose:
        #         print(f"INFO :: LP should have atleast 8 and atmost 10 characters, where LP has {len(xml_dict['object'])} characters!!")
        # if img_name in confused_characters:
        #     doubtful = True
        #     if verbose:
        #         print("INFO :: LP character/s was/were found in the confuse directory!!")
        if 1:
            lp_width =  int(xml_dict['size']['width']) 
            lp_height =  int(xml_dict['size']['height'])

            for obj1 in xml_dict['object']:
                left1 = int(obj1['bndbox']['xmin'])
                top1 = int(obj1['bndbox']['ymin'])
                right1 = int(obj1['bndbox']['xmax'])
                bottom1 = int(obj1['bndbox']['ymax'])

                obj1_width = right1 - left1
                obj1_height = bottom1 - top1
                # if ((obj1_height / lp_height) < 0.2):
                #     doubtful = True
                #     # if verbose:
                #     #     print("INFO :: LP character/s is/are too small w.r.t LP!!")
                #     break

                for obj2 in xml_dict['object']:
                    if obj1 is obj2: continue

                    left2 = int(obj2['bndbox']['xmin'])
                    top2 = int(obj2['bndbox']['ymin'])
                    right2 = int(obj2['bndbox']['xmax'])
                    bottom2 = int(obj2['bndbox']['ymax'])

                    overlaped = is_overlapping(
                                                left1, top1, right1, bottom1,
                                                left2, top2, right2, bottom2,
                                                0.75
                                            )
                    
                    if overlaped: continue
                    if overlaped:
                        doubtful = True
                        # if verbose:
                        #     print("INFO :: LP characters are overlapping!!")
                        break
                    
                if doubtful:
                    break

        if doubtful:
            new_img_path = os.path.join(part, 'doubtful_data', 'JPEGImages', img.split(os.sep)[-1])
            new_xml_path = os.path.join(part, 'doubtful_data', 'Annotations', xml.split(os.sep)[-1])

        with open(new_xml_path, 'w') as f:
            f.write(xml_str)

        shutil.copyfile(img, new_img_path)

    except Exception as e:
        print(img)
        print(e)
