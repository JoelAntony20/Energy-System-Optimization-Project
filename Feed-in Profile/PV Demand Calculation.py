import pvlib
from pvlib.modelchain import ModelChain
from pvlib.location import Location
from pvlib.pvsystem import PVSystem
from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS

import pandas as pd
import matplotlib.pyplot as plt


location = Location(latitude=51.500917, longitude = 10.772781, tz=  'Europe/Berlin', altitude=80 , name= 'Wohnhaus Justus Jonas' )

sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')
cec_inverters = pvlib.pvsystem.retrieve_sam('CECInverter')

module = sandia_modules['Canadian_Solar_CS5P_220M___2009_']
inverter = cec_inverters['ABB__TRIO_20_0_TL_OUTD_S_US_480__480V_']

temperature_parameters = TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']

system = PVSystem(surface_tilt=45, surface_azimuth=90, module_parameters=module,  
                  inverter_parameters=inverter, temperature_model_parameters=temperature_parameters, 
                  modules_per_string=20, strings_per_inverter=4)

modelchain = ModelChain(system, location)

tmy = pd.read_csv("Pvlib_data_justus_jonas_2023.csv", index_col=0)
tmy.index = pd.to_datetime(tmy.index)
modelchain.run_model(tmy)
plt.figure(figsize=(16,9))
modelchain.results.ac.plot()
plt.show()

#Add detaila in plot
plt.xlabel('Date and Time')
plt.ylabel('AC Power (W)')
plt.title('Energy yield from PV')
# plt.legend()

plt.figure(figsize=(16,9))
modelchain.results.ac.resample("M").sum().plot()
plt.show()
plt.xlabel('Date and Time')
plt.ylabel('AC Power (Wh)')
plt.title('Energy yield from PV (Monthly data)')
# plt.legend()

# modelchain.results.ac.to_csv("Power_PV_Justus_Jonas_15360.csv")