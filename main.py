# pylint: disable=global-statement,redefined-outer-name
import argparse
import csv
import glob
import json
import os

import yaml
from flask import Flask, jsonify, redirect, render_template, send_from_directory, send_file, url_for
from flask_frozen import Freezer
from flaskext.markdown import Markdown
# from flaskext.cache import Cache
import pytz
from pytz import timezone
import tzlocal
import datetime
from dateutil import tz
import sys

#from utils import zoom as zoomUtils
#from utils import slack as slackUtils
from modules.tutorials import Tutorials
from modules.zoom_creator import ZoomCreator

site_data = {}
by_uid = {}


def paper_check(row):
    return "paper" in row['type']

def industry_check(row):
    return "industry" in row['type']

def music_check(row):
    return "music" in row['type']

def lbd_check(row):
    return "lbd" in row['type']

def main(site_data_path):
    global site_data, extra_files
    extra_files = ["README.md"]
    # Load all for your sitedata one time.
    for f in glob.glob(site_data_path + "/*"):
        extra_files.append(f)
        name, typ = f.split("/")[-1].split(".")
        if typ == "json":
            site_data[name] = json.load(open(f))
        elif typ in {"csv", "tsv"}:
            site_data[name] = list(csv.DictReader(open(f)))
        elif typ == "yml":
            site_data[name] = yaml.load(open(f).read(), Loader=yaml.SafeLoader)
    for typ in ["papers", "industry", "music", "lbds", "events"]:
        by_uid[typ] = {}
        # print(typ)
        # if typ == 'lbds':
        #     from IPython import embed
        #     embed()
        for p in site_data[typ]:

            by_uid[typ][p["uid"]] = p
    print("Data Successfully Loaded")
    by_uid["days"] = {}
    site_data["days"] = []
    for day in ['1', '2', '3', '4']:
        speakers = [s for s in site_data["events"] if s["day"] == day and s["category"] == "All Meeting"]
        posters = [p for p in site_data["events"] if p["day"] == day and p["category"] == "Poster session"]
        lbd = [l for l in site_data["events"] if l["day"] == day and l["category"] == "LBD"]
        music = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Music"]
        industry = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Industry"]
        meetup = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Meetup"]
        vmeetup = [m for m in site_data["events"] if m["day"] == day and m["category"] == "VMeetup"]
        master = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Masterclass"]
        wimir = [w for w in site_data["events"] if w["day"] == day and w["category"] == "WiMIR Meetup"]
        special = [s for s in site_data["events"] if s["day"] == day and s["category"] == "Meetup-Special"]
        opening = [o for o in site_data["events"] if o["day"] == day and o["category"] == "Opening"]
        business = [o for o in site_data["events"] if o["day"] == day and o["category"] == "Awards"]
        social = [o for o in site_data["events"] if o["day"] == day and o["category"] == "Social"]

        by_uid["days"][day] = {
            "uid": day,
            "speakers": speakers,
            "all": all,
            "meetup": meetup,
            "special": special,
            "master": master,
            "wimir": wimir,
            "posters": posters,
            "lbd": lbd,
            "music": music,
            "industry": industry,
            "day": day,
            "opening": opening,
            "business": business,
            "social": social,
            "vmeetup":vmeetup
        }
        site_data["days"].append(by_uid["days"][day])
    return extra_files
"""
def setupZoomMeetings(root_path):
    zoomCreator = ZoomCreator(root_path + "events.csv")
        
    # Setting up zoom Utils.
    zoomCreator.setupZoomCalls(zoomUtils)

def setupSlackChannels(target_module, root_path):
    if (target_module == "tutorials"):
        tutorials_module = Tutorials(root_path + "tutorials.csv")
        
        # Setting up zoom Utils.
        tutorials_module.setupSlackChannels(slackUtils)

    else:
        raise Exception("Module is not supported")
"""


# ------------- SERVER CODE -------------------->

app = Flask(__name__)
# cache = Cache(app,config={'CACHE_TYPE': 'simple'})
app.config.from_object(__name__)
freezer = Freezer(app)
markdown = Markdown(app)

# MAIN PAGES


def _data():
    data = {}
    data["config"] = site_data["config"]
    return data


