#tets
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

    cell = sim.IF_curr_alpha()

    population = sim.Population(120, cell)
    population[0:120].set(cm=0.025,
                        v_rest=-70.0,
                        tau_m=10.0,
                        v_reset=-70.0,
                        v_thresh=-55.0,
                        tau_refrac=10.0,
                        tau_syn_E=30.0,
                        tau_syn_I=30.0)
    
    popSize = 10

    CON = sim.FixedProbabilityConnector(1)
    ACON = sim.AllToAllConnector()
    
    hl = 10
    fl = 20
    fr = 30
    hr = 40

    length = 40
    
    flInh = length + fl
    frInh = length + fr
    
    for x in range(1,5):
        sim.Projection(presynaptic_population=population[x-1:x],
                       postsynaptic_population=population[x*10:(x*10+popSize)],
                       connector=ACON,
                       synapse_type=sim.StaticSynapse(weight=4.0,delay=0.1))
        
    for x in range(1,5):
            sim.Projection(presynaptic_population=population[x*10:(x*10+popSize)],
                   postsynaptic_population=population[x*10+length:(x*10+length+popSize)],
                   connector=CON,
                   synapse_type=sim.StaticSynapse(weight=4.0,delay=0.1))
            sim.Projection(presynaptic_population=population[x*10+length:(x*10+length+popSize)],
                   postsynaptic_population=population[x*10:(x*10+popSize)],
                   connector=CON,
                   synapse_type=sim.StaticSynapse(weight=-18.0,delay=0.1))


    
    sim.Projection(presynaptic_population=population[fl:(fl+popSize)],
                   postsynaptic_population=population[90:(90+popSize)],
                   connector=CON,
                   synapse_type=sim.StaticSynapse(weight=4.0,delay=0.1))
    sim.Projection(presynaptic_population=population[hr:(hr+popSize)],
                   postsynaptic_population=population[90:(90+popSize)],
                   connector=CON,
                   synapse_type=sim.StaticSynapse(weight=-4.0,delay=0.1))
    sim.Projection(presynaptic_population=population[90:(90+popSize)],
                   postsynaptic_population=population[hr:(hr+popSize)],
                   connector=CON,
                   synapse_type=sim.StaticSynapse(weight=0.1,delay=0.1))
    
    sim.Projection(presynaptic_population=population[fr:(fr+popSize)],
                   postsynaptic_population=population[100:(100+popSize)],
                   connector=CON,
                   synapse_type=sim.StaticSynapse(weight=4.0,delay=0.1))
    sim.Projection(presynaptic_population=population[hl:(hl+popSize)],
                   postsynaptic_population=population[100:(100+popSize)],
                   connector=CON,
                   synapse_type=sim.StaticSynapse(weight=-4.0,delay=0.1))
    sim.Projection(presynaptic_population=population[100:(100+popSize)],
                   postsynaptic_population=population[hl:(hl+popSize)],
                   connector=CON,
                   synapse_type=sim.StaticSynapse(weight=0.1,delay=0.1))
    
    
    sim.Projection(presynaptic_population=population[fl:(fl+popSize)],
                   postsynaptic_population=population[fr:(fr+popSize)],
                   connector=CON,
                   synapse_type=sim.StaticSynapse(weight=-4.0,delay=0.1))
    sim.Projection(presynaptic_population=population[fr:(fr+popSize)],
                   postsynaptic_population=population[fl:(fl+popSize)],
                   connector=CON,
                   synapse_type=sim.StaticSynapse(weight=-4.0,delay=0.1))
    
    sim.Projection(presynaptic_population=population[fr:(fr+popSize)],
                   postsynaptic_population=population[hr:(hr+popSize)],
                   connector=CON,
                   synapse_type=sim.StaticSynapse(weight=-4.0,delay=0.1))
    sim.Projection(presynaptic_population=population[hr:(hr+popSize)],
                   postsynaptic_population=population[fr:(fr+popSize)],
                   connector=CON,
                   synapse_type=sim.StaticSynapse(weight=-4.0,delay=0.1))
    
    sim.Projection(presynaptic_population=population[hr:(hr+popSize)],
                   postsynaptic_population=population[hl:(hl+popSize)],
                   connector=CON,
                   synapse_type=sim.StaticSynapse(weight=-4.0,delay=0.1))
    sim.Projection(presynaptic_population=population[hl:(hl+popSize)],
                   postsynaptic_population=population[hr:(hr+popSize)],
                   connector=CON,
                   synapse_type=sim.StaticSynapse(weight=-4.0,delay=0.1))
    
    sim.Projection(presynaptic_population=population[hl:(hl+popSize)],
                   postsynaptic_population=population[fl:(fl+popSize)],
                   connector=CON,
                   synapse_type=sim.StaticSynapse(weight=-4.0,delay=0.1))
    sim.Projection(presynaptic_population=population[fl:(fl+popSize)],
                   postsynaptic_population=population[hl:(hl+popSize)],
                   connector=CON,
                   synapse_type=sim.StaticSynapse(weight=-4.0,delay=0.1))
    

    
    
    
    


    sim.Projection(presynaptic_population=population[hl:(hl+popSize)],
                   postsynaptic_population=population[5:6],
                   connector=ACON,
                   synapse_type=sim.StaticSynapse(weight=0.5,delay=0.1))
    sim.Projection(presynaptic_population=population[fl:(fl+popSize)],
                   postsynaptic_population=population[6:7],
                   connector=ACON,
                   synapse_type=sim.StaticSynapse(weight=0.5,delay=0.1))

    sim.initialize(population, v=population.get('v_rest'))

    return population


circuit = create_brain()