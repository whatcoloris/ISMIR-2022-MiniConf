import tutorials
import sys

# TODO Move the utils code to the same repo once everything is setup.
sys.path.append("..")
sys.path.append(".")

from utils import slack as slackUtils
from utils import zoom as zoomUtils
from modules.tutorials import Tutorials
from modules.papers import Papers

# Uncommnet below for tutorials
#tutObj = Tutorials("../../ISMIR-2022-Miniconf-Data/sitedata/papers.csv", "../../ISMIR-2022-Miniconf-Data/sitedata/townscript.csv")
#tutObj.setupSlackChannels(slackUtils)

##########################

# Uncommnet below for papers
paperObj = Papers("../../ISMIR-2022-Miniconf-Data/sitedata/papers.csv", "../../ISMIR-2022-Miniconf-Data/sitedata/townscript.csv")
paperObj.setupZoomCalls(zoomUtils)