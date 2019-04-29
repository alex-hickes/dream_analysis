from Fralysis.Dream import Dream

class Client:

    def __init__(self, name: str = ""):
        self.name = name
        self.dreams = []

    def set_name(self, name : str):
        self.name = name

    def get_name(self) -> str:
        return self.name

    def add_dream(self, dream: Dream = None):
        self.dreams.append(dream)

    def get_dreams(self):
        return self.dreams

    def get_dream(self, index: int = 0) -> Dream:
        if len(self.dreams) >= 1:
            return self.dreams[index]
        else:
            return None
