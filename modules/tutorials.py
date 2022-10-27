# Defining the class that exposes the folliwing methods.
class Tutorials:
    """
    This method takes the config data loaded and the tutorials csv file.
    """
    def __init__(self, tutorialsCsvFile):
        self.tutorialsCsvFile = tutorialsCsvFile

    """
    This method inputs the 
    """
    def setupZoomCalls(self, zoomUtils):
        if(self.tutorialsCsvFile is None):
            raise Exception("self.tutorialsCsvFile passed in contructor is null")
        zoomUtils.createZoomLinksIfNeeded(self.tutorialsCsvFile, "title", "zoom_link", "UID")

    """
    This method inputs the slack utils, and uses it to create the slack channels.
    """
    def setupSlackChannels(self, slackUtils):
        if(self.tutorialsCsvFile is None):
            raise Exception("self.tutorialsCsvFile passed in contructor is null")
        slackUtils.createSlackChannelsIfNeeded(self.tutorialsCsvFile, "slack_channel")

    """ 
    This method takes the file path andd loads the data into memory.
    """
    # def setupDataForWebPage():
    #     if(self.tutorialsCsvFile is None):
    #         raise Exception("self.tutorialsCsvFile passed in contructor is null")
    #     site_data = list(csv.DictReader(open(self.tutorialsCsvFile)))
    #     data["tutorials"] = [t for t in site_data if t['category'] == "Tutorials"]
    #     data["tut_md"] = {}
    #     for t in ['1', '2', '3', '4', '5']:
    #         data["tut_md"][t] = open(f"static/tutorials/tut_{t}.md").read()
    #     return data

