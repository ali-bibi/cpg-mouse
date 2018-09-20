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
    SENSORPARAMS = {'cm': 0.025,
                    'v_rest': -70.0,
                    'tau_m': 10.0,
                    'v_reset': -70.0,
                    'v_thresh': -55.0,
                    'tau_refrac': 10.0,
                    'tau_syn_E': 30.0,
                    'tau_syn_I': 30.0}

    SYNAPSE_PARAMS = {'weight': 4.0,
                      'delay': 0.1}
    SYNAPSE_PARAMS_M = {'weight': 0.05,
                      'delay': 0.1}
    SYNAPSE_PARAMS_I = {'weight': -18.0,
                      'delay': 0.1}
    SYNAPSE_PARAMS_I_S = {'weight': -12.0,
                      'delay': 0.1}

    cell = sim.IF_curr_alpha(**SENSORPARAMS)

    population = sim.Population(8, cell)

    SYN = sim.StaticSynapse(**SYNAPSE_PARAMS)
    SYNM = sim.StaticSynapse(**SYNAPSE_PARAMS_M)
    SYNI = sim.StaticSynapse(**SYNAPSE_PARAMS_I)
    SYNIS = sim.StaticSynapse(**SYNAPSE_PARAMS_I_S)

    # Connect neurons
    CON = sim.OneToOneConnector()

    sim.Projection(presynaptic_population=population[0:],
                   postsynaptic_population=population[4:],
                   connector=CON,
                   synapse_type=SYN)
    sim.Projection(presynaptic_population=population[1:],
                   postsynaptic_population=population[5:],
                   connector=CON,
                   synapse_type=SYN)

    sim.Projection(presynaptic_population=population[4:],
                   postsynaptic_population=population[6:],
                   connector=CON,
                   synapse_type=SYN)
    sim.Projection(presynaptic_population=population[5:],
                   postsynaptic_population=population[7:],
                   connector=CON,
                   synapse_type=SYN)

    sim.Projection(presynaptic_population=population[7:],
                   postsynaptic_population=population[5:],
                   connector=CON,
                   synapse_type=SYNIS)
    sim.Projection(presynaptic_population=population[6:],
                   postsynaptic_population=population[4:],
                   connector=CON,
                   synapse_type=SYNIS)
    
    sim.Projection(presynaptic_population=population[6:],
                   postsynaptic_population=population[7:],
                   connector=CON,
                   synapse_type=SYNI)
    sim.Projection(presynaptic_population=population[7:],
                   postsynaptic_population=population[6:],
                   connector=CON,
                   synapse_type=SYNI)

    sim.Projection(presynaptic_population=population[4:],
                   postsynaptic_population=population[2:],
                   connector=CON,
                   synapse_type=SYNM)
    sim.Projection(presynaptic_population=population[5:],
                   postsynaptic_population=population[3:],
                   connector=CON,
                   synapse_type=SYNM)

    sim.initialize(population, v=population.get('v_rest'))

    return population


circuit = create_brain()
