# welcome to yama: yet another mal api
# features:
# - searches myanimelist
# - filters out html
# - returns a dictionary

# "documentation"

# installation
# 1) copy yama.py
# 2) example:
# import yama
# sakurasou = yama.anime_search("the pet girl of sakurasou", "shittyusername", "shittypassword", 1)
# note: int at the end represents which search results to get [range starts from 1! DO NOT USE ZERO!]
# print(sakurasou['description'])

# available stuff - anime_search
# ex:
# sak = yama.anime_search("bleach", "shittyuser", "shittypwd", 1)
# note: int at the end represents which search results to get [range starts from 1! DO NOT USE ZERO!]
# print(sak['description'])
# dictionary contents:
# title | jap title
# english_title | en title
# description | series description
# description_one_paragraph | series description, first paragraph only
# image_url | series cover url
# url | mal listing URL
# status | Finished Airing, Not Yet Aired, etc
# type | TV, Movie, ONA, etc
# start_date | i.e 2004-10-05
# end_date | i.e 2004-10-05
# score | i.e 7.95
# episodes | 12, 366, 4 etc
# description_raw | raw description, without html formatting

# available stuff - functions
# wouldn't recommend using these, they're shit
# find(t, target) | finds the text for target in t
# format_description_html | removes all the HTML stuff and replaces it with normal, looks really weird without
# format_description_one_paragraph | cuts it down to one paragraph
# anime_search | see above
# manga_search | not implemented

import requests
import xml.etree.ElementTree as xml


def find(t, target):
    return t.find(target).text


def format_description_html(target_desc: str):
    description_a = target_desc.replace("&quot;", '"')
    description_b = description_a.replace("<br />", "\n")
    description_c = description_b.replace("[i]", "_")
    description_d = description_c.replace("[/i]", "_")
    description_e = description_d.replace("&#039;", "'")
    description_f = description_e.replace("&mdash;", "—")
    description_g = description_f.replace("&rsquo;", "'")
    return description_g


def format_description_one_paragraph(target_p: str):
    x = format_description_html(target_p)
    return x.split("\n")[0]


def anime_search(search_target: str, user: str, pwd: str, option: int):
    """ searches myanimelist. authentication is required. """
    request_content = search_target.replace(" ", "+") # change spaces to plus signs for get
    reply = requests.get("https://myanimelist.net/api/anime/search.xml?q="
                         + request_content,
                         auth=(user, pwd))  
    r = xml.fromstring(reply.content.decode("utf-8"))
    optionx = option - 1
    x = r[optionx]
    search_dict = {
        "description_raw": find(x, "synopsis"), # raw desc
        "description": format_description_html(find(x, "synopsis")), # anime description (i.e Ichigo Kurosaki is..)
        "description_one_paragraph": format_description_one_paragraph(find(x, "synopsis")),
        "image_url": find(x, "image"), # image URL (i.e https://myanimelist.cdn-dena.com/images/anime/3/40451.jpg)
        "title": find(x, "title"), # anime title (japanese)
        "url": "https://myanimelist.net/anime/" + find(x, "id"), # anime URL
        "mal_icon_url": "http://i.imgur.com/TimEmnI.png", # static MAL icon URL
        "status": find(x, "status"), # status (finished airing, not yet aired, etc)
        "type": find(x, "type"), # type (TV, Movie, ONA etc)
        "start_date": find(x, "start_date"), # start date (i.e 2004-10-05)
        "end_date": find(x, "end_date"), # end date (i.e 2012-03-27)
        "english_title": find(x, "english"), # english title (i.e bleach)
        "score": find(x, "score"), # score (i.e 7.95)
        "episodes": find(x, "episodes"), # total episodes (i.e 366)
    }
    # future ideas:
    # - see git repo
    # goodbye for now
    return search_dict


def manga_search():
    # too lazy
    raise NotImplementedError
