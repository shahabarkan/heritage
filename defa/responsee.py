class response:
    class Errorres:
        def __init__(self,status_code,des):
            self.status_code = status_code
            self.description = des
    class successres:
        def __init__(self,des):
            self.status_code = 200
            self.description = des
