from Map.map import Map
from Map.map_directed import Map_directed
#from Map.map import * # Dårlig kodeskik at importere en hel fil
from Agent.agent import Agent
from Agent.IDCMAPF_agent import IDCMAPF_agent
from Swarm.swarm import Swarm
from Swarm.swarm_IDCMAPF import Swarm_IDCMAPF
from Renderer.renderer import Renderer
#from Renderer.renderer_pygame import Renderer as Renderer_Pygame
from Simulator.simulator import Simulator
from IDCMAPF_Tests.tests import * # Dårlig kodeskik at importere en hel fil
from Logger.logger import Logger
from GA.GA_Rules import GA_Priority_rules
from GA.GA_Fluid import GA_Fluid

from generate_start_and_target import generate_start_and_target_to_numpy, load_position_list_from_nplist, generate_start_and_target_to_list, generate_start_and_target_from_scenario


for env in ["random-64-64-20", "empty-48-48"]:
    for num_agents in [400]:
        start, target = generate_start_and_target_from_scenario(f"Scenario\{env}-random-",num_agents)
        start = start*10
        target = target*10
        #save list to npy
        #print(len(start))
        np.save(f"Statistical_test_comparison\start_and_target_positions_for_experiments/{env}_{num_agents}_agents_start.npy", start)
        np.save(f"Statistical_test_comparison\start_and_target_positions_for_experiments/{env}_{num_agents}_agents_target.npy", target)