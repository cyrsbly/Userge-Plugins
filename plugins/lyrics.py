import os
import re

import requests
from bs4 import BeautifulSoup
from googlesearch import search
from userge import Message, userge


@userge.on_cmd(
    "glyrics",
    about={
        "header": "Genius Lyrics",
        "description": "Scrape Song Lyrics from Genius.com",
        "usage": "{tr}glyrics [Song Name]",
        "examples": "{tr}glyrics Swalla Nicki Minaj",
    },
)
async def glyrics(message: Message):
    song = message.input_str
    if not song:
        await message.edit("Bruh WTF?")
        return
    await message.edit(f"🌀 __Processing..__\n\n🤖 Follow [Cy Music Bot](https://t.me/cyuserbot1)")
    to_search = song + "genius lyrics"
    gen_surl = list(search(to_search, num=1, stop=1))[0]
    gen_page = requests.get(gen_surl)
    scp = BeautifulSoup(gen_page.text, "html.parser")
    lyrics = scp.find("div", class_="lyrics")
    if not lyrics:
        await message.edit(f"No Results Found for: `{song}`")
        return
    lyrics = lyrics.get_text()
    lyrics = re.sub(r"[\(\[].*?[\)\]]", "", lyrics)
    lyrics = os.linesep.join((s for s in lyrics.splitlines() if s))
    title = scp.find("title").get_text().split("|")
    writers_box = [
        writer
        for writer in scp.find_all("span", {"class": "metadata_unit-label"})
        if writer.text == "Written By"
    ]
    if writers_box:
        target_node = writers_box[0].find_next_sibling(
            "span", {"class": "metadata_unit-info"}
        )
        writers = target_node.text.strip()
    else:
        writers = "UNKNOWN"
    lyr_format = ""
    lyr_format += "**" + title[0] + "**\n"
    lyr_format += "__" + lyrics + "__"
    lyr_format += "\n\n**Written By: **" + "__" + writers + "__"
    lyr_format += "\n**Source: **" + "`" + title[1] + "`"

    if lyr_format:
        await message.edit_or_send_as_file(lyr_format)
    else:
        await message.edit_or_send_as_file(f"No Lyrics Found for **{song}**")
