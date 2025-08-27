import akshare as ak
import pandas as pd

# 设置Pandas显示选项，以便更好地查看DataFrame
pd.set_option('display.max_rows', None)

print("正在测试 AkShare 网络连通性...")

try:
    # 使用正确的函数名 tool_trade_date_hist_sina 获取A股交易日历
    trade_date_df = ak.tool_trade_date_hist_sina()

    # 如果能成功获取并打印数据，说明网络通畅
    print("网络连接成功！已成功获取交易日历数据：")
    print("最新交易日历 (前5行):")
    print(trade_date_df.head())
    print("\n最早交易日历 (后5行):")
    print(trade_date_df.tail())


except Exception as e:
    print(f"网络连接或数据获取失败，发生错误: {e}")