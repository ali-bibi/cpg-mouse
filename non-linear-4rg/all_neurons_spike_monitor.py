# Imported Python Transfer Function
@nrp.NeuronMonitor(nrp.brain.record[slice(0, 610, 1)], nrp.spike_recorder)
def all_neurons_spike_monitor(t):
    return True
