import akshare as ak

# 备用接口通常更稳定
try:
    print("--- 正在使用 akshare 的备用接口 ak.stock_us_daily 获取 NVDA 数据 ---")

    # 使用 ak.stock_us_daily 函数
    # 注意：它的参数和返回值与 stock_us_hist 略有不同
    # 它默认就会返回前复权的数据
    stock_us_daily_df = ak.stock_us_daily(symbol="NVDA", adjust="qfq")

    if not stock_us_daily_df.empty:
        print("成功通过 akshare 备用接口获取到数据！")
        # 它的列名可能是英文的
        print(stock_us_daily_df.tail())  # 打印最后5行数据看看

        # 保存到Excel
        file_name = "NVDA_akshare_daily_data.xlsx"
        stock_us_daily_df.to_excel(file_name, index=False)
        print(f"数据已成功保存到文件: {file_name}")
    else:
        print("使用 akshare 备用接口获取失败。")

except Exception as e:
    print(f"使用 akshare 时发生错误: {e}")
