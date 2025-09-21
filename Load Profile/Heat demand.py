# -*- coding: utf-8 -*-
"""
Creating heat demand profiles using the bdew method.

"""
import datetime
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import demandlib.bdew as bdew

# read example temperature series
filename = "temp_justus_2023.csv"
dirname = os.getcwd()
datapath = os.path.join(dirname, filename)
if not os.path.isfile(datapath):
    msg = (
        "The file {0} could not be found in the current working directory.\n "
        "This could happen due to the following reasons:\n"
        "* you forgot to download the example data from the repository\n"
        "* the filename is wrong\n"
        "* the file is not located in {1}\n"
        "Download the file from the demandlib repository and copy it to the "
        "right directory.\nAlternatively you can adapt the name of the file "
        "or the name of the directory in the example script."
    )
    print(msg.format(filename, dirname))
    sys.exit(0)

temperature = pd.read_csv(datapath)["temperature"]


# The following dictionary is create by "workalendar"
from workalendar.europe import Germany
cal = Germany()
holidays = dict(cal.holidays(2023))


#ann_demands_per_type = {"efh": 25000, "mfh": 80000, "ghd": 140000}
ann_demands_per_type = {"efh": 25000, "mfh": 33628, "ghd": 140000}

# Create DataFrame for 2023
demand = pd.DataFrame(
    index=pd.date_range(
        datetime.datetime(2023, 1, 1, 0), periods=8760, freq="h"
    )
)

# Single family house (efh: Einfamilienhaus)
demand["efh"] = bdew.HeatBuilding(
    demand.index,
    holidays=holidays,
    temperature=temperature,
    shlp_type="EFH",
    building_class=1,
    wind_class=1,
    annual_heat_demand=ann_demands_per_type["efh"],
    name="EFH",
).get_bdew_profile()

# Plot demand of building
ax = demand.plot()
ax.set_xlabel("Date")
ax.set_ylabel("Heat demand in kW")
ax.set_title("Heat demand (2023)")
plt.show()

print("Annual consumption: \n{}".format(demand.sum()))

print(demand)

# save calculated heat demand to csv file
#demand.to_csv("heat_demand_justus_2023.csv")
