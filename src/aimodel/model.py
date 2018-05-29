



class MyKerasModel(object):
    """KERAS model"""
    def save(self, path2file_noextention):
        """
        save model to file
        :param path2file_noextention: str path to save file
        """
        raise NotImplemented(__name__)

    def __init__(self, model_config):
        """

        :type model_config: list
        """
        self.model_config = model_config
