import ccxt
import pandas as pd
from datetime import datetime, timedelta

# 1. 初始化交易所
exchange = ccxt.binanceusdm()  # 连接Binance U本位合约市场

# 2. 定义参数
symbol = 'ZRO/USDT'
timeframe = '1m'  # 分钟级K线
start_date = '2024-06-20T00:00:00Z' # 使用ISO 8601格式

# CCXT使用毫秒级时间戳
since = exchange.parse8601(start_date)
end_time = since + 7 * 24 * 60 * 60 * 1000  # 7天后的时间戳

# 3. 获取K线数据 (OHLCV)
# 交易所API单次请求有上限（如1000条），需要循环获取
all_ohlcv = []
while since < end_time:
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since)
        if len(ohlcv):
            since = ohlcv[-1][0] + exchange.parse_timeframe(timeframe) * 1000
            all_ohlcv.extend(ohlcv)
            print(f"获取到 {len(ohlcv)} 条数据，最新时间: {exchange.iso8601(ohlcv[-1][0])}")
        else:
            break
    except Exception as e:
        print(f"出现错误: {e}")
        break

# 转换成Pandas DataFrame
df_ohlcv = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df_ohlcv['datetime'] = pd.to_datetime(df_ohlcv['timestamp'], unit='ms')

# 4. 获取资金费率数据
# 资金费率数据通常是每8小时或4小时一次，获取逻辑类似
all_funding_rates = []
print("\n开始获取资金费率数据...")
try:
    # 1. API调用获取数据
    funding_rates = exchange.fetch_funding_rate_history(symbol, limit=1000)

    # 2. 关键检查：先判断有没有拿到数据
    if funding_rates:
        # 3. 如果有数据，才进行后续所有处理
        df_funding = pd.DataFrame(funding_rates)

        # 4. 使用正确的列名 'fundingTimestamp'
        df_funding['datetime'] = pd.to_datetime(df_funding['fundingTimestamp'], unit='ms')
        df_funding['fundingRate'] = pd.to_numeric(df_funding['fundingRate'])

        df_funding = df_funding[['datetime', 'fundingRate']].rename(columns={'fundingRate': 'funding_rate'})

        # 5. 保存数据到CSV
        df_funding.to_csv('ZROUSDT_funding_rate.csv', index=False)
        print("资金费率数据获取成功并已保存。")

    else:
        # 如果API调用成功了，但就是没返回数据（比如这个合约太新了还没有费率记录）
        print("未能获取到资金费率数据，API返回为空。")

except Exception as e:
    # 如果连API调用都失败了（比如网络问题、API接口名错误等）
    print(f"获取资金费率时出现错误: {e}")


# 5. 保存数据到CSV，方便后续分析
df_ohlcv.to_csv('ZROUSDT_1m_ohlcv.csv', index=False)

print("数据获取完成并已保存到CSV文件。")