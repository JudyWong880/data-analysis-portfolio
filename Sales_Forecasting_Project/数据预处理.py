import pandas as pd

# 1. 加载所需数据
orders = pd.read_csv('olist_orders_dataset.csv')
order_items = pd.read_csv('olist_order_items_dataset.csv')
products = pd.read_csv('olist_products_dataset.csv')

# 2. 数据合并 (模拟SQL的多表JOIN)
# 合并订单与订单商品信息
df = pd.merge(orders, order_items, on='order_id')
# 再合并商品信息
df = pd.merge(df, products, on='product_id')

# 3. 数据清洗与特征工程
# 筛选核心字段
df = df[['order_id', 'product_id', 'product_category_name', 'order_purchase_timestamp']]

# 将时间戳列转换为datetime对象，这是时间序列分析的基石
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

# 提取日期部分
df['order_date'] = df['order_purchase_timestamp'].dt.date

# 按天统计每个商品(product_id)的销量
# 这里我们假设一行就是一个销量，所以用size()来计数
daily_sales = df.groupby(['order_date', 'product_id']).size().reset_index(name='daily_quantity')
daily_sales['order_date'] = pd.to_datetime(daily_sales['order_date'])

print(daily_sales.head())
# 至此，我们得到了进行时序分析的基础数据表 daily_sales