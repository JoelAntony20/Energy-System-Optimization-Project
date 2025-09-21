import pandas as pd
import pvlib
import matplotlib.pyplot as plt

# Fetch PVGIS data (same code as you already have)
result = pvlib.iotools.get_pvgis_hourly(
    latitude=51.500917, 
    longitude=10.772781, 
    start=2023, 
    end=2023, 
    raddatabase="PVGIS-ERA5", 
    components=True, 
    surface_tilt=45, 
    surface_azimuth=90,  # north=0, south=180, east=90, west=270
    outputformat='json', 
    usehorizon=True, 
    userhorizon=None, 
    pvcalculation=False, 
    peakpower=None, 
    pvtechchoice='crystSi', 
    mountingplace='free', 
    loss=0, 
    trackingtype=0, 
    optimal_surface_tilt=False, 
    optimalangles=False, 
    url='https://re.jrc.ec.europa.eu/api/', 
    map_variables=True, 
    timeout=30
)

# Unpack the returned values
pv_data_justus_jonas_2023, inputs, metadata = result

# Print the DataFrame to understand the structure of the data
print(pv_data_justus_jonas_2023.head())

# Assuming pv_data_2023 contains columns like 'ghi', 'dni', 'dhi', etc.
# Plot Global Horizontal Irradiance (GHI), Direct Normal Irradiance (DNI), and Diffuse Horizontal Irradiance (DHI)

plt.figure(figsize=(10, 6))

# # Plot GHI
# plt.plot(pv_data_2023.index, pv_data_2023['ghi'], label='Global Horizontal Irradiance (GHI)', color='orange')

# Plot DNI
plt.plot(pv_data_justus_jonas_2023.index, pv_data_justus_jonas_2023['poa_direct'], label='Direct Normal Irradiance (DNI)', color='blue')

# Plot DHI
plt.plot(pv_data_justus_jonas_2023.index, pv_data_justus_jonas_2023['poa_sky_diffuse'], label='Diffuse Horizontal Irradiance (DHI)', color='green')

# Add labels and title
plt.xlabel('Date and Time')
plt.ylabel('Irradiance (W/m²)')
plt.title('Irradiance Data from PVGIS for 2023 (Wohnheim Justus Jonas)')

# Add a legend
plt.legend()

# Rotate the x-axis labels for better readability
plt.xticks(rotation=45)

# Show the plot
plt.tight_layout()
plt.show()

#  create csv file
# pv_data_justus_jonas_2023.to_csv("pv_data_justus_jonas_2023.csv")