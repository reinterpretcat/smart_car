class Fake:
    def __init__(self, typeName) -> None:
        self.typeName = typeName

    def __getattr__(self, name):
        def simulate(*args, **kwargs):
            print(f"{self.typeName}.{name}: use fake instead")
            return None

        return simulate
