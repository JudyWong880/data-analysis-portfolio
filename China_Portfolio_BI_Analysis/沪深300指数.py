import akshare as ak
import os

# 1. 定义基准指数的参数
index_code = "000300"
index_name = "沪深300指数"

# 2. 定义数据的时间范围
start_date = "20250101"
end_date = "20250721"  # 当前日期

# 3. 定义输出文件夹 (与上一步使用的文件夹相同)
output_dir = "stock_data_csv"
# 确保文件夹存在
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"已创建文件夹: '{output_dir}'")

# 4. 获取并保存指数数据
print(f"--- 正在获取基准数据: {index_name} ({index_code}) ---")
print(f"时间范围: {start_date} 到 {end_date}")

try:
    # 使用 ak.index_zh_a_hist 函数来获取指数数据
    index_df = ak.index_zh_a_hist(symbol=index_code,
                                  period="daily",
                                  start_date=start_date,
                                  end_date=end_date)

    if not index_df.empty:
        # 定义要保存的文件路径
        file_path = os.path.join(output_dir, f"{index_code}_{index_name}.csv")

        # 保存到CSV文件，使用 'utf-8-sig' 编码以确保中文在Excel中正常显示
        index_df.to_csv(file_path, index=False, encoding='utf-8-sig')

        print(f"  √ 基准数据已成功保存到: {file_path}")
    else:
        print(f"  ! 未获取到 {index_name} ({index_code}) 的数据。")

except Exception as e:
    print(f"  × 获取 {index_name} ({index_code}) 数据时发生错误: {e}")

print("\n基准数据处理完毕！")