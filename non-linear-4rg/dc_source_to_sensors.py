# Imported Python Transfer Function
import sensor_msgs.msg
import hbp_nrp_cle.tf_framework.tf_lib
@nrp.MapSpikeSource("f_left_dc_source", nrp.brain.sensors[0], nrp.dc_source)
@nrp.MapSpikeSource("f_right_dc_source", nrp.brain.sensors[1], nrp.dc_source)
@nrp.MapSpikeSource("h_left_dc_source", nrp.brain.sensors[2], nrp.dc_source)
@nrp.MapSpikeSource("h_right_dc_source", nrp.brain.sensors[3], nrp.dc_source)
@nrp.MapSpikeSource("phase", nrp.brain.sensors[4], nrp.dc_source)
@nrp.Robot2Neuron()
def dc_source_to_sensors(t, phase, f_left_dc_source, f_right_dc_source, h_left_dc_source, h_right_dc_source):
    from random import random as random
    # 0.6e2 -> 2.2e2
    factor = 0.6e2
    f_left_dc_source.amplitude = (0.0395 + 0.001 * random()) * factor
    f_right_dc_source.amplitude = (0.0395 + 0.001 * random()) * factor
    h_left_dc_source.amplitude = (0.0395 + 0.001 * random()) * factor
    h_right_dc_source.amplitude = (0.0395 + 0.001 * random()) * factor
    phase.amplitude = (0.0395 + 0.001 * random()) * factor
