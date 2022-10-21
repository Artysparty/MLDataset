import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("./venv/data/thermopoints.csv")
pd.core.frame.DataFrame
pd.set_option("display.max.columns", None)
data.head()

# Количество лесных пожаров по видам
plt.plot(data.type_name.unique(), data.type_name.value_counts())
plt.show()

# Количоство пожаров по годам
data['dt'] = pd.to_datetime(data['dt'])
data['year'] = data['dt'].dt.year
data['month'] = data['dt'].dt.month
data['day'] = data['dt'].dt.day

data = data.set_index(['dt'])
plt.plot(data.year.unique(), [data.loc['2012'].year.value_counts(),
                              data.loc['2013'].year.value_counts(),
                              data.loc['2014'].year.value_counts(),
                              data.loc['2015'].year.value_counts(),
                              data.loc['2016'].year.value_counts(),
                              data.loc['2017'].year.value_counts(),
                              data.loc['2018'].year.value_counts(),
                              data.loc['2019'].year.value_counts(),
                              data.loc['2020'].year.value_counts(),
                              data.loc['2021'].year.value_counts()
                              ])
plt.show()
