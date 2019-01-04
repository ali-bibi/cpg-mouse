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
    wI = 0.9
    w = 0.9
    
    multW2I = 0.07
    multWI = 0.01
    
    multWs2I = 0.07
    multWsI = 0.01
    
    multW2 = 0.07
    multW = 0.01
    
    multWs2 = 0.07
    multWs = 0.01

    SYNAPSE_PARAMS = {'weight': 4.1,
                      'delay': 0.1}
    SYNAPSE_PARAMS_P = {'weight': 0.1,
                      'delay': 0.1}
    SYNAPSE_PARAMS_M = {'weight': 100.5,
                      'delay': 0.1}
    SYNAPSE_PARAMS_I = {'weight': -4.0,
                      'delay': 0.1}
    SYNAPSE_PARAMS_I_S = {'weight': -18.0,
                      'delay': 0.1}

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
    
    population[130:190].set(cm=5e0,v_thresh=-55.0,
                        tau_syn_E=150.0,
                        tau_syn_I=50.0)
    population[200:600].set(cm=1e0,v_thresh=-55.0,
                        tau_syn_E=15.0,
                        tau_syn_I=5.0)
    
    InhW = -18
    ExW = 0.7
    population[330:350].set(cm=5e0,v_thresh=-55.0, # 5
                        tau_syn_E=30.0, # 50
                        tau_syn_I=100.0) # 30
    
    population[350:370].set(cm=2e0,v_thresh=-55.0, # 5
                          tau_refrac=10.0,
                        tau_syn_E=80, # 50
                        tau_syn_I=30) # 30
    population[10:30].set(cm=5e0,v_thresh=-55.0, # 5
                        tau_syn_E=30.0, # 50
                        tau_syn_I=100.0) # 30
    
    population[30:50].set(cm=2e0,v_thresh=-55.0, # 5
                          tau_refrac=10.0,
                        tau_syn_E=80, # 50
                        tau_syn_I=30) # 30
    
    popSize = 10

    SYN = sim.StaticSynapse(**SYNAPSE_PARAMS)
    SYNP = sim.StaticSynapse(**SYNAPSE_PARAMS_P)
    SYNM = sim.StaticSynapse(**SYNAPSE_PARAMS_M)
    SYNI = sim.StaticSynapse(**SYNAPSE_PARAMS_I)
    SYNIS = sim.StaticSynapse(**SYNAPSE_PARAMS_I_S)

    # Connect neurons
    CON = sim.FixedProbabilityConnector(1)
    OCON = sim.OneToOneConnector()
    ACON = sim.AllToAllConnector()
    SinCON = sim.FromFileConnector("pynn-sin-weights.txt")
    CosCON = sim.FromFileConnector("pynn-cos-weights.txt")
    
    fl = 10
    fr = 20
    hl = 330
    hr = 340

    length = 20
    
    flInh = length + fl
    frInh = length + fr
    
    cnxProb = 1
    
    if True:
        sim.Projection(presynaptic_population=population[235:260],
                       postsynaptic_population=population[fl:fl+popSize],
                       connector=sim.FixedProbabilityConnector(cnxProb),
                       synapse_type=sim.StaticSynapse(weight=w,delay=0.1))
        sim.Projection(presynaptic_population=population[295:320],
                       postsynaptic_population=population[fl:fl+popSize],
                       connector=sim.FixedProbabilityConnector(cnxProb),
                       synapse_type=sim.StaticSynapse(weight=w,delay=0.1))
    if False:
        sim.Projection(presynaptic_population=population[205:230],
                       postsynaptic_population=population[fr:fr+popSize],
                       connector=sim.FixedProbabilityConnector(cnxProb),
                       synapse_type=sim.StaticSynapse(weight=w,delay=0.1))
        sim.Projection(presynaptic_population=population[265:290],
                       postsynaptic_population=population[fr:fr+popSize],
                       connector=sim.FixedProbabilityConnector(cnxProb),
                       synapse_type=sim.StaticSynapse(weight=-w,delay=0.1))
    if True:
        sim.Projection(presynaptic_population=population[430:460],
                       postsynaptic_population=population[hl:hl+popSize],
                       connector=sim.FixedProbabilityConnector(cnxProb),
                       synapse_type=sim.StaticSynapse(weight=wI,delay=0.1))
        sim.Projection(presynaptic_population=population[490:520],
                       postsynaptic_population=population[hl:hl+popSize],
                       connector=sim.FixedProbabilityConnector(cnxProb),
                       synapse_type=sim.StaticSynapse(weight=wI,delay=0.1))
    if False:
        sim.Projection(presynaptic_population=population[400:430],
                       postsynaptic_population=population[hr:hr+popSize],
                       connector=sim.FixedProbabilityConnector(cnxProb),
                       synapse_type=sim.StaticSynapse(weight=wI,delay=0.1))
        sim.Projection(presynaptic_population=population[460:490],
                       postsynaptic_population=population[hr:hr+popSize],
                       connector=sim.FixedProbabilityConnector(cnxProb),
                       synapse_type=sim.StaticSynapse(weight=wI,delay=0.1))

    # hind circuit
    # sin * concurrent inh neurons: sin part
    sim.Projection(presynaptic_population=population[160:190],
                       postsynaptic_population=population[460:490],
                       connector=OCON,
                       synapse_type=sim.StaticSynapse(weight=multWs2I,delay=0.1))
    sim.Projection(presynaptic_population=population[160:190],
                       postsynaptic_population=population[490:520],
                       connector=OCON,
                       synapse_type=sim.StaticSynapse(weight=multWs2I,delay=0.1))
    # sin * concurrent inh neurons: second part
    sim.Projection(presynaptic_population=population[hl+length:hl+length+popSize],
                       postsynaptic_population=population[460:490], 
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=multWsI,delay=0.1))
    sim.Projection(presynaptic_population=population[hr+length:hr+length+popSize],
                       postsynaptic_population=population[490:520], 
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=multWsI,delay=0.1))
    # cos * concurrent drive neurons: cos part
    sim.Projection(presynaptic_population=population[130:160],
                       postsynaptic_population=population[400:430],
                       connector=OCON,
                       synapse_type=sim.StaticSynapse(weight=multW2I,delay=0.1))
    sim.Projection(presynaptic_population=population[130:160],
                       postsynaptic_population=population[430:460],
                       connector=OCON,
                       synapse_type=sim.StaticSynapse(weight=multW2I,delay=0.1))
    # cos * concurrent drive neurons: second part
    sim.Projection(presynaptic_population=population[hl:hl+popSize],
                       postsynaptic_population=population[400:430],
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=multWI,delay=0.1))
    sim.Projection(presynaptic_population=population[hr:hr+popSize],
                       postsynaptic_population=population[430:460],
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=multWI,delay=0.1))
    
    # fore circuit
    # sin * concurrent inh neurons: sin part
    sim.Projection(presynaptic_population=population[160:190],
                       postsynaptic_population=population[260:290],
                       connector=OCON,
                       synapse_type=sim.StaticSynapse(weight=multWs2,delay=0.1))
    sim.Projection(presynaptic_population=population[160:190],
                       postsynaptic_population=population[290:320],
                       connector=OCON,
                       synapse_type=sim.StaticSynapse(weight=multWs2,delay=0.1))
    # sin * concurrent inh neurons: second part
    sim.Projection(presynaptic_population=population[fl+length:fl+length+popSize],
                       postsynaptic_population=population[260:290], 
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=multWs,delay=0.1))
    sim.Projection(presynaptic_population=population[fr+length:fr+length+popSize],
                       postsynaptic_population=population[290:320], 
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=multWs,delay=0.1))
    # cos * concurrent drive neurons: cos part
    sim.Projection(presynaptic_population=population[130:160],
                       postsynaptic_population=population[200:230], # 200-230
                       connector=OCON,
                       synapse_type=sim.StaticSynapse(weight=multW2,delay=0.1))
    sim.Projection(presynaptic_population=population[130:160],
                       postsynaptic_population=population[230:260], # 230-260
                       connector=OCON,
                       synapse_type=sim.StaticSynapse(weight=multW2,delay=0.1))
    # cos * concurrent drive neurons: second part
    sim.Projection(presynaptic_population=population[fl:fl+popSize],
                       postsynaptic_population=population[200:230], # 200-230
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=multW,delay=0.1))
    sim.Projection(presynaptic_population=population[fr:fr+popSize],
                       postsynaptic_population=population[230:260], # 230-260
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=multW,delay=0.1))

    
    # phase feed level 1 and 2
    for x in range(70,100):
        sim.Projection(presynaptic_population=population[4:5],
                       postsynaptic_population=population[x:x+1],
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=1.22185/(x-69),delay=0.1))
        sim.Projection(presynaptic_population=population[x:x+1],
                       postsynaptic_population=population[x+30:x+30+1],
                       connector=OCON,
                       synapse_type=sim.StaticSynapse(weight=2.7,delay=0.1))

    # level 2 winner takes all
    for x in range(101,130):
        for y in range(100,x):
            sim.Projection(presynaptic_population=population[x:x+1],
                       postsynaptic_population=population[y:y+1],
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=-28.0, delay=0.1))
    
    # cos 130-160
    sim.Projection(presynaptic_population=population[100:130],
                       postsynaptic_population=population[130:160],
                       connector=CosCON,
                       synapse_type=sim.StaticSynapse(weight=0.2,delay=0.1))
    
    # sin 160-190
    sim.Projection(presynaptic_population=population[100:130],
                       postsynaptic_population=population[160:190],
                       connector=SinCON,
                       synapse_type=sim.StaticSynapse(weight=0.2,delay=0.1))
    
    # feed network
    for x in range(1,3):
        sim.Projection(presynaptic_population=population[x-1:x],
                       postsynaptic_population=population[x*10:(x*10+popSize)],
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=4.7,delay=0.1))
    for x in range(3,5):
        sim.Projection(presynaptic_population=population[x-1:x],
                       postsynaptic_population=population[300+x*10:(300+x*10+popSize)],
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=4.7,delay=0.1))
    
    # oscillators (self-inhibition)
    for x in range(1,3):
            sim.Projection(presynaptic_population=population[x*10:(x*10+popSize)],
                   postsynaptic_population=population[x*10+length:(x*10+length+popSize)],
                   connector=OCON,
                   synapse_type=sim.StaticSynapse(weight=ExW,delay=0.1))
            sim.Projection(presynaptic_population=population[x*10+length:(x*10+length+popSize)],
                   postsynaptic_population=population[x*10:(x*10+popSize)],
                   connector=OCON,
                   synapse_type=sim.StaticSynapse(weight=InhW,delay=0.1))
    for x in range(3,5):
            sim.Projection(presynaptic_population=population[300+x*10:(300+x*10+popSize)],
                   postsynaptic_population=population[300+x*10+length:(300+x*10+length+popSize)],
                   connector=OCON,
                   synapse_type=sim.StaticSynapse(weight=ExW,delay=0.1))
            sim.Projection(presynaptic_population=population[300+x*10+length:(300+x*10+length+popSize)],
                   postsynaptic_population=population[300+x*10:(300+x*10+popSize)],
                   connector=OCON,
                   synapse_type=sim.StaticSynapse(weight=InhW,delay=0.1))
    
    
    # connect to actors
    sim.Projection(presynaptic_population=population[fl:(fl+popSize)],
                   postsynaptic_population=population[601:602],
                   connector=ACON,
                   synapse_type=SYNM)
    sim.Projection(presynaptic_population=population[fr:(fr+popSize)],
                   postsynaptic_population=population[602:603],
                   connector=ACON,
                   synapse_type=SYNM)
    sim.Projection(presynaptic_population=population[hl+length:(hl+length+popSize)],
                   postsynaptic_population=population[603:604],
                   connector=ACON,
                   synapse_type=SYNM)
    sim.Projection(presynaptic_population=population[hr+length:(hr+length+popSize)],
                   postsynaptic_population=population[604:605],
                   connector=ACON,
                   synapse_type=SYNM)
    sim.Projection(presynaptic_population=population[hl+length:(hl+length+popSize)],
                   postsynaptic_population=population[605:606],
                   connector=ACON,
                   synapse_type=SYNM)
    sim.Projection(presynaptic_population=population[hr+length:(hr+length+popSize)],
                   postsynaptic_population=population[606:607],
                   connector=ACON,
                   synapse_type=SYNM)
    sim.Projection(presynaptic_population=population[fl:(fl+popSize)],
                   postsynaptic_population=population[607:608],
                   connector=ACON,
                   synapse_type=SYNM)
    sim.Projection(presynaptic_population=population[fr:(fr+popSize)],
                   postsynaptic_population=population[608:609],
                   connector=ACON,
                   synapse_type=SYNM)

    sim.initialize(population, v=population.get('v_rest'))

    return population


circuit = create_brain()