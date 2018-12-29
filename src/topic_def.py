# this is zbv pub-sub topic definision file.

#topic names
_zbv_data = "zbv_data"


class zbv_data:
    """
    zbv data is the topic for transfer data from data_reader.ScadaDataFile to GUI
    """

    def msgDataSpec(msg= ''):
        """
        - msg: a text string message about current state of ScadaDataFile in free form to inform user
        """

    class subtopic_11:
        """
        Explain when subtopic_11 should be used
        """

        def msgDataSpec(msg, msg2, extra=None):
            """
            - extra: something optional
            - msg2: a text string message #2 for recipient
            """


class topic_2:
    """
    Some something useful about topic2
    """

    def msgDataSpec(msg=None):
        """
        - msg: a text string
        """

    class subtopic_21:
        """
        description for subtopic 21
        """

        def msgDataSpec(msg, arg1=None):
            """
            - arg1: UNDOCUMENTED
            """

# End of topic tree definition.