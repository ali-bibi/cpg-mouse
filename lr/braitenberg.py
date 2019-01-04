### The following can be removed when PyNN 0.8 has been established or we have a more elegant
### solution
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
    SENSORPARAMS = {'cm': 20e-5,
                    'v_rest': -70.0,
                    'tau_m': 40.0,
                    'v_reset': -70.0,
                    'v_thresh': -55.0,
                    'tau_refrac': 10.0,
                    'tau_syn_E': 30.0,
                    'tau_syn_I': 60.0}

    cell = sim.IF_curr_alpha(**SENSORPARAMS)

    population = sim.Population(200, cell)
    
    popSize = 10



    # Connect neurons
    CON = sim.FixedProbabilityConnector(0.9)
    ACON = sim.AllToAllConnector()
    
    lf = 10
    le = 20
    rf = 30
    re = 40
    
    v0dl = 50
    v0dr = 60
    v3l = 70
    v3r = 80
    
    v0vl = 90
    v0vr = 100
    
    ini1l = 110
    ini2l = 120
    ini1r = 130
    ini2r = 140
    
    f_v0d = 0.4
    f_v3 = 0.25
    v0d_f = -0.08
    v3_f = 0.04
    e_v0v = 0.4
    v0v_f = 0.12
    f_ini1 = 0.4
    ini1_e = -1.0
    e_ini2 = 0.4
    ini2_f = -0.08
    m = 1.0
    a1 = 0.002
    a2 = 0.002
    
    
    sim.Projection(presynaptic_population=population[0:1],
                   postsynaptic_population=population[lf:(lf+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=a1,delay=0.1))
    sim.Projection(presynaptic_population=population[1:2],
                   postsynaptic_population=population[le:(le+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=a2,delay=0.1))
    sim.Projection(presynaptic_population=population[2:3],
                   postsynaptic_population=population[rf:(rf+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=a1,delay=0.1))
    sim.Projection(presynaptic_population=population[3:4],
                   postsynaptic_population=population[re:(re+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=a2,delay=0.1))
    
    sim.Projection(presynaptic_population=population[lf:(lf+popSize)],
                   postsynaptic_population=population[ini1l:(ini1l+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=f_ini1,delay=0.1))
    sim.Projection(presynaptic_population=population[rf:(rf+popSize)],
                   postsynaptic_population=population[ini1r:(ini1r+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=f_ini1,delay=0.1))
    sim.Projection(presynaptic_population=population[ini1l:(ini1l+popSize)],
                   postsynaptic_population=population[le:(le+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=ini1_e,delay=0.1))
    sim.Projection(presynaptic_population=population[ini1r:(ini1r+popSize)],
                   postsynaptic_population=population[re:(re+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=ini1_e,delay=0.1))
    
    sim.Projection(presynaptic_population=population[le:(le+popSize)],
                   postsynaptic_population=population[ini2l:(ini2l+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=e_ini2,delay=0.1))
    sim.Projection(presynaptic_population=population[re:(re+popSize)],
                   postsynaptic_population=population[ini2r:(ini2r+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=e_ini2,delay=0.1))
    sim.Projection(presynaptic_population=population[ini2l:(ini2l+popSize)],
                   postsynaptic_population=population[lf:(lf+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=ini2_f,delay=0.1))
    sim.Projection(presynaptic_population=population[ini2r:(ini2r+popSize)],
                   postsynaptic_population=population[rf:(re+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=ini2_f,delay=0.1))

    sim.Projection(presynaptic_population=population[lf:(lf+popSize)],
                   postsynaptic_population=population[v0dl:(v0dl+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=f_v0d,delay=0.1))
    sim.Projection(presynaptic_population=population[rf:(rf+popSize)],
                   postsynaptic_population=population[v0dr:(v0dr+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=f_v0d,delay=0.1))
    sim.Projection(presynaptic_population=population[lf:(lf+popSize)],
                   postsynaptic_population=population[v3l:(v3l+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=f_v3,delay=0.1))
    sim.Projection(presynaptic_population=population[rf:(rf+popSize)],
                   postsynaptic_population=population[v3r:(v3r+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=f_v3,delay=0.1))
    
    sim.Projection(presynaptic_population=population[v0dl:(v0dl+popSize)],
                   postsynaptic_population=population[rf:(rf+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=v0d_f,delay=0.1))
    sim.Projection(presynaptic_population=population[v0dr:(v0dr+popSize)],
                   postsynaptic_population=population[lf:(lf+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=v0d_f,delay=0.1))
    sim.Projection(presynaptic_population=population[v3l:(v3l+popSize)],
                   postsynaptic_population=population[rf:(rf+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=v3_f,delay=0.1))
    sim.Projection(presynaptic_population=population[v3r:(v3r+popSize)],
                   postsynaptic_population=population[lf:(lf+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=v3_f,delay=0.1))
    
    sim.Projection(presynaptic_population=population[le:(le+popSize)],
                   postsynaptic_population=population[v0vl:(v0vl+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=e_v0v,delay=0.1))
    sim.Projection(presynaptic_population=population[v0vl:(v0vl+popSize)],
                   postsynaptic_population=population[rf:(rf+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=v0v_f,delay=0.1))
    sim.Projection(presynaptic_population=population[re:(re+popSize)],
                   postsynaptic_population=population[v0vr:(v0vr+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=e_v0v,delay=0.1))
    sim.Projection(presynaptic_population=population[v0vr:(v0vr+popSize)],
                   postsynaptic_population=population[lf:(lf+popSize)],
                   connector=CON,
                   synapse_type= sim.StaticSynapse(weight=v0v_f,delay=0.1))
    

    sim.Projection(presynaptic_population=population[lf:(lf+popSize)],
                   postsynaptic_population=population[5:6],
                   connector=ACON,
                   synapse_type=sim.StaticSynapse(weight=m,delay=0.1))
    sim.Projection(presynaptic_population=population[le:(le+popSize)],
                   postsynaptic_population=population[6:7],
                   connector=ACON,
                   synapse_type=sim.StaticSynapse(weight=m,delay=0.1))
    sim.Projection(presynaptic_population=population[rf:(rf+popSize)],
                   postsynaptic_population=population[7:8],
                   connector=ACON,
                   synapse_type=sim.StaticSynapse(weight=m,delay=0.1))
    sim.Projection(presynaptic_population=population[re:(re+popSize)],
                   postsynaptic_population=population[8:9],
                   connector=ACON,
                   synapse_type=sim.StaticSynapse(weight=m,delay=0.1))

    sim.initialize(population, v=population.get('v_rest'))

    return population


circuit = create_brain()