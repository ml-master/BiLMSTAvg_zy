import csv
import re

# 定义文件路径
tsv_file = './data/datasample/gossipcop_v3-3_integration_based_fake_tn200.tsv'
tsv_output_file = './data/datasample/gossipcop_v3-3_integration_based_fake_tn200_label.tsv'

# 读取 TSV 文件
csv.field_size_limit(int(2**31-1))
with open(tsv_file, 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='\t')
    headers = next(reader)  # 读取表头
    # 准备一个新的数据列表，用于存储处理后的数据
    new_data = []

    # 遍历每一行数据
    for row in reader:
        # 根据条件设置 Non_credible 的值
        if row[0] == 'fake':
            Non_credible = 1
        else:
            Non_credible = 0
        # 假设 Website, PageNo, PageURL, PageArchivedURL 的值已经知道是 'gossipcop'
        # 如果这些值应该在原始数据中获取，你需要根据实际情况调整 row 的索引
        Website = 'gossipcop'
        # 定义一个正则表达式模式来匹配数字部分
        pattern = r'\d+'
        # 在字符串中搜索匹配的部分
        match = re.search(pattern, row[1])
        match2 = re.search(pattern, row[2])
        PageNo = match.group()+match2.group()

        PageURL = 'gossipcop'  # 如果 URL 在原始数据中，也需要调整
        PageArchivedURL = 'gossipcop'  # 同上

        # 将处理后的数据添加到新的数据列表中
        new_data.append([Non_credible, Website, PageNo, PageURL, PageArchivedURL])

# 写入新的 TSV 文件
with open(tsv_output_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter='\t')
    # 写入新的表头
    writer.writerow(['Non_credible', 'Website', 'PageNo', 'PageURL', 'PageArchivedURL'])
    # 写入处理后的数据
    for row in new_data:
        writer.writerow(row)

print(f'数据已写入{tsv_output_file}')
