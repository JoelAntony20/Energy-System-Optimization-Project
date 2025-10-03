# Energy System   Modelling of Buildings
This is an academic project checking the feasibility of integrating Renewable Energy Sources to commercial buildings using open source Python packages such as [RAMP](https://rampdemand.readthedocs.io/en/latest/intro.html), [pvlib-Python](https://pvlib-python.readthedocs.io/en/stable/index.html), and [OEMOF](https://oemof.org/).
# Table of Contents
1. [Introduction](#introduction)
2. [Load Profile](#load-profile)
    - [Electricity Profile](#electricity-profile)
    - [Heat Demand Profile](#heat-demand-profile)
3. [Feed-in Profile](#feed-in-profile)
     - [PV Output](#pv-output)
     - [Heat Power Output](#heat-power-output)
4. [Energy Optimization](#energy-optimization)


# Introduction
This projects aims to do the modelling of energy systems using the renewable energy sources such as Solar energy and photovoltaic system, and to optimize the energy system to meet the energy demands of the stakeholders. The first task is to create the load profiles and feed-in profiles, and use these energy data to optimize the system.

The load profiles implemented during this project include the electricity profile, PV demand, and solar thermal energy demand. Mostly the load profiles were created using Python and the related packages. RAMP, a package in Python was used to create the electricity profile, PvlibPython was used to create the PV demand profile and OEMOF was used to check the energy system feasibility.
The sources of renewable energy preferred by the clients were mainly photovoltaics and solar thermal collectors for meeting the electricity and heating demands respectively. This information was received by conducting a survey

# Load Profile
The Load profiles include electricity demand and heat demand, which is then used to optimize the energy system.

## Electricity profile
The electricity profile was created by using the RAMP package inside Python. Any user-driven demand for energy time series can be stochastically simulated using RAMP, an open-source software suite built on Python that requires only a few basic inputs. The software actually only requires a fundamental knowledge of the expected patterns of user activity and the inputs that are owned by the user, such as electrical appliances like refrigerators and lights inside buildings[^1]. 
[^1]: Francesco Lombardi. RAMP project. accessed 13-02-2025. 2019. url: https : / / rampdemand.org/.

Initial steps for creating the electricity profile include understanding the user behavior of the various electrical appliances and details of these appliances installed in the building. The number of appliances and their time of usage was calculated as per the details shared with the survey, moreover, some vital information was assumed as it was not provided during the survey. The electricity profile was implemented separately for summer and winter as the usage of the electrical appliances differs seasonally.

## Heat Demand profile
The heat demand profile is created using [demandlib](https://github.com/oemof/demandlib/blob/dev/examples/heat_demand_example.py), where we need to input the temperature data of the building's location and select the type of building, for example if it is a single family, multi-family building or industry.

# Feed in Profile
The feed-in profiles for the project include PV output and heat power output from the solar thermal collectors.

## PV Output
+ The first step is to calculate the irradiance present in the region under consideration, for the project pvlib library using the PVGIS module[^2] was utilized for this purpose.
[^2]: Holmgren, W., Hansen, C., and Mikofski, M. “pvlib python: a python package for modeling solar energy systems.” Journal of Open Source Software, 3(29), 884, (2018). DOI: 10.21105/joss.00884.
+ The next step is to retrieve the irradiation, temperature and wind speed data from the PVGIS module[^2].
+ The final step is to pre-process the PV data retrieved to use only the necessary data and name them properly for excel file, so the data can be correctly read by pvlib-Python during the PV output calculation.
+ Modelchain module in the pvlib library[^2] is used for the PV output calculattion, the process include:
    * Selection of the location.
    * Selection of the PV module and inverter specifications.
    * Reading the PV data retrieved.
## Heat Power Output 
The oemof.thermal library[^3] calculates the heat power output for the selected solar collectors, when the required information are given, such as a1, a2, diffuse radiation, global radiation, and temperature.
[^3]: oemof developer group. (2020). oemof-thermal: Thermal energy components in oemof (v0.0.1). Zenodo. https://doi.org/10.5281/zenodo.3606385.

# Energy Optimization
The simulation of all energy resources can be executed only after the energy system has been designed. The energy system is the main model containing the energy elements. The initial step in this process is correctly defining the nodes. The energy system is made up of nodes and there are two types of nodes - components and buses. The bus contains all flows in and out. The components need to be connected to one or more buses and this connection is called flow. The components are source, sink, converter, and storage. The full description of the energy system can be found in [oemof user's guide](https://oemof-solph.readthedocs.io/en/v0.5.7/usage.html#solph-components). The next step of the simulation is to add the required buses and components to the energy system. The PV system and the solar thermal collector energy yield are the renewable energy sources considered in this simulation, and the calculated feed-in profiles of these respective energy sources are also fed as the fixed data for the simulation. The load profiles are also required, such as the temperature, electricity demand, and heat demand hourly information[^4].
[^4]: Krien, U., Kaldemeyer, C., Günther, S., Schönfeldt, P., Simon, H., Launer, J., Röder, J., Möller, C., Kochems, J., Huyskens, H., Developer, A., Schachler, B., Pl, F., Sayadi, S., Duc, P.-F., Endres, J., Büllesbach, F., Fuhrländer, D., Developer, A., … Freißmann, J. (2025). oemof.solph (v0.6.0). Zenodo. https://doi.org/10.5281/zenodo.15607673.
