import os
import cv2
import xmltodict

part = '/home/vadmin/Desktop/28_/veri'
top_boundary_extension_factor = 0.2
bottom_boundary_extension_factor = 0.1
left_boundary_extension_factor = 0.1
right_boundary_extension_factor = 0.1

extention_factor = 0
scaling_factor = 1.0

imgs_path = os.path.join(part, 'JPEGImages')
xmls_path = os.path.join(part, 'Annotations')

imgs = [os.path.join(imgs_path, f) for f in os.listdir(imgs_path)]
xmls = [os.path.join(xmls_path, f) for f in os.listdir(xmls_path)]

imgs.sort()
xmls.sort()

count = 0
for idx, (img, xml) in enumerate(zip(imgs, xmls), 1):

    #print(count)
    count = count + 1

    image = cv2.imread(img)
    
    xml = img.replace("JPEGImages", "Annotations", 1)[:-4] + ".xml"
    # print(img, xml)
    if not os.path.exists(xml):  # Check if XML file exists
        print(f"XML file not found for image: {img}. Skipping...")
        continue
    with open(xml) as f:
        xml_dict = xmltodict.parse(f.read())['annotation']

    if not 'object' in xml_dict:
        continue

    if not isinstance(xml_dict['object'], list):
        xml_dict['object'] = [xml_dict['object']]

    #img_name = img.split(os.sep)[-1].split('.')[0]

    img_name = img.split(os.sep)[-1].split('.jpg')[0]
    # try:
    #     allowed_classes = {
    #         "Car", "SUV", "Bicycle", "Van", "Bus", "Motorcycle", "Truck", "Pickup Truck",
    #         "Machinery Vehicle", "Sports Car", "Crane", "Fire Truck", "Heavy Truck",
    #         "Ambulance", "Rickshaw"
    #     }

    #     for obj in xml_dict['object']:
    #         name = obj['name']

    #         # Filter: Process only allowed vehicle classes
    #         if name not in allowed_classes:
    #             continue

    #         pose = obj.get('pose', 'Unspecified')
    #         truncated = obj.get('truncated', 0)
    #         difficult = obj.get('difficult', 0)

    #         xmin = int(obj['bndbox']['xmin'])
    #         ymin = int(obj['bndbox']['ymin'])
    #         xmax = int(obj['bndbox']['xmax'])
    #         ymax = int(obj['bndbox']['ymax'])

    #         width = xmax - xmin
    #         height = ymax - ymin

    #         # Optional: Skip small objects
    #         if width < 50 or height < 50:
    #             continue

    #         x_ext = int(width * extention_factor)
    #         y_ext = int(height * extention_factor)

    #         xmin = max(0, xmin - x_ext)
    #         ymin = max(0, ymin - y_ext)
    #         xmax = min(image.shape[1], xmax + x_ext)
    #         ymax = min(image.shape[0], ymax + y_ext)

    #         char_name = f'{img_name}_{pose}_{truncated}_{difficult}_{xmin}_{ymin}_{xmax}_{ymax}.jpg'
    #         dst_folder = os.path.join(part, 'segregate_characters', name)
    #         os.makedirs(dst_folder, exist_ok=True)
    #         char_path = os.path.join(dst_folder, char_name)

    #         char_roi = image[ymin:ymax, xmin:xmax]
    #         char_roi = cv2.resize(char_roi, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_CUBIC)
    #         cv2.imwrite(char_path, char_roi, [cv2.IMWRITE_JPEG_QUALITY, 100])

    # except Exception as e:
    #     print(f"Error processing {img_name}: {e}")
    # try:
    #     for obj in xml_dict['object']:
    #         name = obj['name']
    #         pose = obj['pose']
    #         truncated = obj['truncated']
    #         difficult = obj['difficult']

    #         xmin = int(obj['bndbox']['xmin'])
    #         ymin = int(obj['bndbox']['ymin'])
    #         xmax = int(obj['bndbox']['xmax'])
    #         ymax = int(obj['bndbox']['ymax'])

    #         x = xmax - xmin
    #         y = ymax - ymin

    #         # Directional extension factors
    #         # top_ext = int(y * top_boundary_extension_factor)
    #         # bottom_ext = int(y * bottom_boundary_extension_factor)
    #         # left_ext = int(x * left_boundary_extension_factor)
    #         # right_ext = int(x * right_boundary_extension_factor)
    #         # Directional shrink factors (same values, reverse effect)
    #         top_shrink = int(y * top_boundary_extension_factor)
    #         bottom_shrink = int(y * bottom_boundary_extension_factor)
    #         left_shrink = int(x * left_boundary_extension_factor)
    #         right_shrink = int(x * right_boundary_extension_factor)

    #         # Shrink the bounding box inward
    #         xmin += left_shrink
    #         ymin += top_shrink
    #         xmax -= right_shrink
    #         ymax -= bottom_shrink
    #         # xmin -= left_ext
    #         # ymin -= top_ext
    #         # xmax += right_ext
    #         # ymax += bottom_ext

    #         xmin = max(0, xmin)
    #         ymin = max(0, ymin)
    #         xmax = min(xmax, image.shape[1])
    #         ymax = min(ymax, image.shape[0])

    #         char_name = f'{img_name}_{pose}_{truncated}_{difficult}_{xmin}_{ymin}_{xmax}_{ymax}.jpg'
    #         dst_folder = os.path.join(part, 'segregate_characters', name)
    #         os.makedirs(dst_folder, exist_ok=True)
    #         char_path = os.path.join(dst_folder, char_name)

    #         char_roi = image[ymin:ymax, xmin:xmax]
    #         char_roi = cv2.resize(char_roi, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_CUBIC)
    #         cv2.imwrite(char_path, char_roi, [cv2.IMWRITE_JPEG_QUALITY, 100])

    # except Exception as e:
    #     print(img_name, "***", e)


    try:
        for obj in xml_dict['object']:
            name = obj['name']
            pose = obj['pose']
            #pose = "Unspecified"
            truncated = obj['truncated']
            difficult = obj['difficult']

            xmin = int(obj['bndbox']['xmin'])
            ymin = int(obj['bndbox']['ymin'])
            xmax = int(obj['bndbox']['xmax'])
            ymax = int(obj['bndbox']['ymax'])

            x = xmax - xmin
            y = ymax - ymin
            
            #if x < 50 or y < 50: continue

            x_ext = int(x * extention_factor)
            y_ext = int(y * extention_factor )

            xmin -= x_ext
            ymin -= y_ext
            xmax += x_ext
            ymax += y_ext

            xmin = max(0, xmin)
            ymin = max(0, ymin)
            xmax = min(xmax, image.shape[1])
            ymax = min(ymax, image.shape[0])

            char_name = f'{img_name}_{pose}_{truncated}_{difficult}_{xmin}_{ymin}_{xmax}_{ymax}.jpg'
            dst_folder = os.path.join(part, 'segregate_characters', name)
            os.makedirs(dst_folder, exist_ok=True)
            char_path = os.path.join(dst_folder, char_name)
            

            char_roi = image[ymin:ymax, xmin:xmax]
            char_roi = cv2.resize(char_roi, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(char_path, char_roi, [cv2.IMWRITE_JPEG_QUALITY, 100])
    except Exception as e:
        print(img_name, "***", e)


