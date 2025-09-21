# importing functions
# electricity profile for Wohnhaus Justus Jonas
import matplotlib.pyplot as plt
from ramp import User, UseCase, Appliance, UseCase, get_day_type
import pandas as pd
household_jonas= User(
    user_name="Household_sommer",
    num_users=10,
)
# add_appliance is meth
indoor_bulb = household_jonas.add_appliance(
    name="Indoor Light Bulb",  # the name of the appliance
    number=5,  # how many of this appliance each user has in this user category
    power=7,  # the power (in Watt) of each single appliance. RAMP does not deal with units of measures, you should check the consistency of the unit of measures throughout your model
    num_windows=2,  # how many usage time windows throughout the day?
    func_time=60,  # the total usage time of appliances
    func_cycle=10,  # the minimum usage time after a switch on event
    window_1=[360, 480],  # from 6am to 8am
    window_2=[1200, 1380],  # from 8pm to 11pm
    random_var_w=0.35,  # Variability of the windows in percentage
    time_fraction_random_variability=0.2,  # randomizes the total time the appliance is on (between 0 and 1)
)
phone_charger = household_jonas.add_appliance(
    name="Phone Charger",
    number=1,
    power=15,
    num_windows=1,
    func_time=100,  #  30 minutes
    func_cycle=100,
    window_1=[600, 1320],  # from 6am to 8am
    random_var_w=0.35,  # Variability of the windows in percentage
    time_fraction_random_variability=0.2,  # randomizes the total time the appliance is on (between 0 and 1)
)
Monitor = household_jonas.add_appliance(
    name="Monitor",
    number=1,
    power=15,
    num_windows=2,
    func_time=120,  # 3 hours
    func_cycle=30, #atleast 3 hours will be used after turning on
    occasional_use=1,  # always present in the mix of appliances,
    window_1 = [600,840],
    window_2=[1080, 1320],  # from 6pm to 11pm
    random_var_w=0.35,  # Variability of the windows in percentage
    time_fraction_random_variability=0.2,  # randomizes the total time the appliance is on (between 0 and 1)
)

fridge = household_jonas.add_appliance(
    name="Fridge",
    number=1,
    power=200,
    num_windows=1,
    func_time=1440,
    time_fraction_random_variability=0,
    func_cycle=40,
    fixed="yes",
    fixed_cycle=3,  # number of cycles
)

# setting the functioning windows
fridge.windows([0, 1440])  # always on during the whole day, for all days of the year

# assiging the specific cycles
# first cycle: standard cycle
fridge.specific_cycle_1(
    p_11=200,  # power level for the first operation segment
    t_11=10,  # duration of the first operation segment
    p_12=5,  # power level for the second operation segment
    t_12=30,  # duration of the second operation segment
    r_c1=0,  # random variability assigned to the duration of each segment
)
# second cycle: intermediate cycle
fridge.specific_cycle_2(p_21=200, t_21=20, p_22=5, t_22=20, r_c2=0)

# third cycle: intensive cycle
fridge.specific_cycle_3(p_31=200, t_31=30, p_32=5, t_32=10, r_c3=0)

# defining cycle behaviour
fridge.cycle_behaviour(
    cw11=[0, 299], cw12=[1201, 1440], cw21=[300, 479], cw31=[480, 1200]
)
Mixer = household_jonas.add_appliance(
    name="Mixer",
    number=1,
    power=800,
    num_windows=1,
    func_time=5,  # 1 minute
    func_cycle=5, #atleast 1 min will be used after turning on
    occasional_use=0.3,  # always present in the mix of appliances,
    random_var_w=0.35,  # Variability of the windows in percentage
    time_fraction_random_variability=0.2,  # randomizes the total time the appliance is on (between 0 and 1)
    window_1=[780, 1200],  # from 7pm to 8pm
)
#power for cooking
# soup for lunch
soup_2 = household_jonas.add_appliance(
    name="soup for lunch",
    power=1200,
    func_time=50,
    func_cycle=50,
    fixed_cycle=1,
    window_1=[540,840], # 11am to 13pm
    p_11=1200,  # power of the first cycle
    t_11=30,  # time needed for the first cycle
    p_12=750,  # power of the second cycle
    t_12=20,  # time needed for the second cycle
    cw11=[540,840], # 11am to 13pm,
)
# rice for dinner
rice_2 = household_jonas.add_appliance(
    name="rice for dinner",
    power=1200,
    func_time=60,
    func_cycle=60,
    fixed_cycle=1,
    window_1=[900, 1200],  # from 7pm to 8pm
    p_11=1200,  # power of the first cycle
    t_11=30,  # time needed for the first cycle
    p_12=600,  # power of the second cycle
    t_12=30,  # time needed for the second cycle
    cw11=[1140, 1200],  # from 7pm to 8pm
) 

