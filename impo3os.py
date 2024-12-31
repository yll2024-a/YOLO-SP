import os
from PIL import Image

# 文件夹路径
folder_path = 'VOCdevkit/VOC2007/JPEGImages'

def convert_jpeg_to_jpg(folder_path):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.jpeg'):
            # 构建文件的完整路径
            jpeg_path = os.path.join(folder_path, filename)
            jpg_path = os.path.join(folder_path, os.path.splitext(filename)[0] + '.jpg')

            # 打开JPEG文件并转换为JPG格式
            with Image.open(jpeg_path) as img:
                img.convert('RGB').save(jpg_path, 'JPEG')
            
            # 删除原来的JPEG文件
            os.remove(jpeg_path)
            print(f"Converted and removed: {filename}")

if __name__ == "__main__":
    convert_jpeg_to_jpg(folder_path)
