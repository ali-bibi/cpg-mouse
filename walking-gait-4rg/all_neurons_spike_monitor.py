# Imported Python Transfer Function
@nrp.NeuronMonitor(nrp.brain.record, nrp.spike_recorder)
def all_neurons_spike_monitor(t):
    return True