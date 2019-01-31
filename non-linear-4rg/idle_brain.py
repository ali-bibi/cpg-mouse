### The following can be removed when PyNN 0.8 has been established or we have a more elegant

from pkg_resources import parse_version
import pyNN

if not parse_version(pyNN.__version__) >= parse_version('0.8.0'):
	raise RuntimeError("The brain model requires PyNN 0.8.0 to be installed. The Platform is "
                       "currently using %s" % pyNN.__version__)
### END: PyNN Version Check

from hbp_nrp_cle.brainsim import simulator as sim
import numpy as np
import logging

logger = logging.getLogger(__name__)



def create_brain():

    
    cell = sim.IF_curr_alpha()
    population = sim.Population(610, cell)
    
    population[0:610].set(cm=5.0,
                        v_rest=-70.0,
                        tau_m=55.0,
                        v_reset=-70.0,
                        v_thresh=-50.0,
                        tau_refrac=10.0,
                        tau_syn_E=300.0,
                        tau_syn_I=150.0)
    
    # motorpopulations
    population[600:610].set(cm=1e0,v_thresh=-55.0,
                        tau_syn_E=35.0,
                        tau_syn_I=5.0)
    
    # layer 1 population
    population[100:130].set(cm=5e0,v_thresh=-55.0,
                        tau_syn_E=300.0,
                        tau_syn_I=50.0)
    
    # layer 2 populations
    population[130:190].set(cm=5e0,v_thresh=-55.0,
                        tau_syn_E=150.0,
                        tau_syn_I=50.0)
    population[250:310].set(cm=5e0,v_thresh=-55.0,
                        tau_syn_E=150.0,
                        tau_syn_I=50.0)
    
    # layer 4 populations
    population[310:550].set(cm=1e0,v_thresh=-55.0,
                        tau_syn_E=15.0,
                        tau_syn_I=5.0)
    

    # RG-F populations
    population[10:50].set(cm=5e0,v_thresh=-55.0,
                        tau_syn_E=30.0,
                        tau_syn_I=50.0)
    
    # RG-E populations
    population[50:90].set(cm=2e0,v_thresh=-55.0,
                          tau_refrac=10.0,
                        tau_syn_E=80,
                        tau_syn_I=30)
    
    # default population size for RGs
    popSize = 10

    # weights
    mlr_rgf = 1.7
    rge_rgf = -18
    rgf_rge = 0.7
    mlr_l10 = 1.022185
    l1_l2 = 4.7
    l2_l2 = -28.0
    l2_l3 = 0.2
    l3_l4s = 0.07
    l3_l4 = 0.01
    l4_rg = 0.7
    rgf_actor = 0.1
    rge_actor = 0.04

    # connect neurons
    cnxProb = 1
    CON = sim.FixedProbabilityConnector(1)
    OCON = sim.OneToOneConnector()
    ACON = sim.AllToAllConnector()
    SinCON = sim.FromFileConnector("pynn-sin-weights.txt")
    CosCON = sim.FromFileConnector("pynn-cos-weights.txt")
    SinCON2 = sim.FromFileConnector("pynn-sin-weights.txt")
    CosCON2 = sim.FromFileConnector("pynn-cos-weights.txt")
    
    #limbs
    hl = 10
    fl = 20
    fr = 30
    hr = 40
    length = 40
    
    # connect to actors
    sim.Projection(presynaptic_population=population[hr:(hr+popSize)],
                   postsynaptic_population=population[601:602],
                   connector=ACON,
                   synapse_type=sim.StaticSynapse(weight=rgf_actor,delay=0.1))
    sim.Projection(presynaptic_population=population[fr:(fr+popSize)],
                   postsynaptic_population=population[602:603],
                   connector=ACON,
                   synapse_type=sim.StaticSynapse(weight=rgf_actor,delay=0.1))
    sim.Projection(presynaptic_population=population[fl:(fl+popSize)],
                   postsynaptic_population=population[603:604],
                   connector=ACON,
                   synapse_type=sim.StaticSynapse(weight=rgf_actor,delay=0.1))
    sim.Projection(presynaptic_population=population[hl:(hl+popSize)],
                   postsynaptic_population=population[604:605],
                   connector=ACON,
                   synapse_type=sim.StaticSynapse(weight=rgf_actor,delay=0.1))
    sim.Projection(presynaptic_population=population[hr+length:(hr+length+popSize)],
                   postsynaptic_population=population[605:606],
                   connector=ACON,
                   synapse_type=sim.StaticSynapse(weight=rge_actor,delay=0.1))
    sim.Projection(presynaptic_population=population[fr+length:(fr+length+popSize)],
                   postsynaptic_population=population[606:607],
                   connector=ACON,
                   synapse_type=sim.StaticSynapse(weight=rge_actor,delay=0.1))
    sim.Projection(presynaptic_population=population[fl+length:(fl+length+popSize)],
                   postsynaptic_population=population[607:608],
                   connector=ACON,
                   synapse_type=sim.StaticSynapse(weight=rge_actor,delay=0.1))
    sim.Projection(presynaptic_population=population[hl+length:(hl+length+popSize)],
                   postsynaptic_population=population[608:609],
                   connector=ACON,
                   synapse_type=sim.StaticSynapse(weight=rge_actor,delay=0.1))
    
    # unit 4: hr:l4 -> fl:rg
    sim.Projection(presynaptic_population=population[490:520],
                       postsynaptic_population=population[fl:fl+popSize],
                       connector=sim.FixedProbabilityConnector(cnxProb),
                       synapse_type=sim.StaticSynapse(weight=l4_rg,delay=0.1))
    sim.Projection(presynaptic_population=population[520:550],
                       postsynaptic_population=population[fl:fl+popSize],
                       connector=sim.FixedProbabilityConnector(cnxProb),
                       synapse_type=sim.StaticSynapse(weight=l4_rg,delay=0.1))
        
    # unit 3: hl:l4 -> hr:rg
    sim.Projection(presynaptic_population=population[430:460],
                       postsynaptic_population=population[hr:hr+popSize],
                       connector=sim.FixedProbabilityConnector(cnxProb),
                       synapse_type=sim.StaticSynapse(weight=l4_rg,delay=0.1))
    sim.Projection(presynaptic_population=population[460:490],
                       postsynaptic_population=population[hr:hr+popSize],
                       connector=sim.FixedProbabilityConnector(cnxProb),
                       synapse_type=sim.StaticSynapse(weight=l4_rg,delay=0.1))
        
    # unit 2: fr:l4 -> hl:rg
    sim.Projection(presynaptic_population=population[370:400],
                       postsynaptic_population=population[hl:hl+popSize],
                       connector=sim.FixedProbabilityConnector(cnxProb),
                       synapse_type=sim.StaticSynapse(weight=l4_rg,delay=0.1))
    sim.Projection(presynaptic_population=population[400:430],
                       postsynaptic_population=population[hl:hl+popSize],
                       connector=sim.FixedProbabilityConnector(cnxProb),
                       synapse_type=sim.StaticSynapse(weight=l4_rg,delay=0.1))
        
    # unit 1: fl:l4 -> fr:rg
    sim.Projection(presynaptic_population=population[310:340],
                       postsynaptic_population=population[fr:fr+popSize],
                       connector=sim.FixedProbabilityConnector(cnxProb),
                       synapse_type=sim.StaticSynapse(weight=l4_rg,delay=0.1))
    sim.Projection(presynaptic_population=population[340:370],
                       postsynaptic_population=population[fr:fr+popSize],
                       connector=sim.FixedProbabilityConnector(cnxProb),
                       synapse_type=sim.StaticSynapse(weight=l4_rg,delay=0.1))

    # unit 4
    # sin * concurrent inh neurons: sin
    sim.Projection(presynaptic_population=population[280:310],
                       postsynaptic_population=population[520:550],
                       connector=OCON,
                       synapse_type=sim.StaticSynapse(weight=l3_l4s,delay=0.1))
    # sin * concurrent inh neurons: rg
    sim.Projection(presynaptic_population=population[hr+length:hr+length+popSize],
                       postsynaptic_population=population[520:550], 
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=l3_l4,delay=0.1))
    # cos * concurrent drive neurons: cos
    sim.Projection(presynaptic_population=population[250:280],
                       postsynaptic_population=population[490:520],
                       connector=OCON,
                       synapse_type=sim.StaticSynapse(weight=l3_l4s,delay=0.1))
    # cos * concurrent drive neurons: rg
    sim.Projection(presynaptic_population=population[hr:hr+popSize],
                       postsynaptic_population=population[490:520],
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=l3_l4,delay=0.1))
        
    # unit 3
    # sin * concurrent inh neurons: sin
    sim.Projection(presynaptic_population=population[190:220],
                       postsynaptic_population=population[460:490],
                       connector=OCON,
                       synapse_type=sim.StaticSynapse(weight=l3_l4s,delay=0.1))
    # sin * concurrent inh neurons: rg
    sim.Projection(presynaptic_population=population[hl+length:hl+length+popSize],
                       postsynaptic_population=population[460:490], 
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=l3_l4,delay=0.1))
    # cos * concurrent drive neurons: cos
    sim.Projection(presynaptic_population=population[160:190],
                       postsynaptic_population=population[430:460],
                       connector=OCON,
                       synapse_type=sim.StaticSynapse(weight=l3_l4s,delay=0.1))
    # cos * concurrent drive neurons: rg
    sim.Projection(presynaptic_population=population[hl:hl+popSize],
                       postsynaptic_population=population[430:460],
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=l3_l4,delay=0.1))
        
    # unit 2
    # sin * concurrent inh neurons: sin
    sim.Projection(presynaptic_population=population[280:310],
                       postsynaptic_population=population[400:430],
                       connector=OCON,
                       synapse_type=sim.StaticSynapse(weight=l3_l4s,delay=0.1))
    # sin * concurrent inh neurons: rg
    sim.Projection(presynaptic_population=population[fr+length:fr+length+popSize],
                       postsynaptic_population=population[400:430], 
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=l3_l4,delay=0.1))
    # cos * concurrent drive neurons: cos
    sim.Projection(presynaptic_population=population[250:280],
                       postsynaptic_population=population[370:400],
                       connector=OCON,
                       synapse_type=sim.StaticSynapse(weight=l3_l4s,delay=0.1))
    # cos * concurrent drive neurons: rg
    sim.Projection(presynaptic_population=population[fr:fr+popSize],
                       postsynaptic_population=population[370:400],
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=l3_l4,delay=0.1))
        
    # unit 1
    # sin * concurrent inh neurons: sin
    sim.Projection(presynaptic_population=population[190:220],
                       postsynaptic_population=population[340:370],
                       connector=OCON,
                       synapse_type=sim.StaticSynapse(weight=l3_l4s,delay=0.1))
    # sin * concurrent inh neurons: rg
    sim.Projection(presynaptic_population=population[fl+length:fl+length+popSize],
                       postsynaptic_population=population[340:370], 
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=l3_l4,delay=0.1))
    # cos * concurrent drive neurons: cos
    sim.Projection(presynaptic_population=population[160:190],
                       postsynaptic_population=population[310:340],
                       connector=OCON,
                       synapse_type=sim.StaticSynapse(weight=l3_l4s,delay=0.1))
    # cos * concurrent drive neurons: 
    sim.Projection(presynaptic_population=population[fl:fl+popSize],
                       postsynaptic_population=population[310:340], 
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=l3_l4,delay=0.1))

    
    # sin 280-310
    sim.Projection(presynaptic_population=population[220:250],
                       postsynaptic_population=population[280:310],
                       connector=SinCON,
                       synapse_type=sim.StaticSynapse(weight=l2_l3,delay=0.1))
    # cos 250-280
    sim.Projection(presynaptic_population=population[220:250],
                       postsynaptic_population=population[250:280],
                       connector=CosCON,
                       synapse_type=sim.StaticSynapse(weight=l2_l3,delay=0.1))

    # level 2 winner takes all
    for x in range(220,250):
        for y in range(220,x):
            sim.Projection(presynaptic_population=population[x:x+1],
                       postsynaptic_population=population[y:y+1],
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=l2_l2, delay=0.1))


    # sin 160-190
    sim.Projection(presynaptic_population=population[130:190],
                       postsynaptic_population=population[190:220],
                       connector=SinCON2,
                       synapse_type=sim.StaticSynapse(weight=l2_l3,delay=0.1))
    # cos 130-160
    sim.Projection(presynaptic_population=population[130:190],
                       postsynaptic_population=population[160:190],
                       connector=CosCON2,
                       synapse_type=sim.StaticSynapse(weight=l2_l3,delay=0.1))

            
    # layer 2 winner takes all
    for x in range(130,160):
        for y in range(160,x,-1):
            sim.Projection(presynaptic_population=population[x:x+1],
                       postsynaptic_population=population[y:y+1],
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=l2_l2, delay=0.1))
    
    # phase feed layer 1 and 2
    for x in range(100,130):
        sim.Projection(presynaptic_population=population[4:5],
                       postsynaptic_population=population[x:x+1],
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=mlr_l10/(x-99),delay=0.1))
        sim.Projection(presynaptic_population=population[x:x+1],
                       postsynaptic_population=population[130-x+130:130-x+130+1],
                       connector=OCON,
                       synapse_type=sim.StaticSynapse(weight=l1_l2,delay=0.1))
        sim.Projection(presynaptic_population=population[x:x+1],
                       postsynaptic_population=population[120+x:120+x+1],
                       connector=OCON,
                       synapse_type=sim.StaticSynapse(weight=l1_l2,delay=0.1))
    
    # oscillators (self-inhibition)
    for x in range(1,5):
            sim.Projection(presynaptic_population=population[x*10:(x*10+popSize)],
                   postsynaptic_population=population[x*10+length:(x*10+length+popSize)],
                   connector=OCON,
                   synapse_type=sim.StaticSynapse(weight=rgf_rge,delay=0.1))
            sim.Projection(presynaptic_population=population[x*10+length:(x*10+length+popSize)],
                   postsynaptic_population=population[x*10:(x*10+popSize)],
                   connector=OCON,
                   synapse_type=sim.StaticSynapse(weight=rge_rgf,delay=0.1))
            
    # feed network
    for x in range(1,5):
        sim.Projection(presynaptic_population=population[x-1:x],
                       postsynaptic_population=population[x*10:(x*10+popSize)],
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=mlr_rgf,delay=0.1))


    sim.initialize(population, v=population.get('v_rest'))

    return population


circuit = create_brain()