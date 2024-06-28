import csv
import re


tsv_file = './data/datasample/gossipcop_v3-3_integration_based_fake_tn200.tsv'
# tsv_output_file = './data/datasample/gossipcop_v3-1_style_based_fake_1_label.tsv'
# 读取 TSV 文件
# 增加字段大小限制
csv.field_size_limit(int(2**31-1))
with open(tsv_file, 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='\t')
    headers = next(reader)  # 读取表头
    for row in reader:
        content = row[3]
        # 定义一个正则表达式模式来匹配数字部分
        pattern = r'\d+'
        # 在字符串中搜索匹配的部分
        match = re.search(pattern, row[1])
        match2 = re.search(pattern, row[2])
        PageNo = match.group() + match2.group()
        number_part = PageNo

        # 写入 TSV 文件
        with open(f'./data/datasample/tem2/page{number_part}.txt', 'w', errors='ignore') as f:
            # 写入数据到文件
            f.write(content)






