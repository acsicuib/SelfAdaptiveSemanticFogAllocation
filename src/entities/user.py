
class User:

    def __init__(self, id, env, service_discovery,scenario):
        self.id = id
        self.env = env
        self.service_discovery = service_discovery
        self.time_between_request = 10

        #TODO define User services
        self.my_profile = None
        self.number_request_containers = 0
        self.max_tries = 3
        self.time_between_SD=10

        self.scenario = scenario

    def start(self):
        tries = 0
        container = None
        interrupt = False

        print("User_%i arrives at the Infrastructure at: %.2f." % (self.id, self.env.now))

        # Wait to be attend by the Service Discovery Entity
        while True:
            with self.service_discovery.scale.request() as request:
                yield request
                # Wait to get a Container (new or already deployed)
                yield self.env.process(self.service_discovery.assign_resource(self.id))
                # Get the Container object
                container = yield self.service_discovery.get_resource()
                if container is not None:
                    self.number_request_containers +=1
                    print("User_%i will get service from Container: %i on Resource %i, at %.2f." % (self.id, container.id, container.id_res,self.env.now))
                else:
                    # The service discovery does not find a resource with the user needs.
                    if tries <= self.max_tries:
                        break
                    else:
                        tries += 1
                        # User tries another time
                        #TODO test
                        continue

            interrupt = False
            tries = 0
            while True:
                yield self.env.timeout(self.time_between_request)
                print("User_%i get service from Container: %i on Resource %i, at %.2f."%(self.id, container.id, container.id_res, self.env.now))

                if self.scenario["resources"][container.id_res]: #The service
                    profiles = container.profiles()
                    if self.my_profile in profiles:
                        print("User_%i changes the SLA in the he container_%i: %.2f" % (self.id, container.id, self.env.now))
                        interrupt = False
                    else:
                        print("User_%i leaves the container_%i: %.2f. and looks for another one" % (self.id, container.id, self.env.now))
                        break

        print("User_%i leaves the Infrastructure at: %.2f" % (self.id, self.env.now))