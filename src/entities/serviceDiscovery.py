
import simpy

class ServiceDiscovery(object):
    def __init__(self,env,resources):
        self.env = env
        self.resources = resources

        self.counter = 10
        #Var communication with user
        self.scale = simpy.Resource(env,1)
        self.resource = simpy.Store(env)

    def assign_resource(self,name):
        print("Discoverying a resource for a service called: %s"%name)
        yield self.env.timeout(2)

        self.resource.put(self.counter)
        self.counter +=1

    def get_resource(self):
        return self.resource.get()





