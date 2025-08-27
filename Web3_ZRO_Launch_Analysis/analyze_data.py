# analyze_data.py

import pandas as pd
import numpy as np

# --- 数据加载与准备 ---
try:
    # 加载我们第一阶段获取的数据
    df = pd.read_csv('ZROUSDT_1m_ohlcv_spot.csv')
    # 将datetime字符串转换为真正的日期时间格式，并设为索引
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)
    print("数据加载成功！开始进行深度分析...")
    print("-" * 50)
except FileNotFoundError:
    print("错误：未找到 ZROUSDT_1m_ohlcv_spot.csv 文件。")
    print("请确保分析脚本和数据文件在同一个目录下。")
    exit()

# --- 分析维度一：开盘效应分析 (Opening Effect Analysis) ---
print("维度一：开盘效应分析 (前60分钟)")
# 选取上线后第一个小时的数据
first_hour_df = df.head(60)

# a. 价格波动分析
if not first_hour_df.empty:
    opening_price = first_hour_df['open'].iloc[0]
    peak_price = first_hour_df['high'].max()
    low_price = first_hour_df['low'].min()
    closing_price_1h = first_hour_df['close'].iloc[-1]

    price_range = peak_price - low_price
    volatility_pct = (price_range / opening_price) * 100

    print(f"  - 开盘价: ${opening_price:.4f}")
    print(f"  - 1小时内最高价: ${peak_price:.4f}, 最低价: ${low_price:.4f}")
    print(f"  - 1小时收盘价: ${closing_price_1h:.4f}")
    print(f"  - 价格绝对波动范围: ${price_range:.4f}")
    print(f"  - 相对开盘价波动率: {volatility_pct:.2f}%")

    # b. 成交量分布
    total_volume_first_hour = first_hour_df['volume'].sum()
    peak_volume_minute_time = first_hour_df['volume'].idxmax()
    peak_volume_minute_value = first_hour_df['volume'].max()

    print(f"\n  - 第一个小时总成交量: {total_volume_first_hour:,.2f} ZRO")
    print(f"  - 成交量峰值时刻: {peak_volume_minute_time}")
    print(f"  - 峰值分钟成交量: {peak_volume_minute_value:,.2f} ZRO")

    # c. 多空力量对比
    up_volume = first_hour_df[first_hour_df['close'] >= first_hour_df['open']]['volume'].sum()
    down_volume = first_hour_df[first_hour_df['close'] < first_hour_df['open']]['volume'].sum()
    bull_bear_ratio = up_volume / down_volume if down_volume > 0 else float('inf')

    print(f"\n  - 买方主导成交量 (绿K): {up_volume:,.2f} ZRO")
    print(f"  - 卖方主导成交量 (红K): {down_volume:,.2f} ZRO")
    print(f"  - 多空成交量比值: {bull_bear_ratio:.2f}")
else:
    print("  - 数据不足，无法进行开盘效应分析。")

print("-" * 50)

# --- 分析维度二：流动性分析 (Liquidity Analysis) ---
print("维度二：流动性趋势分析")
# 计算每分钟的成交额 (Turnover in USDT)
df['turnover_usdt'] = df['close'] * df['volume']

# 按小时聚合，计算每小时的总成交量和总成交额
hourly_liquidity = df.resample('H').agg(
    total_volume=('volume', 'sum'),
    total_turnover_usdt=('turnover_usdt', 'sum'),
    avg_price=('close', 'mean')
)

# 过滤掉没有交易的空白小时
hourly_liquidity = hourly_liquidity[hourly_liquidity['total_volume'] > 0]

print("  - 上线后几个小时的流动性变化趋势 (按小时统计):")
# 为了方便阅读，格式化输出
hourly_liquidity['total_volume_str'] = hourly_liquidity['total_volume'].map('{:,.2f}'.format)
hourly_liquidity['total_turnover_usdt_str'] = hourly_liquidity['total_turnover_usdt'].map('${:,.2f}'.format)
print(hourly_liquidity[['total_volume_str', 'total_turnover_usdt_str', 'avg_price']].head(10))  # 展示前10个小时
print("-" * 50)

# --- 结论与下一步 ---
print("分析完成！")
print("现在你已经从数据中提取了关键的量化指标。")
print("下一步，我们将把这些数字变成图表，用 Tableau 或 Power BI 制作可视化报告！")