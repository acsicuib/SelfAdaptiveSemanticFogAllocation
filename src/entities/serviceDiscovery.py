from entities.container import Container
import simpy

class ServiceDiscovery(object):
    def __init__(self,env,resources,scenario):
        self.env = env
        self.resources = resources

        # self.private_id_container = 0
        #Var communication with user
        self.scale = simpy.Resource(env,1)
        self.channel_resource = simpy.Store(env)
        self.scenario = scenario

    def assign_resource(self,id_service):
        print("ServiceDiscovery looking for a resource for Service:: %s"%id_service)
        yield self.env.timeout(2)

        container = Container(len(self.scenario["containers"]), id_service,self.env)

        #Option A: Exhaustive search
        # Theory
        # The computational cost must be o(n) lineal
        # Sorting by diverse SLA criteria or profiles, the computational cost is o(n.log)
        # Total_Overhead: this cost * (number of time SLA is not satisfied)
        # Another option (A.2) is to try to maximize the number of profiles that resource

        for id_res in self.scenario["resources"]:
            res = self.scenario["resources"][id_res]
            #TODO implement some criteria selection
            print(res)
            if res.has_capacity():
                res.add_container()
                container.id_res = res.id
                break

        #Option B: Semantic model
        # Theory
        # The computational cost must be o(n) lineal ????
        # Total_Overhead: this cost * (number of time SLA is not satisfied -  number of suitable profiles)
        # TODO HERE integrate semantic query to look for a resource
        # and comment "option A"




        self.scenario["containers"].append(container)
        self.channel_resource.put(container)
        # self.private_id_container += 1





    def get_resource(self):
        return self.channel_resource.get()





