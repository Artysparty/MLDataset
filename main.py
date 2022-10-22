import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import LineString
from shapely.ops import split
from shapely.affinity import translate

data = pd.read_csv("./venv/data/thermopoints.csv")
pd.core.frame.DataFrame
pd.set_option("display.max.columns", None)

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

# Метод сдвига координат
def shift_geom(shift, gdataframe):
    shift -= 180
    moved_map = []
    splitted_map = []
    border = LineString([(shift,90),(shift,-90)])

    for row in gdataframe["geometry"]:
        splitted_map.append(split(row, border))
    for element in splitted_map:
        items = list(element)
        for item in items:
            minx, miny, maxx, maxy = item.bounds
            if minx >= shift:
                moved_map.append(translate(item, xoff=-180-shift))
            else:
                moved_map.append(translate(item, xoff=180-shift))

    gdf = gpd.GeoDataFrame({"geometry": moved_map})
    # if plotQ:
    #     fig, ax = plt.subplots()
    #     gdf.plot(ax=ax)
    #     plt.show()

    return gdf

# Проекция координат пожаров за май 2012 года на карту России
small_data = data.loc[(data.year == 2012) & (data.month == 5)]
gdf = gpd.GeoDataFrame(
    small_data,
    geometry=gpd.points_from_xy(pd.to_numeric(small_data['lon'], errors='coerce').fillna(0, downcast='infer'),
                                pd.to_numeric(small_data['lat'], errors='coerce').fillna(0, downcast='infer')))

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
russia = world[world['name'] == 'Russia']

rus_shift_90 = shift_geom(90, russia)
good_geom_rus = shift_geom(-90, rus_shift_90)

fig, ax = plt.subplots(figsize=(10,10))
good_geom_rus.plot(ax=ax, color='lightgrey', zorder=1)
gdf.plot(ax=ax, alpha=0.5, zorder=2)
plt.show()
