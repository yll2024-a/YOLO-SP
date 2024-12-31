import os
import xml.etree.ElementTree as ET

def extract_class_ids(xml_folder, output_file):
    class_ids = set()  # 使用集合去重

    # 遍历文件夹中的所有XML文件
    for file_name in os.listdir(xml_folder):
        if file_name.endswith('.xml'):
            file_path = os.path.join(xml_folder, file_name)
            
            # 解析XML文件
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()
                
                # 遍历所有HRSC_Object标签，提取每个对象的Class_ID
                objects = root.findall('.//HRSC_Object')
                for obj in objects:
                    class_id = obj.find('Class_ID')
                    if class_id is not None and class_id.text is not None:
                        class_ids.add(class_id.text.strip())
            except ET.ParseError as e:
                print(f"Error parsing {file_name}: {e}")
            except Exception as e:
                print(f"Unexpected error with {file_name}: {e}")

    # 将提取的Class_ID写入文本文件
    with open(output_file, 'w') as f:
        for class_id in sorted(class_ids):
            f.write(f"{class_id}\n")

# 使用示例
xml_folder = 'VOCdevkit/VOC2007/Annotations1'  # XML文件夹路径
output_file = 'class_ids.txt'  # 输出文本文件路径
extract_class_ids(xml_folder, output_file)
