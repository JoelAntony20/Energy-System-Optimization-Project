import logging
import os
import pprint as pp
from oemof.tools import economics
from oemof import solph
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from oemof.tools import logger

from oemof.solph import EnergySystem
from oemof.solph import Model
from oemof.solph import buses
from oemof.solph import components
from oemof.solph import create_time_index
from oemof.solph import flows
from oemof.solph import helpers
from oemof.solph import processing
from oemof.solph import views

STORAGE_LABEL = "battery_storage"
HEAT_STORAGE_LABEL = "heat_storage"

def plot_figures_for(element: dict) -> None:
    figure, axes = plt.subplots(figsize=(10, 5))
    element["sequences"].plot(ax=axes, kind="line", drawstyle="steps-post")
    plt.legend(
        loc="upper center",
        prop={"size": 8},
        bbox_to_anchor=(0.5, 1.25),
        ncol=2,
    )
    figure.subplots_adjust(top=0.8)
    plt.show()

def main(dump_and_restore=False):
    # For models that need a long time to optimise, saving and loading the
    # EnergySystem might be advised. By default, we do not do this here. Feel
    # free to experiment with this once you understood the rest of the code.
    dump_results = restore_results = dump_and_restore

    # *************************************************************************
    # ********** PART 1 - Define and optimise the energy system ***************
    # *************************************************************************
    
    data = pd.read_csv(r"Data_1_wohnheim_justus.csv") # mention the path of the csv file containing all the load and feed-in data
    periods = 8760
    number_of_time_steps = len(data)
    demand = list(data["heat demand"].iloc[:number_of_time_steps])
    solver = "cbc"  # 'glpk', 'gurobi',....
    debug = False  # Set number_of_timesteps to 3 to get a readable lp-file.
    solver_verbose = False  # show/hide solver output

    # initiate the logger (see the API docs for more information)
    logger.define_logging(
        logfile="oemof_justus.log",
        screen_level=logging.INFO,
        file_level=logging.INFO,
    )

    logging.info("Initialize the energy system")
    date_time_index = create_time_index(2023, number=number_of_time_steps)

    # create the energysystem and assign the time index
    energysystem = EnergySystem(
        timeindex=date_time_index, infer_last_interval=False
    )
    ##########################################################################
    # Create oemof objects
    ##########################################################################

    logging.info("Create oemof objects")

    # The bus objects were assigned to variables which makes it easier to
    # connect components to these buses (see below).
    
    # create thermal bus
    bus_thermal = buses.Bus(label="thermal")

    # create electricity bus
    bus_electricity = buses.Bus(label="electricity")
    
    # create natural_gas bus
    bus_gas = buses.Bus(label="natural_gas")
    
    # create solar bus
    bus_solar = buses.Bus(label="solar")

    # adding the buses to the energy system
    energysystem.add(bus_thermal, bus_gas, bus_electricity, bus_solar)
    
    # create fixed source object representing pv power plants
    energysystem.add(
        components.Source(
            label="pv",
            outputs={
                bus_electricity: flows.Flow(
                    fix=data["pv"], nominal_value=15360  # nominal value here is the peak capacity
                )
            },
        )
    )
    # create fixed source object representing solar thermal collector
    energysystem.add(
        components.Source(
            label="solar thermal heat",
            outputs={
                bus_solar: flows.Flow(
                    fix=data["collector_heat"], nominal_value=1    # size of collector= 10 m2
                )
            },
        )
    )
    
    # create fixed source object representing electricity grid
    energysystem.add(
        components.Source(
            label="electricity grid",
            outputs={
                bus_electricity: flows.Flow(
                    variable_costs= 0.41       #   €/kWh, assuming 41 cents for one kWh, we get 1058 euro (annual), demand 2580kWh
                )
            },
        )
    )
    # create fixed source object representing backup system for solar thermal collectors
    energysystem.add(
        components.Source(
            label="backup thermal",
            outputs={
                bus_thermal: flows.Flow(
                    variable_costs= 0.04        # €/kWh, assume 4 cents for converting gas to 1 kWh electricity
                )           #     assuming total backup system costs € 40
            },
        )
    )
    
    # create excess component for the electricity bus to allow overproduction
    energysystem.add(
        components.Sink(
            label="heat_demand",
            inputs={bus_thermal: flows.Flow(fix=demand, nominal_value=1)},  # nominal value as 1, since no normalization of the data
        )
    )

    # create excess component for the electricity bus to allow overproduction
    energysystem.add(
        components.Sink(
            label="excess_solar_heat",
            inputs={bus_solar: flows.Flow()},
        )
    )

    # create simple sink object representing the electrical demand
    # nominal_value is set to 1 because demand_el is not a normalised series
    energysystem.add(
        components.Sink(
            label="demand",
            inputs={
                bus_electricity: flows.Flow(
                    fix=data["demand_el"], nominal_value=1
                )
            },
        )
    )

    # create excess component for the electricity bus to allow overproduction
    energysystem.add(
        components.Sink(
            label="excess_bus_electricity",
            inputs={bus_electricity: flows.Flow()},
        )
    )

    # create simple converter object representing a solar collector
    energysystem.add(
        components.Converter(
            label="solar collector",
            inputs={bus_solar: flows.Flow()},
            outputs={
                bus_thermal: flows.Flow()
            },
            conversion_factors={
            bus_solar: 1,
            bus_electricity: 0.02 * (1 - 0.05), # electrical consumption = 0.02, peripheral losses = 0.05
            bus_thermal: 1 - 0.05,
            },
        )
    )
    
    # create storage object representing a battery
    nominal_capacity = 57600
    nominal_value = nominal_capacity / 6

    battery_storage = components.GenericStorage(
        nominal_storage_capacity=nominal_capacity,
        label=STORAGE_LABEL,
        inputs={bus_electricity: flows.Flow(nominal_value=nominal_value)},
        outputs={
            bus_electricity: flows.Flow(
                nominal_value=nominal_value, variable_costs=0.001
            )
        },
        loss_rate=0.00,
        initial_storage_level=None,
        inflow_conversion_factor=1,
        outflow_conversion_factor=0.8,
    )
    
    # create storage object representing a heat storage
    costs_storage = economics.annuity(20, 20, 0.06) # oemof.tools.economics.annuity(capex, n, wacc, u=None, cost_decrease=0)
    
    heat_storage = components.GenericStorage(
        label= HEAT_STORAGE_LABEL,
        inputs={bus_thermal: flows.Flow()},
        outputs={bus_thermal: flows.Flow()},
        loss_rate=0.0001,
        inflow_conversion_factor=0.98,
        outflow_conversion_factor=0.98,
        investment=solph.Investment(ep_costs=costs_storage),
    )

    energysystem.add(battery_storage, heat_storage)


    ##########################################################################
    # Optimise the energy system and plot the results
    ##########################################################################

    logging.info("Optimise the energy system")

    # initialise the operational model
    energysystem_model = Model(energysystem)

    # This is for debugging only. It is not(!) necessary to solve the problem
    # and should be set to False to save time and disc space in normal use. For
    # debugging the timesteps should be set to 3, to increase the readability
    # of the lp-file.
    if debug:
        file_path = os.path.join(
            helpers.extend_basic_path("lp_files"), "oemof_wohnheim_justus.lp"
        )
        logging.info(f"Store lp-file in {file_path}.")
        io_option = {"symbolic_solver_labels": True}
        energysystem_model.write(file_path, io_options=io_option)

    # if tee_switch is true solver messages will be displayed
    logging.info("Solve the optimization problem")
    energysystem_model.solve(
        solver=solver, solve_kwargs={"tee": solver_verbose}
    )

    logging.info("Store the energy system with the results.")

    # The processing module of the outputlib can be used to extract the results
    # from the model transfer them into a homogeneous structured dictionary.

    # add results to the energy system to make it possible to store them.
    energysystem.results["main"] = processing.results(energysystem_model)
    energysystem.results["meta"] = processing.meta_results(energysystem_model)

    # The default path is the '.oemof' folder in your $HOME directory.
    # The default filename is 'es_dump.oemof'.
    # You can omit the attributes (as None is the default value) for testing
    # cases. You should use unique names/folders for valuable results to avoid
    # overwriting.
    if dump_results:
        energysystem.dump(dpath=None, filename=None)

    # *************************************************************************
    # ********** PART 2 - Processing the results ******************************
    # *************************************************************************

    # Saved data can be restored in a second script. So you can work on the
    # data analysis without re-running the optimisation every time. If you do
    # so, make sure that you really load the results you want. For example,
    # if dumping fails, you might exidentially load outdated results.
    if restore_results:
        logging.info("**** The script can be divided into two parts here.")
        logging.info("Restore the energy system and the results.")

        energysystem = EnergySystem()
        energysystem.restore(dpath=None, filename=None)

    # define an alias for shorter calls below (optional)
    results = energysystem.results["main"]
    storage = energysystem.groups[STORAGE_LABEL]

    # print a time slice of the state of charge
    start_time = datetime(2023, 2, 25, 8, 0, 0)
    end_time = datetime(2023, 2, 25, 17, 0, 0)

    print("\n********* State of Charge (slice) *********")
    print(f"{results[(storage, None)]['sequences'][start_time : end_time]}\n")

    # get all variables of a specific component/bus
    custom_storage = views.node(results, STORAGE_LABEL)
    electricity_bus = views.node(results, "electricity")
    thermal_bus =  views.node(results, "thermal")
    
    # plot the time series (sequences) of a specific component/bus
    plot_figures_for(custom_storage)
    plot_figures_for(electricity_bus)
    plot_figures_for(thermal_bus)
        

    # print the solver results
    print("********* Meta results *********")
    pp.pprint(f"{energysystem.results['meta']}\n")

    # print the sums of the flows around the electricity bus
    print("********* Main results *********")
    print(electricity_bus["sequences"].sum(axis=0))
    print(thermal_bus["sequences"].sum(axis=0))


if __name__ == "__main__":
    main()