Washing_machine = household_jonas.add_appliance(
    name="Washing Machine",
    number=1,
    power=2000,
    num_windows=1,
    func_time=50,
    time_fraction_random_variability=0,
    func_cycle=50,
    fixed_cycle=1,
    window_1=[600, 1200],  # from 7pm to 8pm
    occasional_use=0.7,
    p_11=2000,  # power of the washing cycle
    t_11=30,  # time needed for the washing cycle
    p_12=1000,  # power of the rotating and drying cycle
    t_12=20,  # time needed for the rotating and drying cycle
    cw11=[600, 1200],  # from 7pm to 8pm
)
fan = household_jonas.add_appliance(
    name = "Fan",
    number = 2,
    power=50,
    num_windows=2,  # how many usage time windows throughout the day?
    func_time=420,  # the total usage time of appliances 7 hours
    func_cycle=60,  # the minimum usage time after a switch on 
    window_2 = [0,360],  #12am to 6am
    window_1=[1200, 1440],  # from 8pm to 12pm
    random_var_w=0.35,  # Variability of the windows in percentage
    time_fraction_random_variability=0.2,  # randomizes the total time the appliance is on (between 0 and 1)

)

print(household_jonas)


###################################  WINTER  ####################################################################

household_jonas_winter = User(
    user_name="Household_winter",
    num_users=10,
)

# add_appliance
indoor_bulb = household_jonas_winter.add_appliance(
    name="Indoor Light Bulb",  # the name of the appliance
    number=5,  # how many of this appliance each user has in this user category
    power=7,  # the power (in Watt) of each single appliance. RAMP does not deal with units of measures, you should check the consistency of the unit of measures throughout your model
    num_windows=2,  # how many usage time windows throughout the day?
    func_time=420,  # the total usage time of appliances
    func_cycle=30,  # the minimum usage time after a switch on event
    window_1=[300, 660],  # from 6am to 8am
    window_2=[960, 1380],  # from 8pm to 11pm
    random_var_w=0.35,  # Variability of the windows in percentage
    time_fraction_random_variability=0.2,  # randomizes the total time the appliance is on (between 0 and 1)
)
phone_charger = household_jonas_winter.add_appliance(
    name="Phone Charger",
    number=1,
    power=15,
    num_windows=1,
    func_time=120,  #  30 minutes
    func_cycle=120,
    window_1=[360, 1320],  # from 6am to 8am
    random_var_w=0.35,  # Variability of the windows in percentage
    time_fraction_random_variability=0.2,  # randomizes the total time the appliance is on (between 0 and 1)
)
Monitor = household_jonas_winter.add_appliance(
    name="Monitor",
    number=1,
    power=15,
    num_windows=2,
    func_time=300,  # 3 hours
    func_cycle=60, #atleast 3 hours will be used after turning on
    occasional_use=1,  # always present in the mix of appliances,
    window_1 = [420,720],
    window_2=[900, 1320],  # from 6pm to 11pm
    random_var_w=0.35,  # Variability of the windows in percentage
    time_fraction_random_variability=0.2,  # randomizes the total time the appliance is on (between 0 and 1)
)

fridge = household_jonas_winter.add_appliance(
    name="Fridge",
    number=1,
    power=200,
    num_windows=1,
    func_time=1440,
    time_fraction_random_variability=0,
    func_cycle=40,
    fixed="yes",
    fixed_cycle=3,  # number of cycles
)

# setting the functioning windows
fridge.windows([0, 1440],[0,0])  # always on during the whole day, for all days of the year

# assiging the specific cycles
# first cycle: standard cycle
fridge.specific_cycle_1(
    p_11=200,  # power level for the first operation segment
    t_11=10,  # duration of the first operation segment
    p_12=5,  # power level for the second operation segment
    t_12=30,  # duration of the second operation segment
    r_c1=0,  # random variability assigned to the duration of each segment
)
# second cycle: intermediate cycle
fridge.specific_cycle_2(p_21=200, t_21=20, p_22=5, t_22=20, r_c2=0)

# third cycle: intensive cycle
fridge.specific_cycle_3(p_31=200, t_31=30, p_32=5, t_32=10, r_c3=0)

# defining cycle behaviour
fridge.cycle_behaviour(
    cw11=[480, 1200], cw12=[0,0], cw21=[300, 479],cw22=[0,0],cw31=[0, 299], cw32=[1201, 1440]
) 
Mixer = household_jonas_winter.add_appliance(
    name="Mixer",
    number=1,
    power=800,
    num_windows=1,
    func_time=5,  # 1 minute
    func_cycle=5, #atleast 1 min will be used after turning on
    occasional_use=0.3,  # always present in the mix of appliances,
    random_var_w=0.35,  # Variability of the windows in percentage
    time_fraction_random_variability=0.2,  # randomizes the total time the appliance is on (between 0 and 1)
    window_1=[540, 1200],  # from 7pm to 8pm
)
#power for cooking
# soup for lunch
soup_2 = household_jonas_winter.add_appliance(
    name="soup for lunch",
    power=1200,
    func_time=50,
    func_cycle=50,
    fixed_cycle=1,
    window_1=[540,840], # 11am to 13pm
    p_11=1200,  # power of the first cycle
    t_11=30,  # time needed for the first cycle
    p_12=750,  # power of the second cycle
    t_12=20,  # time needed for the second cycle
    cw11=[540,840], # 11am to 13pm,
)
# rice for dinner
rice_2 = household_jonas_winter.add_appliance(
    name="rice for dinner",
    power=1200,
    func_time=100,
    func_cycle=100,
    fixed_cycle=1,
    window_1=[900, 1320],  # from 7pm to 8pm
    p_11=1200,  # power of the first cycle
    t_11=50,  # time needed for the first cycle
    p_12=600,  # power of the second cycle
    t_12=50,  # time needed for the second cycle
    cw11=[900, 1320],  # from 7pm to 8pm
) 

