import os
import xml.etree.ElementTree as ET

def extract_unique_classes_from_xml(xml_folder, output_txt_file):
    # 用于存储不重复的类别
    unique_classes = set()

    # 遍历xml文件夹中的所有文件
    for xml_file in os.listdir(xml_folder):
        if xml_file.endswith(".xml"):
            xml_path = os.path.join(xml_folder, xml_file)
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # 找到所有的目标类别
            for obj in root.findall('object'):
                cls = obj.find('name').text
                unique_classes.add(cls)

    # 将不重复的类别写入txt文件
    with open(output_txt_file, 'w') as f:
        for cls in sorted(unique_classes):
            f.write(cls + '\n')

# 使用示例
xml_folder = 'VOCdevkit/VOC2007/Annotations1'
output_txt_file = 'output_classes.txt'
extract_unique_classes_from_xml(xml_folder, output_txt_file)
