import akshare as ak
import pandas as pd

# 1. 定义要查询的参数
stock_code = "600519"
start_date = "20250101"  # 从2025年初开始
end_date = "20250721"  # 到今天的日期
# 复权选项: 'qfq' (前复权), 'hfq' (后复权), '' (不复权)
# 使用 'hfq' (后复权) 进行长期分析和回测能更准确地反映资产的真实收益
adjustment = "hfq"

print(f"正在获取股票代码: {stock_code} 的历史行情...")
print(f"时间范围: {start_date} 到 {end_date}")

try:
    # 2. 调用 AkShare 核心函数获取A股历史数据
    stock_hist_df = ak.stock_zh_a_hist(symbol=stock_code,
                                       period="daily",
                                       start_date=start_date,
                                       end_date=end_date,
                                       adjust=adjustment)

    # 3. 显示获取到的数据
    print("\n数据获取成功！")
    print("数据预览 (前5行):")
    print(stock_hist_df.head())

    print("\n数据预览 (后5行):")
    print(stock_hist_df.tail())

    print("\n数据基本信息 (列名、数据类型等):")
    stock_hist_df.info()

except Exception as e:
    print(f"\n获取数据时发生错误: {e}")