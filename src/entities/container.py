import simpy

class Container:

    def __init__(self, id, id_service,env):
        self.id = id
        self.service = id_service
        self.id_res = -1 # It is updated along the Service Disovery assignments
        self.SAC = simpy.Resource(env,1)

    def profiles(self):
        """

        :return: a set of profiles that the service can provide
        """
        #TODO implement profiles
        return [0,1,2]
