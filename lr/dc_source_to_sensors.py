# Imported Python Transfer Function
import sensor_msgs.msg
import hbp_nrp_cle.tf_framework.tf_lib
@nrp.MapSpikeSource("h_left_dc_source", nrp.brain.sensors[0], nrp.dc_source)
@nrp.MapSpikeSource("f_left_dc_source", nrp.brain.sensors[1], nrp.dc_source)
@nrp.MapSpikeSource("f_right_dc_source", nrp.brain.sensors[2], nrp.dc_source)
@nrp.MapSpikeSource("h_right_dc_source", nrp.brain.sensors[3], nrp.dc_source)
@nrp.Robot2Neuron()
def dc_source_to_sensors (t, f_left_dc_source, f_right_dc_source, h_left_dc_source, h_right_dc_source):
    from random import random as random
    factor = 1e-2
    h_left_dc_source.amplitude = (0.0395 + 0.01 * random()) * factor
    f_left_dc_source.amplitude = (0.0395 + 0.01 * random()) * factor * 2
    f_right_dc_source.amplitude = (0.0395 + 0.01 * random()) * factor
    h_right_dc_source.amplitude = (0.0395 + 0.01 * random()) * factor * 2