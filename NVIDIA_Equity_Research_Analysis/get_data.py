import yfinance as yf
import time  # 导入 time 模块

# 创建一个股票代码列表（即使现在只有一个）
ticker_symbols = ["NVDA"]  # 未来你可以添加更多, 例如: ["NVDA", "AAPL", "GOOGL"]

for ticker_symbol in ticker_symbols:
    try:
        print(f"--- 正在获取 {ticker_symbol} 的数据 ---")

        # 获取股票对象
        ticker_obj = yf.Ticker(ticker_symbol)

        # 获取历史市场数据
        # 这个调用是触发速率限制的主要原因
        hist_data = ticker_obj.history(period="5y", interval="1d")

        # --- 将历史数据保存到Excel文件 ---
        file_name = f"{ticker_symbol}_historical_data.xlsx"
        hist_data.to_excel(file_name)
        print(f"历史数据已保存至: {file_name}")

        # --- 获取其他信息 ---
        # .info 属性包含大量信息，它也是一次独立的API调用
        info = ticker_obj.info

        # 使用 .get() 方法安全地获取数据，避免因缺少某个键而报错
        market_cap = info.get('marketCap', 'N/A')  # 市值
        beta = info.get('beta', 'N/A')  # Beta系数

        print(f"市值 (Market Cap): {market_cap}")
        print(f"Beta系数 (5Y Monthly): {beta}")

        # --- 关键步骤: 在下次请求前等待 ---
        # 为了尊重API的使用规则，增加2秒的延迟
        print("等待2秒后进行下一次请求...")
        time.sleep(2)

    except Exception as e:
        # 如果获取某只股票时出错，打印错误信息并继续处理下一只，而不是让整个程序崩溃
        print(f"获取 {ticker_symbol} 数据失败: {e}")

print("\n所有任务已完成。")