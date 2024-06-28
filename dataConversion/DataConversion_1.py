import json
import csv
#
# # 读取JSON文件
# with open('./data/datasample/gossipcop_v3-1_style_based_fake.json', 'r', encoding='utf-8') as json_file:
#     data = json.load(json_file)

# 将数据写入TSV文件
# with open('./data/datasample/gossipcop_v3-1_style_based_fake.tsv', 'w', newline='', encoding='utf-8') as tsv_file:
#     writer = csv.writer(tsv_file, delimiter='\t')
#
#     # 写入表头
#     writer.writerow(data.keys())  # 获取字典的键
#
#     # 写入数据
#     for item in data.values():  # 使用字典的values()方法遍历字典的值
#         writer.writerow(item.values())
# 读取JSON文件
with open('./data/datasample/gossipcop_v3-3_integration_based_fake_tn200.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# 定义新的表头映射
header_mapping = {
    "origin_id": "Number",
    "origin_label": None,
    "origin_text": None,
    "generated_text": "Content",
    "generated_label": "Label",
    "has_top_img": None
}

# 将数据写入TSV文件
with open('./data/datasample/gossipcop_v3-3_integration_based_fake_tn200.tsv', 'w', newline='', encoding='utf-8') as tsv_file:
    writer = csv.writer(tsv_file, delimiter='\t')

    # 写入新的表头
    writer.writerow(["Label", "Number1","Number2", "Content"])

    # 写入数据
    for value in data.values():
        # 创建新的行数据，仅包含映射表头中存在的列
        row = [
            value.get("doc_2_label", ""),  # 使用映射中的替代列名
            value.get("doc_1_id", ""),
            value.get("doc_2_id", ""),         # 使用映射中的替代列名
            value.get("generated_text", "")     # 使用映射中的替代列名
        ]
        writer.writerow(row)

# # 修改列名、保留列和删除列
# modified_data = []
# for item in data:
#     modified_item = {
#         "Label": item["generated_label"],
#         "Number": item["origin_id"],
#         "Content": item["generated_text"]
#     }
#     modified_data.append(modified_item)
#
# # 将修改后的数据写入TSV文件
# with open('./data/datasample/gossipcop_v3-1_style_based_fake.tsv', 'w', newline='', encoding='utf-8') as tsv_file:
#     writer = csv.DictWriter(tsv_file, fieldnames=["Label", "Number", "Content"], delimiter='\t')
#     writer.writeheader()
#     writer.writerows(modified_data)


