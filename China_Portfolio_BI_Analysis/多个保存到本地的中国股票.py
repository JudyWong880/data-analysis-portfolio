import akshare as ak
import pandas as pd
import os

# 1. 定义股票池 (使用字典，可以同时保存名称和代码)
stock_portfolio = {
    "贵州茅台": "600519",
    "宁德时代": "300750",
    "中国平安": "601318",
    "比亚迪": "002594"  # 额外增加一个
}

# 2. 定义数据的时间范围
start_date = "20250101"
end_date = "20250721"  # 当前日期

# 3. 创建用于存放CSV文件的文件夹
output_dir = "stock_data_csv"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"已创建文件夹: '{output_dir}'")

# 4. 循环获取并保存数据
print("\n开始批量下载股票数据并保存为CSV文件...")
for name, code in stock_portfolio.items():
    print(f"--- 处理中: {name} ({code}) ---")

    try:
        # 从AkShare获取后复权历史数据
        stock_df = ak.stock_zh_a_hist(symbol=code,
                                      period="daily",
                                      start_date=start_date,
                                      end_date=end_date,
                                      adjust="hfq")

        # 检查是否成功获取了数据
        if not stock_df.empty:
            # 定义要保存的文件路径和名称
            file_path = os.path.join(output_dir, f"{code}_{name}.csv")

            # 保存到CSV文件
            # index=False: 不将DataFrame的索引写入文件
            # encoding='utf-8-sig': 使用此编码确保中文在Excel中正常显示，避免乱码
            stock_df.to_csv(file_path, index=False, encoding='utf-8-sig')

            print(f"  √ 数据已成功保存到: {file_path}")
        else:
            print(f"  ! 未获取到 {name} ({code}) 的数据。")

    except Exception as e:
        print(f"  × 获取 {name} ({code}) 数据时发生错误: {e}")

print("\n所有股票处理完毕！")