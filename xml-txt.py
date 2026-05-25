import os
import xml.etree.ElementTree as ET

# 【唯一需要确认的：你的XML真实路径】
XML_INPUT = r"C:\Users\zjk\Desktop\Annotations"  # XML所在文件夹
TXT_OUTPUT = r"C:\Users\zjk\Desktop\GTA5Dataset\labels\train"  # 输出TXT文件夹

# 你的XML里类别就是 car，完全匹配
CLASSES = ["car"]

# 自动创建文件夹
os.makedirs(TXT_OUTPUT, exist_ok=True)

# 开始转换
for xml_file in os.listdir(XML_INPUT):
    if not xml_file.endswith(".xml"):
        continue

    # 读取XML
    tree = ET.parse(os.path.join(XML_INPUT, xml_file))
    root = tree.getroot()

    # 读取图片宽高
    width = int(root.find("size/width").text)
    height = int(root.find("size/height").text)

    # 创建TXT
    txt_file = os.path.splitext(xml_file)[0] + ".txt"
    txt_path = os.path.join(TXT_OUTPUT, txt_file)

    with open(txt_path, "w", encoding="utf-8") as f:
        # 遍历所有标注目标
        for obj in root.findall("object"):
            name = obj.find("name").text
            if name not in CLASSES:
                continue

            # 读取框坐标
            xmin = float(obj.find("bndbox/xmin").text)
            ymin = float(obj.find("bndbox/ymin").text)
            xmax = float(obj.find("bndbox/xmax").text)
            ymax = float(obj.find("bndbox/ymax").text)

            # 转 YOLO 格式
            x_center = (xmin + xmax) / 2 / width
            y_center = (ymin + ymax) / 2 / height
            w = (xmax - xmin) / width
            h = (ymax - ymin) / height

            # 写入数据
            f.write(f"0 {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n")

print("✅ 转换成功！所有 TXT 标签已生成，内含标注数据！")