@app.route("/")
def index():
    return redirect("/calendar.html")


# TOP LEVEL PAGES


@app.route("/index.html")
def home():
    return redirect("/calendar.html")


@app.route("/about.html")
def about():
    data = _data()
    data["FAQ"] = site_data["faq"]["FAQ"]
    return render_template("about.html", **data)


@app.route("/papers.html")
def papers():
    data = _data()
    data["papers"] = site_data["papers"]
    return render_template("papers.html", **data)


@app.route("/paper_vis.html")
def paper_vis():
    data = _data()
    return render_template("papers_vis.html", **data)


@app.route("/calendar.html")
def schedule():
    data = _data()
    data["days"] = []
    # data = _data()
    for day in ['1', '2', '3', '4']:
        speakers = [s for s in site_data["events"] if s["day"] == day and s["category"] == "All Meeting"]
        posters = [p for p in site_data["events"] if p["day"] == day and p["category"] == "Poster session"]
        lbd = [l for l in site_data["events"] if l["day"] == day and l["category"] == "LBD"]
        music = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Music"]
        industry = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Industry"]
        meetup = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Meetup"]
        vmeetup = [m for m in site_data["events"] if m["day"] == day and m["category"] == "VMeetup"]
        master = [m for m in site_data["events"] if m["day"] == day and m["category"] == "Masterclass"]
        wimir = [w for w in site_data["events"] if w["day"] == day and w["category"] == "WiMIR Meetup"]
        special = [s for s in site_data["events"] if s["day"] == day and s["category"] == "Meetup-Special"]
        opening = [o for o in site_data["events"] if o["day"] == day and o["category"] == "Opening"]
        business = [o for o in site_data["events"] if o["day"] == day and o["category"] == "Awards"]
        social = [o for o in site_data["events"] if o["day"] == day and o["category"] == "Social"]

        out = {
            "speakers": speakers,
            "all": all,
            "meetup": meetup,
            "special": special,
            "master": master,
            "wimir": wimir,
            "posters": posters,
            "lbd": lbd,
            "music": music,
            "industry": industry,
            "day": day,
            "opening": opening,
            "business": business,
            "social": social,
            "vmeetup": vmeetup

        }
        data["days"].append(out)
    return render_template("schedule.html", **data)


@app.route("/tutorials.html")
def tutorials():
    data = _data()
    data["tutorials"] = [t for t in site_data["events"] if t['category'] == "Tutorials"]
    data["tut_md"] = {}
    for t in ['1', '2', '3', '4', '5', '6']:
        data["tut_md"][t] = open(f"static/tutorials/tut_{t}.md").read()
    return render_template("tutorials.html", **data)

@app.route("/music.html")
def musics():
    data = _data()
    data["music"] = site_data["music"]
    data["music_top"] = open("music_top.md").read()
    data["music_bottom"] = open("music_bottom.md").read()
    return render_template("music.html", **data)

@app.route("/industry.html")
def industries():
    data = _data()
    data["industry"] = site_data["industry"]
    data["industry_top"] = open("industry_top.md").read()
    data["industry_bottom"] = open("industry_bottom.md").read()
    return render_template("industry.html", **data)

@app.route("/lbds.html")
def lbds():
    data = _data()
    data["lbds"] = site_data["lbds"]
    return render_template("lbds.html", **data)

@app.route("/lbds_vis.html")
def lbds_vis():
    data = _data()
    return render_template("lbds_vis.html", **data)

@app.route("/special_meetings.html")
def topics():
    data = _data()
    return render_template("special_meetings.html", **data)

# DOWNLOAD CALENDAR

@app.route("/getCalendar")
def get_calendar():
    #return send_file('static/calendar/ISMIR_2022.ics',
    #                mimetype='text/ics',
    #                attachment_filename='ISMIR_2022.ics',
    #                as_attachment=True)
    filepath = 'static/calendar/'
    filename = 'ISMIR_2022.ics'
    return send_file(os.path.join(filepath,filename), as_attachment=True)

def extract_list_field(v, key):
    value = v.get(key, "")
    if isinstance(value, list):
        return value
    else:
        return value.split(";")


