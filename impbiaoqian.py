import os
import shutil
import xml.etree.ElementTree as ET
from xml.dom import minidom

def prettify_element(elem):
    """格式化XML元素为字符串，并增加缩进和换行"""
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def convert_hrsc_to_voc(xml_folder, output_folder, move_folder_xml, move_folder_img):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(move_folder_xml):
        os.makedirs(move_folder_xml)
    if not os.path.exists(move_folder_img):
        os.makedirs(move_folder_img)

    # 类别ID到类别名称的映射字典
    id_to_name = {
        "100000002": "aircraft carrier",
        "100000003": "warcraft",
        "100000004": "merchant ship",
        "100000005": "aircraft carrier",
        "100000006": "aircraft carrier",
        "100000007": "warcraft",
        "100000008": "warcraft",
        "100000009": "warcraft",
        "100000010": "warcraft",
        "100000011": "warcraft",
        "100000012": "aircraft carrier",
        "100000013": "aircraft carrier",
        "100000014": "warcraft",
        "100000015": "warcraft",
        "100000016": "warcraft",
        "100000017": "warcraft",
        "100000018": "merchant ship",
        "100000019": "warcraft",
        "100000020": "merchant ship",
        "100000022": "merchant ship",
        "100000024": "merchant ship",
        "100000025": "merchant ship",
        "100000026": "merchant ship",
        "100000027": "submarine",
        "100000028": "warcraft",
        "100000029": "warcraft",
        "100000030": "merchant ship",
        "100000031": "aircraft carrier",
        "100000032": "aircraft carrier",
        "100000033": "aircraft carrier"
    }

    # 遍历xml文件夹中的所有文件
    for xml_file in os.listdir(xml_folder):
        if xml_file.endswith(".xml"):
            xml_path = os.path.join(xml_folder, xml_file)
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # 检查是否仅包含类别"100000001"
            only_100000001 = True
            objects = root.findall('.//HRSC_Object')
            for obj in objects:
                class_id = obj.find('Class_ID').text
                if class_id != "100000001":
                    only_100000001 = False
                    break
            
            if only_100000001:
                # 移动XML文件和对应的图像文件到新的文件夹
                shutil.move(xml_path, os.path.join(move_folder_xml, xml_file))
                img_file = root.find('Img_FileName').text + '.' + root.find('Img_FileFmt').text
                img_path = os.path.join(xml_folder, img_file)
                if os.path.exists(img_path):
                    shutil.move(img_path, os.path.join(move_folder_img, img_file))
                continue

            # 创建新的VOC格式的XML结构
            annotation = ET.Element("annotation")
            
            # 添加文件名、路径等基础信息
            folder = ET.SubElement(annotation, "folder").text = xml_folder
            filename = ET.SubElement(annotation, "filename").text = root.find('Img_FileName').text + '.' + root.find('Img_FileFmt').text
            path = ET.SubElement(annotation, "path").text = os.path.join(xml_folder, filename)

            # 添加图像尺寸信息
            size = ET.SubElement(annotation, "size")
            ET.SubElement(size, "width").text = root.find('Img_SizeWidth').text
            ET.SubElement(size, "height").text = root.find('Img_SizeHeight').text
            ET.SubElement(size, "depth").text = root.find('Img_SizeDepth').text

            # 设置segmented为0
            ET.SubElement(annotation, "segmented").text = "0"

            # 添加目标对象信息
            for obj in objects:
                object = ET.SubElement(annotation, "object")
                class_id = obj.find('Class_ID').text
                class_name = id_to_name.get(class_id, "unknown")  # 根据ID映射名称，若ID不存在则用"unknown"
                ET.SubElement(object, "name").text = class_name
                ET.SubElement(object, "pose").text = "Unspecified"
                ET.SubElement(object, "truncated").text = obj.find('truncated').text
                ET.SubElement(object, "difficult").text = obj.find('difficult').text
                
                bndbox = ET.SubElement(object, "bndbox")
                ET.SubElement(bndbox, "xmin").text = obj.find('box_xmin').text
                ET.SubElement(bndbox, "ymin").text = obj.find('box_ymin').text
                ET.SubElement(bndbox, "xmax").text = obj.find('box_xmax').text
                ET.SubElement(bndbox, "ymax").text = obj.find('box_ymax').text

            # 格式化XML并保存
            formatted_xml = prettify_element(annotation)
            new_xml_file = os.path.join(output_folder, xml_file)
            with open(new_xml_file, 'w', encoding='utf-8') as f:
                f.write(formatted_xml)

# 使用示例
xml_folder = 'VOCdevkit/VOC2007/Annotations'
output_folder = 'VOCdevkit/VOC2007/Annotations1'
move_folder_xml = 'VOCdevkit/VOC2007/Only100000001_XML'
move_folder_img = 'VOCdevkit/VOC2007/Only100000001_IMG'
convert_hrsc_to_voc(xml_folder, output_folder, move_folder_xml, move_folder_img)
