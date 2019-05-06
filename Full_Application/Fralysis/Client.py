from Fralysis.Dream import Dream

class Client:

    """
    Class to represent a therapists client
    """

    def __init__(self, name: str = ""):
        self.name = name
        self.dreams = []

    def set_name(self, name : str):

        """
        Set a clients name (pseudonym, which is a proper noun)

        :param name:
        """

        self.name = name

    def get_name(self) -> str:

        """
        Get a clients identifier (their name)

        :return: client's name
        """

        return self.name

    def add_dream(self, dream: Dream = None):

        """
        Append a client's dream

        :param dream:
        """

        self.dreams.append(dream)

    def get_dreams(self):

        """
        Retrieve a client's list of dreams

        :return: dreams
        """

        return self.dreams

    def get_dream(self, index: int = 0) -> Dream:

        """
        Retrieve a client's dream

        :param index:
        :return: dream
        """

        if len(self.dreams) >= 1:
            return self.dreams[index]
        else:
            return None