Washing_machine = household_jonas_winter.add_appliance(
    name="Washing Machine",
    number=1,
    power=2000,
    num_windows=1,
    func_time=120,
    time_fraction_random_variability=0,
    func_cycle=50,
    fixed_cycle=1,
    window_1=[540, 1320],  # from 7pm to 8pm
    occasional_use=0.7,
    p_11=2000,  # power of the washing cycle
    t_11=30,  # time needed for the washing cycle
    p_12=1000,  # power of the rotating and drying cycle
    t_12=20,  # time needed for the rotating and drying cycle
    cw11=[540, 1320],  # from 7pm to 8pm
)
fan = household_jonas_winter.add_appliance(
    name = "Fan",
    number = 2,
    power=50,
    num_windows=2,  # how many usage time windows throughout the day?
    func_time=420,  # the total usage time of appliances 7 hours
    func_cycle=60,  # the minimum usage time after a switch on 
    window_2 = [0,600],  #12am to 6am
    window_1=[900, 1440],  # from 8pm to 12pm
    random_var_w=0.35,  # Variability of the windows in percentage
    time_fraction_random_variability=0.2,  # randomizes the total time the appliance is on (between 0 and 1)

)

print(household_jonas_winter)

# Generate summer profile
use_case_summer = UseCase(
    users=[household_jonas],  
    date_start="2024-04-01",  
    date_end="2024-09-30"
)
summer_profile = use_case_summer.generate_daily_load_profiles()
summer_profile = summer_profile/10  # number of users: 10
summer_profile = pd.DataFrame(
    summer_profile, columns=["Household_sommer"], index=use_case_summer.datetimeindex
)

# Use case for October to December 2020 (Winter)
use_case_winter_oct_dec = UseCase(
    users=[household_jonas_winter],
    date_start="2024-10-01",
    date_end="2024-12-31"
)

# Use case for January to March 2020 (Winter)
use_case_winter_jan_mar = UseCase(
    users=[household_jonas_winter],
    date_start="2024-01-01",
    date_end="2024-03-31"
)

winter_profile_1 = use_case_winter_jan_mar.generate_daily_load_profiles()
winter_profile_1 = winter_profile_1/10
winter_profile_1 = pd.DataFrame(
    winter_profile_1, columns=["Household_winter"], index=use_case_winter_jan_mar.datetimeindex
)


winter_profile_2 = use_case_winter_oct_dec.generate_daily_load_profiles()
winter_profile_2 = winter_profile_2/10
winter_profile_2 = pd.DataFrame(
    winter_profile_2, columns=["Household_winter"], index=use_case_winter_oct_dec.datetimeindex
)

# Combine winter profiles
winter_profile_df = pd.concat([winter_profile_1, winter_profile_2])
winter_profile_df = winter_profile_df.resample("15min").mean()
summer_profile = summer_profile.resample("15min").mean()



# Plot both profiles in a single graph
# Correcting the column name for winter profile
plt.figure(figsize=(10, 5))
#winter_profile_df.plot()
plt.plot(summer_profile.index, summer_profile["Household_sommer"], label="Summer Profile", color="orange")
plt.plot(winter_profile_df.index, winter_profile_df["Household_winter"], label="Winter Profile", color="blue")  # Fixed name
plt.xlabel("Time")
plt.ylabel("Electricity Consumption (Wh)")
plt.title("Electricity Load Profile - Summer vs Winter")
plt.legend()
plt.grid(True)
plt.show()

#(summer_profile["Household_sommer"].sum()+winter_profile_df["Household_winter"].sum())/1000   run in console to get total power

######################################### SCALING    ##########################

# Scaling the calculated profile to a total electricity demand of 2300kWh
total_profile = pd.concat([winter_profile_df,summer_profile])
total_profile = (total_profile/9629976.135)* 2300000  # the total demand from above calculation is 9621 kWh, and the total is scaled to 2300kWh
plt.figure(figsize=(10, 5))
total_profile.plot()
plt.xlabel("Time")
plt.ylabel("Electricity Consumption (Wh)")
plt.title("Wohnheim Justus Jonas (Electricity profile)")
plt.legend()
plt.show()

#   calculating total demand and saving to csv file
total_demand = pd.concat([winter_profile_1, summer_profile, winter_profile_2])
total_demand  = (total_demand/9629976.135)*9629976.135
total_demand = total_demand.resample("h").mean()
plt.figure(figsize=(10, 5))
total_demand.plot()
plt.show()
# total_demand.to_csv("el_demand_wohnheim_justus_2023.csv")     #remove the comment to save the csv file

















