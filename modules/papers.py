import pandas as pd
import copy


# Defining the class that exposes the methods related to papaers.
class Papers:
    """
    This method takes the config data loaded and the papers csv file.
    """
    def __init__(self, papersCsvFile, townscriptCsvFile):
        self.papersCsvFile = papersCsvFile
        self.townscriptCsvFile = townscriptCsvFile
        self.useDummyValues = True
    
    """
    This method inputs the zoomUtils and setup zoom calls for the all the sessions.
    """
    def setupZoomCalls(self, zoomUtils):
        if(self.papersCsvFile is None):
            raise Exception("self.papersCsvFile passed in contructor is null")
        
        # Creating an empty dataframe ..
        df = pd.DataFrame()

        # Adding columns in the dataframe.
        # UID can eb number 
        columns = ["UID", "title", "zoom_link"]
        data = []

        # Reading the papers data.
        csv_data = pd.read_csv(self.papersCsvFile)

        # Getting unique combinations of day and sessions.
        session_ids = csv_data.groupby(["day", "session"]).size().reset_index()
        print(session_ids)

        # Populating the data.
        for index, entry in session_ids.iterrows():
            data.append([
                entry["session"], # UID
                "Day " + str(entry["day"]) + " Session " + str(entry["session"]),# Title
                "" # zoom_link
                ])
        print("The data extracted for zoom meetings is: ", data)
        # Final DataFrame is
        df_to_write = pd.DataFrame(data, columns=columns)
        print("DataFrame created: ", df_to_write)

        # File cotaining details for the zoom file.
        df_to_write.to_csv("papers-zoom.csv")

        # Creating zoom links if needed.
        zoomUtils.createZoomLinksIfNeeded("papers-zoom.csv", "title", "zoom_link", "UID")