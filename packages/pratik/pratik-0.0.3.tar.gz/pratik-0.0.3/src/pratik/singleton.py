class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.singleton_init(*args, **kwargs)
        elif args or kwargs:
            cls._instance.singleton_init(*args, **kwargs)
        return cls._instance

    def singleton_init(self, *args, **kwargs):
        pass