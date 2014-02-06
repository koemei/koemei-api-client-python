from koemei.base_client import BaseClient



class KoemeiClient(BaseClient):
    """
    Access to the Koemei API.
    """

    def __init__(self):
        """
        Create the api client
        """
        super(KoemeiClient, self).__init__()