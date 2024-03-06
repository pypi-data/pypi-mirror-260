class Task:
    def __init__(self, *args, **kwargs):
        self.name =self.__class__.__name__.lower()
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        raise NotImplementedError
