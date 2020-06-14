import logging.config
import json
import random
import simpy

from entities.resource import Resource
from entities.serviceDiscovery import ServiceDiscovery

random_seed = 1
simulation_time = 100

def user(name,env,serviceDiscovery):
    time_between_request = 10
    interrupt = False
    myContainer = None
    my_profile = None
    number_request_containers = 0
    max_tries = 3
    tries = 0
    time_between_SD=10
    print("User_%i arrives at the Infrastructure at: %.2f."%(name,env.now))

    # Wait to be attend by the Service Discovery Entity
    while True:
        with serviceDiscovery.scale.request() as request:
            yield request
            # Wait to get a Container (new or already deployed)
            yield env.process(serviceDiscovery.assign_resource(name))
            # Get the ID-Container
            myContainer = yield serviceDiscovery.get_resource()
            if myContainer != None:
                number_request_containers +=1
                print("User_%i get at Service from container %i, at %.2f."%(name,myContainer.id,env.now))
            else:
                if tries > max_tries:
                    break
                else:
                    tries+=1
                    yield env.timeout(time_between_SD)

        interrupt = False
        tries = 0
        while True:
            yield env.timeout(time_between_request)
            if interrupt:
                with myContainer.SAC.request() as request:
                    yield request
                    profiles = myContainer.SAC.getprofiles()
                    if my_profile in profiles:
                        print("User_%i changes the SLA in the he container_%i: %.2f"%(name,myContainer.id,env.now))
                        interrupt = False
                    else:
                        print("User_%i leaves the container_%i: %.2f. and looks for another one" %(name,myContainer.id,env.now))
                        break


    print("User_%i leaves the Infrastructure at: %.2f"%(name,env.now))



def setup(env,conf):
    resources = {}
    # Create and setup the resources
    # for i in range(conf["resources"]["number"]):
    #     idx = random.randint(0,len(conf["resources"]["capacities"]))
    #     resources[i] = Resource(i,conf["resources"]["capacities"][idx],env,seed=i)

    # Create Service Discovery process
    serviceDiscovery = ServiceDiscovery(env,resources)

    # Crete Users
    for i in range(conf["users"]):
        env.process(user(i,env,serviceDiscovery))

    while True:
        yield env.timeout(30)

if __name__ == '__main__':

    logging.config.fileConfig('logging.ini')

    numberSimulations = 1

    scenario0 = "scenarios/case0.json"
    conf = json.load(open(scenario0,"r"))
    print(conf['info'])

    random.seed(random_seed)
    for i in range(numberSimulations):
        env = simpy.Environment()
        env.process(setup(env,conf))
        env.run(simulation_time)

print("Simulation Done!")
