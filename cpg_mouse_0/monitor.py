# Imported Python Transfer Function
@nrp.MapSpikeSink("left_wheel_neuron", nrp.brain.actors[0], nrp.leaky_integrator_alpha)def monitor(t):
    if t % 2 < 0.02:
        clientLogger.info('Time: ', t)
    return True
