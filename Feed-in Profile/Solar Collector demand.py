import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from oemof.tools import economics
from oemof.solph import create_time_index
from pvlib.location import Location

from oemof import solph
from oemof.thermal.solar_thermal_collector import flat_plate_precalc

from _plots import plot_collector_heat


def flat_plate_collector_example():
    # Set paths
    base_path = os.path.dirname(os.path.abspath(os.path.join(__file__)))
    data_path = os.path.join(base_path, "data")
    results_path = os.path.join(base_path, "results")
    if not os.path.exists(results_path):
        os.mkdir(results_path)


    # Parameters for the precalculation
    latitude = 51.500917    # justus jonas location
    longitude = 10.772781
    collector_tilt = 10     # angle of collector tilt
    collector_azimuth = 90  # azimuth angle - east facing
    a_1 = 1.7           # thermal loss parameter 1
    a_2 = 0.016         # thermal loss parameter 2
    eta_0 = 0.73        # optical efficiency of collector
    temp_collector_inlet = 20   # inlet temperature of collector
    delta_temp_n = 10       # temperature difference (collector to ambient)
    
    # Read data file
    periods = 8760
    input_data = pd.read_csv(r"collector.csv").head(periods) #mention the path of the csv file contating collector data

    number_of_time_steps = len(input_data)
    # create time index
    date_time_index = create_time_index(2023, number= number_of_time_steps)
    # Ensure the time index length matches the data length
    if len(date_time_index) > len(input_data):
        date_time_index = date_time_index[:-1]  # Trim the extra row
    
    # Set the datetime index to input_data
    input_data.index = date_time_index


    # Precalculation
    # - calculate global irradiance on the collector area
    # and collector efficiency depending on the
    # temperature difference -
    precalc_data = flat_plate_precalc(
        latitude,
        longitude,
        collector_tilt,
        collector_azimuth,
        eta_0,
        a_1,
        a_2,
        temp_collector_inlet,
        delta_temp_n,
        irradiance_global=input_data["global_horizontal_W_m2"],
        irradiance_diffuse=input_data["diffuse_horizontal_W_m2"],
        temp_amb=input_data["temp_amb"],
    )

    precalc_data.to_csv(
        os.path.join(results_path, "flat_plate_precalcs.csv"), sep=";"
    )
    
    heat_out = precalc_data["collectors_heat"]  #The heat power output of the collector
    # Calculate the total heat output
    total_heat_output = heat_out.sum()
    heat_out.to_csv("solar_collector_justus_2023.csv")
    
    # Print the total heat output
    print(f"Total heat output (Q_coll) for the year: {total_heat_output} Wh/m2")
    plt.figure(figsize=(16,9))
    heat_out.plot()
    plt.show()
    plt.xlabel('Date and Time')
    plt.ylabel('Q_coll [Wh/m2]')
    plt.title('Heat power output of the collector')
    plt.legend()
    
    # Example plot
    plot_collector_heat(precalc_data, periods, eta_0)

if __name__ == "__main__":
    flat_plate_collector_example()