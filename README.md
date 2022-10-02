# Welcome to ISMIR 2020!!

Production: https://gh-pages.d2v1pt6u509dae.amplifyapp.com <Need to update this>

Development: http://ddmal.music.mcgill.ca/ISMIR-Conf/ <Need to update this>

___
# Setup and building the site

## MiniConf

<a href="https://mini-conf.github.io/index.html">MiniConf</a> is a virtual conference in a box. It manages the papers, schedules, and speakers for an academic conference run virtually. It can be easily integrated with interactive tools such as video, chat, and QA.

<img src="https://raw.githubusercontent.com/Mini-Conf/Mini-Conf/master/miniconf.gif">

MiniConf was originally built to host <a href="https://iclr.cc/virtual_2020">ICLR 2020</a> a virtual conference with 6000 participants and have been used to host a wide variety of major conferences.

It is designed to be:

* Run based on static files hosted by any server. 
* Modifiable without a database using CSV files.
* Easy to extend to fit any backend or additional frontend tools. 

## Links
Demo system: <a href='http://www.mini-conf.org'> http://www.mini-conf.org</a>

Source Code: <a href='https://github.com/Mini-Conf/Mini-Conf'> https://github.com/Mini-Conf/Mini-Conf</a>

## Get Started

<pre>
> pip install -r requirements.txt
> make run
</pre>

When you are ready to deploy run `make freeze` to get a static version of the site in the `build` folder. 


### Tour

The <a href="https://github.com/Mini-Conf/Mini-Conf">MiniConf</a> repo:

1) *Datastore* This datastore is not in this repository as it will have sensitive data like personal email addresses.

It is a collection of CSV files representing the papers, speakers, workshops, and other important information for the conference. 

The platform expects that path of the data as an input when executing the scripts.

2) *Routing* <a href="https://github.com/Mini-Conf/Mini-Conf/tree/master/main.py">`main.py`</a>

One file flask-server handles simple data preprocessing and site navigation. 

3) *Templates* <a href="https://github.com/Mini-Conf/Mini-Conf/tree/master/templates">`templates/`</a>

Contains all the pages for the site. See `base.html` for the master page and `components.html` for core components.

4) *Frontend* <a href="https://github.com/Mini-Conf/Mini-Conf/tree/master/static">`static/`</a>

Contains frontend components like the default css, images, and javascript libs.

5) *Scripts* <a href="https://github.com/Mini-Conf/Mini-Conf/tree/master/scripts">`scripts/`</a>

Contains additional preprocessing to add visualizations, recommendations, schedules to the conference. 

