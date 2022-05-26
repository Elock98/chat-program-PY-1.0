import time

class TimeStamp:

    """
        Used to get timestamp.
    """

    @staticmethod
    def get_time() -> time.ctime:

        """
            Used to get timestamp.
        """

        return time.ctime()