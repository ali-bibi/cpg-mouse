

"""

arguments:
  simulator      neuron, nest, brian or another backend simulator
  -h, --help     show this help message and exit
  --plot-figure  Plot the simulation results to a file
  --fit-curve    Calculate the best-fit curve to the weight-delta_t measurements
  --debug DEBUG  Print debugging information

"""

from __future__ import division
from math import exp
import numpy as np
import neo
from quantities import ms
from pyNN.utility import get_simulator, init_logging, normalized_filename
from pyNN.utility.plotting import DataTable
from pyNN.parameters import Sequence
from random import random as rand
import matplotlib.pyplot as plt
import random

# === Parameters ============================================================

firing_period = 10.0    # (ms) interval between spikes
cell_parameters = {
    "tau_m": 100.0,       # (ms)
    "v_thresh": -55.0,   # (mV)
    "v_reset": -60.0,    # (mV)
    "v_rest": -60.0,     # (mV)
    "cm": 1.0,           # (nF)
    "tau_refrac": firing_period / 2,  # (ms) long refractory period to prevent bursting
}
n = 30                   # number of synapses / number of presynaptic neurons
delta_t = 1.0            # (ms) time difference between the firing times of neighbouring neurons
t_stop = 180000.0
delay = 3.0              # (ms) synaptic time delay
persistence = 30
units = 4

# === Configure the simulator ===============================================

sim, options = get_simulator(("--plot-figure", "Plot the simulation results to a file", {"action": "store_true"}),
                             ("--fit-curve", "Calculate the best-fit curve to the weight-delta_t measurements", {"action": "store_true"}),
                             ("--dendritic-delay-fraction", "What fraction of the total transmission delay is due to dendritic propagation", {"default": 1}),
                             ("--debug", "Print debugging information"))

if options.debug:
    init_logging(None, debug=True)

sim.setup(timestep=1.0, min_delay=1.0, max_delay=delay)


# === Build the network =====================================================

sp1 = [[] for i in range(n)]
sp3 = [[] for i in range(n)]

for i in range(int(t_stop/persistence/delay/units)):
    angle = rand()*90
    sin = np.sin(angle*np.pi/180)
    for j in range(persistence):
        sp1[int(angle/90*n)].append(i*persistence*delay*units + j*delay*units/2 + 2.0)
        for k in range(int(sin*n)):
            sp3[k].append(i*persistence*delay*units + j*delay*units/2 + 2.0)

# presynaptic population
p1 = sim.Population(n, sim.SpikeSourceArray(), label="presynaptic")
# single postsynaptic neuron
p2 = sim.Population(n, sim.IF_cond_exp(**cell_parameters),
                    initial_values={"v": cell_parameters["v_reset"]}, label="postsynaptic")
# drive to the postsynaptic neuron, ensuring it fires at exact multiples of the firing period
p3 = sim.Population(n, sim.SpikeSourceArray(), label="driver")

for i in range(n):
    p1[i:i+1].set(spike_times = sp1[i])
    p3[i:i+1].set(spike_times = sp3[i])

# we set the initial weights to be very small, to avoid perturbing the firing times of the
# postsynaptic neurons
stdp_model = sim.STDPMechanism(
                timing_dependence=sim.SpikePairRule(tau_plus=20.0, tau_minus=20.0,
                                                    A_plus=0.01, A_minus=0.01),
                weight_dependence=sim.AdditiveWeightDependence(w_min=0, w_max=1),
                weight=0.0000001 * (1 + rand()),
                delay=delay,
                dendritic_delay_fraction=1)
connections = sim.Projection(p1, p2, sim.AllToAllConnector(), stdp_model)

# the connection weight from the driver neuron is very strong, to ensure the
# postsynaptic neuron fires at the correct times
driver_connection = sim.Projection(p3, p2, sim.OneToOneConnector(),
                                   sim.StaticSynapse(weight=100.0, delay=delay))

# == Instrument the network =================================================

p1.record('spikes')
p2.record(['spikes', 'v'])

class WeightRecorder(object):
    """
    Recording of weights is not yet built in to PyNN, so therefore we need
    to construct a callback object, which reads the current weights from
    the projection at regular intervals.
    """

    def __init__(self, sampling_interval, projection):
        self.interval = sampling_interval
        self.projection = projection
        self._weights = []

    def __call__(self, t):
        self._weights.append(self.projection.get('weight', format='array', with_address=False))
        return t + self.interval

    def get_weights(self):
        signal = neo.AnalogSignal(self._weights, units='nA', sampling_period=self.interval * ms,
                                  name="weight")
        signal.channel_index = neo.ChannelIndex(np.arange(len(self._weights[0])))
        return signal

weight_recorder = WeightRecorder(sampling_interval=1.0, projection=connections)

# === Run the simulation =====================================================

sim.run(t_stop, callbacks=[weight_recorder])


# === Save the results, optionally plot a figure =============================

filename = normalized_filename("Results", "simple_stdp", "pkl", options.simulator)
p2.write_data(filename, annotations={'script_name': __file__})

weights = weight_recorder.get_weights()
final_weights = np.array(weights[-1])
print("Final weights: %s" % final_weights)

np.savetxt('test.txt', final_weights)

if options.plot_figure:

    fig, axis = plt.subplots()
    heatmap = axis.pcolor(final_weights, cmap=plt.cm.Blues)
    axis.set_xlabel('Output layer')
    axis.set_ylabel('Input layer')
    #plt.imshow(final_weights, cmap='hot', interpolation='nearest')
    plt.colorbar(heatmap)
    plt.show()

    fig.savefig(filename.replace("pkl", "svg"), dpi=300, format="svg")



# === Clean up and quit ========================================================

sim.end()