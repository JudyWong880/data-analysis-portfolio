# 获取数据.py (最终现货版)

import ccxt
import pandas as pd
from datetime import datetime

# --- 代理设置 (这部分已经成功了，保持不变) ---
proxy_port = 7890 # 如果你的端口不是7890，记得改这里
try:
    # --- ！！！核心修改：从 binanceusdm 改为 binance ！！！---
    exchange = ccxt.binance({
        'proxies': {
            'http': f'http://127.0.0.1:{proxy_port}',
            'https': f'http://127.0.0.1:{proxy_port}',
        },
    })
    exchange.load_markets()
    print(f"代理连接成功！将通过 http://127.0.0.1:{proxy_port} 连接币安【现货】服务器...")
except Exception as e:
    print(f"代理设置或连接失败。错误: {e}")
    exit()
# --- 修改结束 ---

# 1. 定义参数 (保持不变)
symbol = 'ZRO/USDT'
timeframe = '1m'
start_date = '2024-06-20T00:00:00Z'
since = exchange.parse8601(start_date)
end_time = since + 7 * 24 * 60 * 60 * 1000

# 2. 获取K线数据 (OHLCV) (保持不变)
print("\n开始获取K线数据 (OHLCV)...")
all_ohlcv = []
while since < end_time:
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since)
        if len(ohlcv):
            since = ohlcv[-1][0] + exchange.parse_timeframe(timeframe) * 1000
            all_ohlcv.extend(ohlcv)
            print(f"获取到 {len(ohlcv)} 条K线数据，最新时间: {exchange.iso8601(ohlcv[-1][0])}")
        else:
            break
    except Exception as e:
        print(f"获取K线数据时出现错误: {e}")
        break

# 转换成Pandas DataFrame并保存
if all_ohlcv:
    df_ohlcv = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df_ohlcv['datetime'] = pd.to_datetime(df_ohlcv['timestamp'], unit='ms')
    df_ohlcv.to_csv('ZROUSDT_1m_ohlcv_spot.csv', index=False) # 文件名加个spot以示区分
    print("K线数据获取完成并已保存。")
else:
    print("未能获取到K线数据。")


# --- 注意：现货市场没有资金费率，我们将这部分整个移除 ---
# (原获取资金费率的代码已删除)

print("\n--- 所有数据获取任务执行完毕 ---")