# Imported Python Transfer Function
import sensor_msgs.msg
import hbp_nrp_cle.tf_framework.tf_lib
@nrp.MapSpikeSource("f_left_dc_source", nrp.brain.record[10:20], nrp.dc_source)
@nrp.MapSpikeSource("f_right_dc_source", nrp.brain.record[20:30], nrp.dc_source)
@nrp.Robot2Neuron()
def dc_source_to_sensors(t, f_left_dc_source, f_right_dc_source):
    from random import random as random
    
    f_right_dc_source.amplitude = 24.0395 * (1 + 0.01 * random())
    f_left_dc_source.amplitude = 24.0395 * (1 + 0.01 * random())