def format_paper(v):
    list_keys = ["authors", "primary_subject", "secondary_subject", "session"]
    list_fields = {}
    for key in list_keys:
        list_fields[key] = extract_list_field(v, key)

    return {
        "id": v["uid"],
        "forum": v["uid"],
        "pic_id": v['pic_id'],
        "content": {
            "title": v["title"],
            "authors": list_fields["authors"],
            "keywords": list(set(list_fields["primary_subject"] + list_fields["secondary_subject"])),
            "abstract": v["abstract"],
            "TLDR": v["abstract"],
            "recs": [],
            "session": list_fields["session"],
            "pdf_url": v.get("pdf_url", ""),
            "channel_url": v["channel_url"],
            "channel_name": v["channel_name"],
            "day": v["day"],
            "yt_id": v["yt_id"]
        },
        "poster_pdf": "GLTR_poster.pdf",
    }

def format_lbd(v):
    list_keys = ["authors", "session"]
    list_fields = {}
    for key in list_keys:
        list_fields[key] = extract_list_field(v, key)
    channel_name = v.get("channel_name", "")
    channel_url = v.get("channel_url", "")
    if channel_name == "" and channel_url == "" and len(list_fields["session"]) > 0:
        print('Re-creating channel name')
        primary_author_names = v["primary_author"].split(" ")
        primary_author_name = primary_author_names[len(primary_author_names)-1].lower()
        channel_name = "lbd-"+list_fields["session"][0]+"-"+v["uid"]+"-"+primary_author_name
        channel_url = "https://ismir2020.slack.com/archives/"+channel_name

    return {
        "id": v["uid"],
        "forum": v["uid"],
        "content": {
            "title": v["title"],
            "authors": list_fields["authors"],
            "abstract": v["abstract"],
            "TLDR": v["abstract"],
            "session": list_fields["session"],
            "poster_type": v.get("poster_type", ""),
            "bilibili_id": v.get("bilibili_id", ""),
            "youtube_id": v.get("youtube_id", ""),
            "channel_name": channel_name,
            "channel_url": channel_url,
            "day": 4,
        },
    }


def format_workshop(v):
    list_keys = ["authors"]
    list_fields = {}
    for key in list_keys:
        list_fields[key] = extract_list_field(v, key)

    return {
        "id": v["uid"],
        "title": v["title"],
        "organizers": list_fields["authors"],
        "abstract": v["abstract"],
    }

def format_music(v):
    return {
        "id": v["uid"],
        "content": {
            "title": v["title"],
            "first_name": v["first_name"],
            "last_name": v["last_name"],
            "affiliation": v["affiliation"],
            "abstract": v["abstract"],
            "bio": v["bio"],
            "web_link": v["web_link"],
            "session": v["session"],
            "yt_id": v["yt_id"],
            "bb_id": v["bb_id"],
            "authors": v["authors"],
        }
    }

def format_industry(v):
    return {
        "id": v["uid"],
        "content": {
            "title": v["title"],
            "session": v["session"],
            "channel_name": v["channel_name"],
            "channel_url": v["channel_url"],
            "company": v["company"],
        }
    }

@app.template_filter('localcheck')
def datetimelocalcheck(s):
    return tzlocal.get_localzone()

@app.template_filter('localizetime')
def localizetime(date,time,timezone):
    to_zone = tz.gettz(str(timezone))
    date = datetime.datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')
    ref_date_tz = pytz.timezone('Asia/Kolkata').localize(date) #[TODO] take ref time zone as input
    local_date = ref_date_tz.astimezone(to_zone)
    return local_date.strftime("%Y-%m-%d"), local_date.strftime("%H:%M")


# ITEM PAGES

@app.route("/day_<day>.html")
def day(day):
    uid = day
    v = by_uid["days"][uid]
    data = _data()
    data["day"] = v
    data["daynum"] = uid
    return render_template("day.html", **data)

@app.route("/poster_<poster>.html")
def poster(poster):
    uid = poster
    v = by_uid["papers"][uid]
    data = _data()
    data["paper"] = format_paper(v)
    return render_template("poster.html", **data)


@app.route("/speaker_<speaker>.html")
def speaker(speaker):
    uid = speaker
    v = by_uid["speakers"][uid]
    data = _data()
    data["speaker"] = v
    return render_template("speaker.html", **data)


