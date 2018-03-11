import os
import requests
from tkinter import *
from tkinter import ttk

root = Tk()
width = 450
height = 800
champlist = []
folder = 'content/'
progressbar_download_var = IntVar()

root.iconbitmap("icon.ico")
root.title("lol-splash-downlaoder //./ by zlyfa!")
root.geometry('%sx%s+0+0' % (width, height))
if not os.path.exists(folder):
    os.mkdir(folder)

def log(msg):
    listbox_log.insert(END, msg)
    root.update()
    listbox_log.yview(END)
    return
def fileexists(o, log=False):
    if os.path.exists(o):
        return True
    else:
        if log==True:
            log("Failed to open " + o)
        return False
def loadFileList():
    if fileexists('champions.ini'):
        global champlist
        file = open('champions.ini', 'r')
        content = file.readlines()
        listbox_champList.delete(0,END)
        champlist = []
        for line in content:
            line = line.replace('\n', '')
            champlist.append(line)
            listbox_champList.insert(END, line)
            root.update()
            listbox_champList.yview(END)
        progressbar_download.config(maximum=len(content))
        log("Added %s entries." % len(content))
    return
def rem():
    ind = listbox_champList.index(ACTIVE)
    name = listbox_champList.get(ind, ind)[0]
    log("Removed " + name)
    file = open('champions.ini', 'r')
    content = file.readlines()
    file.close()
    file = open('champions.ini', 'w')
    for line in content:
        line = line.replace('\n', '')
        if (line != name):
            file.write(line)
    file.close()
    loadFileList()
    return
def add():
    name = entry_addChamp.get()
    if (name != ""):
        file = open('champions.ini', 'a')
        file.write(name + "\n")
        file.close()
        log("Added " + name)
        print(file.closed)
        loadFileList()
    return
def download():
    link = 'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/'
    log("Download started.")
    progressbar_download_var.set(0)
    for champ in champlist:
        for skin in range(100):
            filename = champ + "_%s.jpg" % skin
            if os.path.exists(folder + filename):
                log("Skipped: " + filename)
            else:
                filerequest = link + champ + "_%s.jpg" % skin
                file = open(folder + filename, 'wb')
                image = requests.get(filerequest).content
                file.write(image)
                file.close()
                if not os.path.exists(folder + filename):
                    log("Failed to download " + filename)
                else:
                    filesize = os.path.getsize(folder + filename)
                    if filesize < 500:
                        os.remove(folder + filename)
                        break
                    else:
                        log("Downloaded: " + filename)
        progressbar_download.step(1)
    log("Download finished.")
    return

progressbar_download = ttk.Progressbar(
                                        root,
                                        mode='determinate',
                                        variable=progressbar_download_var
                                        )
listbox_champList = Listbox(
                            root
                            )
listbox_log = Listbox(
                        root
                        )
entry_addChamp = Entry(
                        root,
                        )
button_addChamp = Button(
                        root,
                        text="Add",
                        command=add,
                        activeforeground="#000",
                        activebackground="#555",
                        foreground="#000",
                        background="#555"
                        )
button_remChamp = Button(
                        root,
                        text="Remove",
                        command=rem,
                        activeforeground="#000",
                        activebackground="#555",
                        foreground="#000",
                        background="#555"
                        )
button_download = Button(
                        root,
                        text="Download",
                        command=download,
                        activeforeground="#000",
                        activebackground="#090",
                        foreground="#000",
                        background="#090"
                        )
button_loadFileList = Button(
                            root,
                            text="Reload champion list",
                            command=loadFileList,
                            activeforeground="#000",
                            activebackground="#990",
                            foreground="#000",
                            background="#990"
                            )
button_exit = Button(
                    root,
                    text="Exit",
                    command=quit,
                    activeforeground="#fff",
                    activebackground="#000",
                    foreground="#fff",
                    background="#000"
                    )

log("lol-splash-downlaoder started.")
log("Creator: zlyfa!")
loadFileList()

listbox_champList.place(x=0, y=0, width=width/2, height=height-31)
listbox_log.place(x=width/2, y=0, width=width/2, height=height-186)
progressbar_download.place(x=width/2, y=height-185, width=width/2, height=30)
button_remChamp.place(x=width-width/2, y=height-154, width=width/2, height=30)
entry_addChamp.place(x=width/2, y=height-123, width=width/4 + width/8, height=30)
button_addChamp.place(x=width-width/8, y=height-123, width=width/8, height=30)
button_download.place(x=width/2, y=height-92, width=width/2, height=30)
button_loadFileList.place(x=width/2, y=height-61, width=width/2, height=30)
button_exit.place(x=0, y=height-30, width=width, height=30)

root.mainloop()
