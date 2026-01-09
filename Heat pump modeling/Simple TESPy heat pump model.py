from tespy.components import SimpleHeatExchanger, CycleCloser, Compressor, Valve
from tespy.connections import Connection
from tespy.networks import Network

import pandas as pd
import numpy as np

from matplotlib import pyplot as plt

wf = "R290"
nwk = Network(p_unit="bar", T_unit="C", iterinfo=False)

cp = Compressor("compressor")
ev = SimpleHeatExchanger("evaporator")
cd = SimpleHeatExchanger("condenser")
va = Valve("expansion valve")
cc = CycleCloser("cycle closer")


c0 = Connection(va, "out1", cc, "in1", label="0")
c1 = Connection(cc, "out1", ev, "in1", label="1")
c2 = Connection(ev, "out1", cp, "in1", label="2")
c3 = Connection(cp, "out1", cd, "in1", label="3")
c4 = Connection(cd, "out1", va, "in1", label="4")

nwk.add_conns(c0, c1, c2, c3, c4)

# connections
c2.set_attr(T=2)
c4.set_attr(T=40)

# components
cp.set_attr(eta_s=0.675)
cd.set_attr(Q=-9.1e3)

# connections
c2.set_attr(fluid={wf: 1}, x=1.0)
c4.set_attr(x=0.0)

# components
cd.set_attr(pr=1)
ev.set_attr(pr=1)

nwk.solve("design")
nwk.print_results()

# calculate the cop
cp.P.val  # work at compressor
cop = abs(cd.Q.val) / cp.P.val  # total heat required at condensot/ work at compressor
cop
print(cop)

# read temperature data csv file
df = pd.read_csv(
    r"C:\Users\joeak\Downloads\Hochschule Nordhausen\Sem_2\Scientific Project\Energy system Optimization\Energy data\temp_justus_2023.csv"
)
df.set_index("timestep", inplace=True)
df["COP"] = np.nan  #create a column for COP

#solve the model using the temperature from data to calculate COP and carnot COP
for ts, T_amb in df["temperature"].items():
    c2.set_attr(T=T_amb - 5)

    try:
        nwk.solve("design")
        df.loc[ts, "COP"] = abs(cd.Q.val) / cp.P.val
    except:
        df.loc[ts, "COP"] = np.nan

#Plot COP vs timstep
plt.figure()
plt.plot(df.index, df["COP"])
plt.xlabel("Timestep")
plt.ylabel("COP")
plt.title("Heat Pump COP over Time")
plt.grid(True)
plt.show()

#Plot COP vs Temperature
plt.figure()
plt.scatter(df["temperature"], df["COP"], s=10)
plt.xlabel("Ambient temperature (°C)")
plt.ylabel("COP")
plt.title("COP vs Ambient Temperature")
plt.grid(True)
plt.show()

#calculate carnot COP and efficiency factor
df["COP_carnot"] = c4.T.val_SI / (c4.T.val - c2.T.val)
df["eta"] = df["COP"] / df["COP_carnot"]

#plot efficiency
plt.figure()
plt.plot(df.index, df["eta"])
plt.xlabel("Timestep")
plt.ylabel("Efficiency factor")
plt.grid(True)
plt.show()
