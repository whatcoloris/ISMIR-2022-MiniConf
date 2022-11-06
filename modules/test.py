import tutorials
import sys

# TODO Move the utils code to the same repo once everything is setup.
sys.path.append("..")
sys.path.append(".")

from utils import slack as slackUtils
from modules.tutorials import Tutorials

#import slack as slackUtils
#from slackChannelCreator import *
#from tutorials import Tutorials


tutObj = Tutorials("../../ISMIR-2022-Miniconf-Data/sitedata/tutorials_all.csv", "../../ISMIR-2022-Miniconf-Data/sitedata/townscript.csv")
tutObj.setupSlackChannels(slackUtils)