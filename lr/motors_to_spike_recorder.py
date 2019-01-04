# Imported Python Transfer Function
@nrp.MapRobotPublisher("topic2", Topic("/robot/forearm_R_joint/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("topic", Topic("/robot/forearm_L_joint/cmd_pos", std_msgs.msg.Float64))
@nrp.Robot2Neuron()
def motors_to_spike_recorder (t, topic, topic2):
    #log the first timestep (20ms), each couple of seconds
    if t % 2 < 0.02:
        clientLogger.info('Time: ', t)