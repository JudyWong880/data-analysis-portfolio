import pandas as pd

# 在原有的代码基础上，增加 low_memory=False 参数
df = pd.read_csv('14_data_EUW_Apex.csv', low_memory=False)

# 验证
print("数据加载成功！并且已消除DtypeWarning。")
print(df.head())

# 您可以再次运行 df.info()，会发现警告消失了
print("\n再次查看数据信息：")
df.info()