@app.route("/workshop_<workshop>.html")
def workshop(workshop):
    uid = workshop
    v = by_uid["workshops"][uid]
    data = _data()
    data["workshop"] = format_workshop(v)
    return render_template("workshop.html", **data)

@app.route("/music_<music>.html")
def music(music):
    uid = music
    v = by_uid["music"][uid]
    data = _data()
    data["music"] = v
    return render_template("piece.html", **data)

@app.route("/industry_<industry>.html")
def industry(industry):
    uid = industry
    v = by_uid["industry"][uid]
    data = _data()
    data["industry"] = v
    return render_template("company.html", **data)

@app.route("/lbd_<lbd>.html")
def lbd(lbd):
    uid = lbd
    v = by_uid["lbds"][uid]
    data = _data()
    data["lbd"] = format_lbd(v)
    return render_template("lbd.html", **data)


@app.route("/chat.html")
def chat():
    data = _data()
    return render_template("chat.html", **data)


# FRONT END SERVING


@app.route("/papers.json")
def paper_json():
    json = []
    for v in site_data["papers"]:
        json.append(format_paper(v))
    return jsonify(json)

@app.route("/music.json")
def music_json():
    json = []
    for v in site_data["music"]:
        json.append(v)
    return jsonify(json)

@app.route("/industry.json")
def industry_json():
    json = []
    for v in site_data["industry"]:
        json.append(v)
    return jsonify(json)

@app.route("/lbds.json")
def lbds_json():
    json = []
    for v in site_data["lbds"]:
        json.append(format_lbd(v))
    return jsonify(json)


@app.route("/static/<path:path>")
def send_static(path):
    if "wo_num" not in path:
        return send_from_directory("static", path)


@app.route("/serve_<path>.json")
def serve(path):
    return jsonify(site_data[path])


# --------------- DRIVER CODE -------------------------->
# Code to turn it all static


@freezer.register_generator
def generator():

    for paper in site_data["papers"]:
        yield "poster", {"poster": str(paper["uid"])}
    for music in site_data["music"]:
        yield "music", {"music": str(music["uid"])}
    for industry in site_data["industry"]:
        yield "industry", {"industry": str(industry["uid"])}
    for lbd in site_data["lbds"]:
        yield "lbd", {"lbd": str(lbd["uid"])}
    for day in site_data["days"]:
        yield "day", {"day": str(day["uid"])}

    for key in site_data:
        if key != 'days':
            yield "serve", {"path": key}


def parse_arguments():
    parser = argparse.ArgumentParser(description="MiniConf Portal Command Line")

    parser.add_argument(
        "--build",
        action="store_true",
        default=False,
        help="Convert the site to static assets",
    )

    parser.add_argument(
        "-b",
        action="store_true",
        default=False,
        dest="build",
        help="Convert the site to static assets",
    )

    parser.add_argument(
        "--target_action", 
        help="Pass the action setup-zoom-meetings, setup-slack-channels or setup-webpage",
        required=True)

    parser.add_argument(
        "--target_module", 
        help="Pass the module for which action has to be done",
        required=False)
    
    parser.add_argument(
        "--path",
        help="Pass the JSON data path and run the server",
        required=True)

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()

    data_path = args.path
    target_action = args.target_action
    target_module = args.target_module

    if(data_path is None):
        raise Exception("--path for the root directory for data is missing")

    if(target_action is None):
        raise Exception("--target_action is not passed. Use setup-zoom-meetings, setup-slack-channels or setup-webpage")
    
    if(target_action == "setup-slack-channels" and target_module is None):
        raise Exception("--target_module is not passed")

    print("Triggering using the following commands: " + str(data_path) + "; " + str(target_action) + "; " + str(target_module))

    if target_action == "setup-zoom-meetings":
        #setupZoomMeetings(data_path)
        print("setup zoom")
    elif target_action == "setup-slack-channels":
        #setupSlackChannels(target_module)
        print("setup slack")
    elif target_action == "setup-webpage":
        extra_files = main(data_path)
        if args.build:
            freezer.freeze()
        else:
            debug_val = False
            if os.getenv("FLASK_DEBUG") == "True":
                debug_val = True
            app.run(port=5100, debug=debug_val, extra_files=extra_files)


    
