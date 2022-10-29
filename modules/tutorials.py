import pandas as pd

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
        # Creating slack channels ...
        print("Trying to create channels if already not created")
        slackUtils.createPrivateSlackChannels(slackUtils.client, self.tutorialsCsvFile, "slack_channel")
        print("############################################") 
        print("#########Creating of channels done##########") 
        print("############################################") 

        # Updating the description of the slack channels.
        print("Starting to update the description now")
        csv_data = pd.read_csv(self.tutorialsCsvFile)
        for index, entry in csv_data.iterrows():
            targetChannel = entry["slack_channel"]
            targetDesc = entry["description"] # TODO -- Add the zoom call link here
            print("Updating the description for ", targetChannel, " with desc ", targetDesc)
            slackUtils.updateDescription(slackUtils.client, targetChannel, targetDesc)

        print("############################################") 
        print("#########Updating of description done#######") 
        print("############################################") 

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

