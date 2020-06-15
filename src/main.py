import logging.config
import json
import random
import simpy

from entities.resource import Resource
from entities.serviceDiscovery import ServiceDiscovery
from entities.user import User

random_seed = 1
simulation_time = 1000
monitoring_period = 10

def execution_context(env,scenario):
    while True:
        yield env.timeout(monitoring_period)
        print("\t Execution context monitor wake up")
        #For each resource, we test if the conditions have change (randomly)
        for id_res in scenario["resources"]:
            scenario["resources"][id_res].update_state()
            print("\t\t%s"%scenario["resources"][id_res])


def setup(env,conf,scenario):
    scenario["containers"] = []

    # Create and setup the resources
    resources = {}
    for i in range(conf["resources"]["number"]):
        id_capacity_conf = random.randint(0,len(conf["resources"]["capacities"])-1)
        resources[i] = Resource(i,conf["resources"]["capacities"][id_capacity_conf],env,seed=i)
    scenario["resources"] = resources

    # Create Service Discovery process
    service_discovery = ServiceDiscovery(env,resources,scenario)
    scenario["SD"] = service_discovery

    # Population infrastructure
    for id in range(conf["users"]):
        u = User(id,env,service_discovery,scenario)
        env.process(u.start())

    env.process(execution_context(env,scenario))
    # setup function must be a simpy.generator, not elegant but...
    while True:
        yield env.timeout(10000000)

if __name__ == '__main__':

    logging.config.fileConfig('logging.ini')

    numberSimulations = 1

    scenario0 = "scenarios/case0.json"
    conf = json.load(open(scenario0,"r"))
    print(conf['info'])


    random.seed(random_seed)
    for i in range(numberSimulations):
        scenario = {}
        env = simpy.Environment()
        env.process(setup(env,conf,scenario))
        env.run(simulation_time)

        for res in scenario["resources"].values():
            print(res)



print("Simulation Done!")
