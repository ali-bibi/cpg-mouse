# Imported Python Transfer Function
import sensor_msgs.msg
import hbp_nrp_cle.tf_framework.tf_lib
@nrp.MapSpikeSource("left_dc_source", nrp.brain.sensors[0], nrp.dc_source)
@nrp.MapSpikeSource("right_dc_source", nrp.brain.sensors[1], nrp.dc_source)
@nrp.Robot2Neuron()
def dc_source_to_sensors(t, left_dc_source, right_dc_source):
    left_dc_source.amplitude = 0.0396
    right_dc_source.amplitude = 0.0395
