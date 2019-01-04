@nrp.MapSpikeSink("right_actor", nrp.brain.actors[0], nrp.leaky_integrator_alpha)
@nrp.MapSpikeSink("left_actor", nrp.brain.actors[3], nrp.leaky_integrator_alpha)
@nrp.MapRobotPublisher("rm_topic", Topic("/robot/forearm_R_joint/cmd_pos", std_msgs.msg.Float64))
@nrp.MapRobotPublisher("lm_topic", Topic("/robot/forearm_L_joint/cmd_pos", std_msgs.msg.Float64))
@nrp.Neuron2Robot()
def monitor_actors (t, right_actor, left_actor, rm_topic, lm_topic):
    rm_topic.send_message(int(right_actor.voltage * 1e3))
    lm_topic.send_message(int(left_actor.voltage * 1e3))