6) For importing calendars as schedule see [scripts/README_Schedule.md](https://github.com/Mini-Conf/Mini-Conf/blob/master/scripts/README_Schedule.md)

### Extensions

MiniConf is designed to be a completely static solution. However it is designed to integrate well with dynamic third-party solutions. We directly support the following providers: 

* Rocket.Chat: The `chat/` directory contains descriptions for setting up a hosted Rocket.Chat instance and for embedding chat rooms on individual paper pages. You can either buy a hosted setting from Rocket.chat or we include instructions for running your own scalable instance through sloppy.io. 

* Auth0 : The code can integrate through Auth0.com to provide both page login (through javascript gating) and OAuth SSO with Rocket Chat. The documentation on Auth0 is very easy to follow, you simply need to create an Application for both the MiniConf site and the Rocket.Chat server. You then enter in the Client keys to the appropriate configs. 

* SlidesLive: It is easy to embedded any video provider -> YouTube, Vimeo, etc. However we have had great experience with SlidesLive and recommend them as a host. We include a slideslive example on the main page. 

* PDF.js: For conferences that use posters it is easy to include an embedded pdf on poster pages. An example is given. 


### Acknowledgements

MiniConf was built by [Hendrik Strobelt](http://twitter.com/hen_str) and [Sasha Rush](http://twitter.com/srush_nlp).

Thanks to Darren Nelson for the original design sketches. Shakir Mohamed, Martha White, Kyunghyun Cho, Lee Campbell, and Adam White for planning and feedback. Hao Fang, Junaid Rahim, Jake Tae, Yasser Souri, Soumya Chatterjee, and Ankshita Gupta for contributions. 

### Citation
Feel free to cite MiniConf:
```bibtex
@misc{RushStrobelt2020,
    title={MiniConf -- A Virtual Conference Framework},
    author={Alexander M. Rush and Hendrik Strobelt},
    year={2020},
    eprint={2007.12238},
    archivePrefix={arXiv},
    primaryClass={cs.HC}
}
```


___
# ISMIR Mini-Conf Platform - Data Description

All data for Mini-Conf can be provided either as CSV, JSON, or YAML. 
So it does not matter if you provide a `papers.csv` or a `papers.yml` as long as
the required data fields are provided.

## Global Configuration (config.yml)

- name: `<short name>`
- tagline: `<long name>`
- date: `<Date of conference>`
- proceedings_title: `<proceedings name for citation>`
- citation_date: `<date for citation export (no HTML)>`
- analytics: `<Google analytics ID starting with UA... >`
- logo: 
    - image: `<link to logo>`
    - width: `<width of the image> or "auto"`
    - height: `<height of the image> or "auto"`
- site_title: `<name of the site>`
- page_title:
    - prefix: `<text to include in title of every page>`
    - separator: `<characters between prefix and name of the current page>`
- background_image: `<link to background image>`
- organization: `<conference committee name>`
- chat_server: `<url of rocket chat server, if used>`
- default_presentation_id: `<default slideslive id, if used>`
- default_poster_pdf: `<default poster pdf, if used>`

## Detail Pages

### committee [.csv | .json | .yml]
The list of members of the orga team visible on the landing page

  - role: `<Chair name>` 
  - name: `<Name>`
  - aff: `<Affiliation>`
  - im: `<Image URL>`
  - tw: `<Twitter name>`
  
 Example (.yml):
 ```yaml
committee:
  - role: Procrastination Chair 
    name: Homer Simpson
    aff: Springfield University
    im: https://en.wikipedia.org/wiki/Homer_Simpson#/media/File:Homer_Simpson_2006.png 
```

<hr>

### papers [.csv | .json | .yml]
The list of papers.

- UID: `<Unique ID>`
- title: `<paper title>`
- authors: `<list of authors>` -- (seperated by `|` in CSV)
- abstract: `<abstract text>`
- keywords: `<list of keywords>` -- (seperated by `|` in CSV)  
- sessions: `<list of session IDs>` --  (seperated by `|` in CSV) 

Example (.csv):
```csv
UID,title,authors,abstract,keywords,sessions
B1xSperKvH,Donuts Holes are the Best,Homer Simpson|Bart Simpson,"Donuts are the cause for a lot of taste.",donuts|food|joy,S1|S3
```

<hr>

### speakers [.csv | .json | .yml]
The list of keynote talks.

- UID: `<Unique ID>`
- title: `<talk title>`
- institution: `<affiliation>`
- speaker: `<speaker name>`
- abstract: `<talk abstract>`
- bio: `<short bio>`
- session: `<session ID>`

Example (.csv):
```csv
UID,title,institution,speaker,abstract,bio,session
1,"AI + Africa = Global Innovation","IBM Research Africa, Nairobi",Dr. Aisha Walcott-Bryant,"Artificial Intelligence (AI) has for some time stoked the creative fires of computer scientists and researchers world-wide -- even before the so-called AI winter. After emerging from the winter, with much improved compute, vast amounts of data, and new techniques, AI has ignited our collective imaginations. We have been captivated by its promise while wary of its possible misuse in applications. AI has certainly demonstrated its enormous potential especially in fields such as healthcare. There, it has been used to support radiologists and to further precision medicine; conversely it has been used to generate photorealistic videos which distort our concept of what is real.  Hence, we must thoughtfully harness AI to address the myriad of scientific and societal challenges; and open pathways to opportunities in governance, policy, and management. In this talk, I will share innovative solutions which leverage AI for global health with a focus on Africa. I will present a vision for the collaborations in hopes to inspire our community to join on this journey to transform Africa and impact the world.","Dr. Aisha Walcott-Bryant is a research scientist and manager of the AI Science and Engineering team at IBM Research, Africa. She is passionate about healthcare, interactive systems, and on addressing Africa's diverse challenges.In addition, Dr. Walcott-Bryant leads a team of researchers and engineers who are working on transformational innovations in global health and development while advancing the state of the art in AI, Blockchain, and other technologies.She and her team are engaged in projects in Maternal Newborn Child Health (MNCH), Family Planning (FP), disease intervention planning, and water access and management.  Her team's recent healthcare work on “Enabling Care Continuity Using a Digital Health Wallet” was awarded Honorable Mention at the International Conference on Health Informatics, ICHI2019.Prior to her career at IBM Research Africa, Dr. Walcott-Bryant worked in Spain. There, she took on projects in the area of Smarter Cities at Barcelona Digital and Telefonica with a focus on physical systems for social media engagement, and multi-modal trip planning and recommending. Dr. Walcott-Bryant earned her PhD in Electrical Engineering and Computer Science at MIT where she conducted research on mobile robot navigation in dynamic environments at their Computer Science and Artificial Intelligence Lab (CSAIL).",S2
```

<hr>

### workshops [.csv | .json | .yml]
The list of workshops or socials.

- UID: `<Unique ID>`
- title: `<workshop title>`
- authors: `<organizer names>`
- abstract: `<abstract text>`
- [TBD] url: `<external link>`

<hr>

### faq [.json | .yml]
The list of FAQ questions partitioned into sections.

 - Section: `<Section Name>`
 - QA:
      - Question: `<Question>`
      - Answer: `<Answer>`

Example (.yml):
```yaml
FAQ:
  - Section: Test Section
    QA:
      - Question: What is a good question?
        Answer: "Here are the answers"
```
