@nrp.MapCSVRecorder("recorder", filename="all_spikes.csv", headers=["id", "time"])
@nrp.MapSpikeSink("record_neurons", nrp.brain.record[slice(0, 320, 1)], nrp.spike_recorder)

def csv_spike_monitor (t, recorder, record_neurons):
    for i in range(0, len(record_neurons.times)):
        recorder.record_entry(
            record_neurons.times[i][0],
            record_neurons.times[i][1]
        )