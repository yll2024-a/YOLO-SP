import os
import cv2
import xml.etree.ElementTree as ET

# 文件夹路径
image_folder = '1'
label_folder = '2'
output_folder = '3'

# 类别名称设置为"object"
class_name = 'litchi'

def convert(size, box):
    dw = size[0]
    dh = size[1]
    x = box[0] * dw
    y = box[1] * dh
    w = box[2] * dw
    h = box[3] * dh
    xmin = int(x - w / 2)
    ymin = int(y - h / 2)
    xmax = int(x + w / 2)
    ymax = int(y + h / 2)
    return xmin, ymin, xmax, ymax

def convert_annotation(image_name, label_name):
    # 获取图像的宽高
    image_path = os.path.join(image_folder, image_name)
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error loading image {image_path}")
        return

    height, width, _ = img.shape

    # 读取标签文件
    label_path = os.path.join(label_folder, label_name)
    with open(label_path, 'r') as file:
        lines = file.readlines()

    # 创建XML文件结构
    root = ET.Element("annotation")
    ET.SubElement(root, "folder").text = os.path.basename(image_folder)
    ET.SubElement(root, "filename").text = image_name
    ET.SubElement(root, "path").text = image_path

    source = ET.SubElement(root, "source")
    ET.SubElement(source, "database").text = "Unknown"

    size_elem = ET.SubElement(root, "size")
    ET.SubElement(size_elem, "width").text = str(width)
    ET.SubElement(size_elem, "height").text = str(height)
    ET.SubElement(size_elem, "depth").text = "3"

    ET.SubElement(root, "segmented").text = "0"

    for line in lines:
        parts = line.strip().split()
        class_id = int(parts[0])
        x_center, y_center, w, h = map(float, parts[1:])

        xmin, ymin, xmax, ymax = convert((width, height), (x_center, y_center, w, h))

        obj = ET.SubElement(root, "object")
        ET.SubElement(obj, "name").text = class_name
        ET.SubElement(obj, "pose").text = "Unspecified"
        ET.SubElement(obj, "truncated").text = "0"
        ET.SubElement(obj, "difficult").text = "0"

        bndbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bndbox, "xmin").text = str(xmin)
        ET.SubElement(bndbox, "ymin").text = str(ymin)
        ET.SubElement(bndbox, "xmax").text = str(xmax)
        ET.SubElement(bndbox, "ymax").text = str(ymax)

    # 保存XML文件
    tree = ET.ElementTree(root)
    xml_output_path = os.path.join(output_folder, label_name.replace(".txt", ".xml"))
    tree.write(xml_output_path)

def main():
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for label_name in os.listdir(label_folder):
        if label_name.endswith('.txt'):
            # 尝试匹配图像文件（.jpg 或 .jpeg）
            base_name = label_name.replace('.txt', '')
            image_name_jpg = base_name + '.jpg'
            image_name_jpeg = base_name + '.jpeg'
            
            # 优先使用 jpg 格式，如果不存在则使用 jpeg 格式
            if os.path.exists(os.path.join(image_folder, image_name_jpg)):
                image_name = image_name_jpg
            elif os.path.exists(os.path.join(image_folder, image_name_jpeg)):
                image_name = image_name_jpeg
            else:
                print(f"Image not found for label file: {label_name}")
                continue
            
            convert_annotation(image_name, label_name)

if __name__ == "__main__":
    main()
