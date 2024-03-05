from mockwind.model import Model
from mockwind.train import Train


class MockWind:
    def __init__(self, endpoint, ak, sk):
        self.endpoint = endpoint
        self.ak = ak
        self.sk = sk
        self.train = Train(self)
        self.model = Model(self)



