import json
import os
import re
import tkinter
from re import sub
from tkinter import ttk, filedialog
from tkinter.constants import END, DISABLED
from urllib.request import Request, urlopen

import requests

main_win = tkinter.Tk()
main_win.geometry("750x500")
main_win.resizable(False, False)
main_win.title("Lalantap Downloader")
links = []

final_link = []


def store_link():
    tex = entry.get()
    links.append(tex)
    entry.delete("0", END)


def scrap_data(vid):
    url = "https://www.youtube.com/youtubei/v1/player?videoId=" + vid + "&key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8" \
                                                                        "&contentCheckOk=True&racyCheckOk=True "
    data = b'{"context": {"client": {"clientName": "ANDROID", "clientVersion": "16.20"}}}'
    headers = {'User-Agent': 'Mozilla/5.0', 'accept-language': 'en-US,en', 'Content-Type': 'application/json'}
    request = Request(url, headers=headers, data=data, method="POST")
    response = urlopen(request)
    js = json.loads(response.read())
    return js


def video_id(url: str) -> str:
    return regex_search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url, group=1)


def regex_search(pattern: str, string: str, group: int):
    regex = re.compile(pattern)
    results = regex.search(string)
    if not results:
        return False

    return results.group(group)


def downloader(url, file_name):
    t_p = file_name.replace(folder_button.cget("text") + "/", "")
    title.config(text=t_p)
    title.update()
    if os.path.exists(file_name):
        resume_header = {'Range': 'bytes=' + str(os.path.getsize(file_name)) + "-"}
        response = requests.get(url, headers=resume_header, stream=True)
        content_length = os.path.getsize(file_name) + int(response.headers.get("Content-Length"))
        with open(file_name, "ab") as f:
            dl = os.path.getsize(file_name)
            for data in response.iter_content(chunk_size=1024):
                dl += len(data)
                f.write(data)
                status = "Downloading percent" + str(int(dl * 100 / content_length)) + "%" + "--File Size" + str(
                    dl) + "/" + str(content_length)
                title2.config(text=status)
                title2.update()

    else:
        response = requests.get(url, stream=True)
        content_length = int(response.headers.get("Content-Length"))
        with open(file_name, "wb") as f:
            dl = 0
            for data in response.iter_content(chunk_size=1024):
                dl += len(data)
                f.write(data)
                status = "Downloading percent--" + str(int(dl * 100 / content_length)) + "%" + "--File Size--" + str(
                    dl) + "/" + str(content_length)
                title2.config(text=status)
                title2.update()
    title.config(text="Title")
    title2.config(text="Info")

def download_audio():
    for item in links:
        kvideo_id = video_id(item)
        scrap_json = scrap_data(kvideo_id)
        main_win.update()
        title_text = scrap_json["videoDetails"]["title"]
        s = sub(r'[^ \w+]', '', title_text)
        file_name = folder_button.cget("text") + "/" + s + ".mp3"
        main_win.update()
        downloader(scrap_json["streamingData"]["formats"][0]["url"], file_name)


def download_720():
    for item in links:
        kvideo_id = video_id(item)
        scrap_json = scrap_data(kvideo_id)
        main_win.update()
        title_text = scrap_json["videoDetails"]["title"]
        s = sub(r'[^ \w+]', '', title_text)
        file_name = folder_button.cget("text") + "/" + s + "720" + ".mp4"
        main_win.update()
        if len(scrap_json["streamingData"]["formats"]) == 2:
            print("720 not found setting resolution to 360")
            downloader(scrap_json["streamingData"]["formats"][1]["url"], file_name)
        else:
            downloader(scrap_json["streamingData"]["formats"][2]["url"], file_name)


def download_360():
    for item in links:
        kvideo_id = video_id(item)
        scrap_json = scrap_data(kvideo_id)
        main_win.update()
        title_text = scrap_json["videoDetails"]["title"]
        s = sub(r'[^ \w+]', '', title_text)
        file_name = folder_button.cget("text") + "/" + s + ".mp4"
        main_win.update()
        downloader(scrap_json["streamingData"]["formats"][1]["url"], file_name)


label = tkinter.Label(main_win, text="Enter link :", font="algerian")
label.grid(row=1, column=1, pady=70)
entry = tkinter.Entry(main_win, width=40)
entry.grid(row=1, column=2, padx=20)
entry.focus()
button1 = tkinter.Button(main_win, command=store_link, text="Store link", width=50)
button1.grid(row=1, column=3)
button2 = tkinter.Button(main_win, text="Scrap Playlist", width=20)
button2.grid(row=2, column=1, pady=10)
button3 = tkinter.Button(main_win, text="Download audio", command=download_audio, width=20)
button3.grid(row=3, column=1, pady=10)
button5 = tkinter.Button(main_win, text="Scrap Text File", width=20)
button5.grid(row=5, column=1, pady=10)
button7 = tkinter.Button(main_win, text="Folder", width=50)
button7.grid(row=2, column=3, pady=10)
button8 = tkinter.Button(main_win, text="Download 720", command=download_720, width=50)
button8.grid(row=3, column=3, pady=10)
button9 = tkinter.Button(main_win, command=download_360, text="Download 370", width=50)
button9.grid(row=2, column=3, pady=10)
button10 = tkinter.Button(main_win, text="Extract Info", width=50)
button10.grid(row=5, column=3, pady=10)
lab_img = tkinter.Label(main_win, text="thumbnail", background="#e9c46a", width=25, height=8)
lab_img.grid(row=2, column=2, rowspan=4)
title = tkinter.Label(main_win, text="Title", background="#ff0000", width=100)
title.grid(row=7, column=0, pady=25, columnspan=100)
title2 = tkinter.Label(main_win, text="Info", background="#ffff00", width=100)
title2.grid(row=9, column=0, pady=20, columnspan=100)


def select_folder():
    open_file = filedialog.askdirectory()
    path = open_file
    folder_button.config(state=DISABLED)
    folder_button.config(text=path)


folder_button = tkinter.Button(main_win, text="Folder", width=30, command=select_folder)
folder_button.grid(row=10, column=1)

main_win.mainloop()
