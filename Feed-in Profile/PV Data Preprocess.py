import pandas as pd
import matplotlib.pyplot as plt

tmy = pd.read_csv("pv_data_justus_jonas_2023.csv", usecols=["time", "temp_air", "global", "poa_direct",
                                               "poa_diffuse","wind_speed"], index_col = 0)

tmy.index = pd.date_range(start="2023-01-01 00:00", end="2023-12-31 23:00", freq="h")

tmy.columns = ["temp_air", "ghi","dni","dhi", "wind_speed"]
print(tmy)

tmy.plot(figsize=(16,9))
tmy.to_csv("Pvlib_data_justus_jonas_2023.csv")
plt.show()
