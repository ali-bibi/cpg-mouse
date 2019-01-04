@nrp.MapCSVRecorder("recorder", filename="all_spikes.csv", headers=["id", "time"])
@nrp.MapSpikeSink("record_neurons", nrp.brain.record, nrp.spike_recorder)
@nrp.Neuron2Robot(Topic('/monitor/spike_recorder', cle_ros_msgs.msg.SpikeEvent))
def csv_spike_monitor (t, recorder, record_neurons):
    for i in range(0, len(record_neurons.times)):
        recorder.record_entry(
            record_neurons.times[i][0],
            record_neurons.times[i][1]
        )