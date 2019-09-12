import os, threading, webbrowser, subprocess
from flask import Flask, render_template, request, flash
app = Flask(__name__)
#sudo dbus-send --system --print-reply --dest=org.bluez /org/bluez/hci0/dev_D0_D2_B0_0D_1A_8E/player2 org.freedesktop.DBus.Properties.Get string:org.bluez.MediaPlayer1 string:Track
click = 0
song = "-------"
artist = "-------"

def openWeb():
    port = 8080
    url = "http://127.0.0.1:"+str(port)
    print("~~~~~~~~~~~~~~~~~~~~~~~Openning~~~~~~~~~~~~~~~~~")
    threading.Timer(1.25, lambda: webbrowser.open(url)).start()
    
def track():
    cmd = "sudo dbus-send --system --print-reply --dest=org.bluez /org/bluez/hci0/dev_D0_D2_B0_0D_1A_8E org.freedesktop.DBus.Properties.Get string:org.bluez.MediaControl1 string:Player"
    player = getName(subprocess.check_output(cmd, shell=True))
    cmd2 = "sudo dbus-send --system --print-reply --dest=org.bluez "+ player +" org.freedesktop.DBus.Properties.Get string:org.bluez.MediaPlayer1 string:Track"                  
    vals = subprocess.check_output(cmd2,shell=True)
    processTrack(vals)
 
def processTrack(val):
    global song, artist
    count = 0 
    first = 0
    last = 0
    track_index = 3
    artist_index = 19
    for e in val:
        count += 1
        if( e == "["):
            first = count
        if( e == "]"):
            last = count
    arr = val[first:last-1]
    li = list(arr.split("\n"))
    song = getName(li[track_index])
    artist = getName(li[artist_index])
    print(getName(li[track_index]))
    print(getName(li[artist_index]))

    
def getName(s):
    count = 0 
    first = 0
    last = 0
    for e in s:
        count += 1
        if( e == "\""):
            if(first != 0):
                last = count
            else:
                first = count
    return s[first:last-1]               
    
@app.route('/', methods=['GET', 'POST'])
def MediaPlayer():
    global click
    if request.method == 'GET':
        print("GET")
        return render_template("play.html", song = song, artist= artist)
    else:
        if "prev_btn" in request.form:
            print("Prev Clicked")
            try:
                os.system("sudo dbus-send --system --print-reply --dest=org.bluez /org/bluez/hci0/dev_D0_D2_B0_0D_1A_8E org.bluez.MediaControl1.Previous")
                track()
            except Exception as e:
                print(str(e))
            if click == 1:
                return render_template("pause.html", song = song, artist= artist)
            if click == 0:
                return render_template("play.html", song = song, artist= artist)
        if "play_btn" in request.form:
            print("Play Clicked")
            if click == 0:
                click += 1
                print(click)
                try:
                    os.system("sudo dbus-send --system --print-reply --dest=org.bluez /org/bluez/hci0/dev_D0_D2_B0_0D_1A_8E org.bluez.MediaControl1.Play")
                    track()
                except Exception as e:
                    print(str(e))
                return render_template("pause.html", song = song, artist= artist)
            if click == 1:
                click = 0
                print(click)
                try:
                    os.system("sudo dbus-send --system --print-reply --dest=org.bluez /org/bluez/hci0/dev_D0_D2_B0_0D_1A_8E org.bluez.MediaControl1.Pause")
                    track()
                except Exception as e:
                    print(str(e))
                return render_template("play.html", song = song, artist= artist)

        if "next_btn" in request.form:
            print("Next Clicked")
            try:
                os.system("sudo dbus-send --system --print-reply --dest=org.bluez /org/bluez/hci0/dev_D0_D2_B0_0D_1A_8E org.bluez.MediaControl1.Next")
                track()
            except Exception as e:
                print(str(e))
            if click == 1:
                return render_template("pause.html", song = song, artist= artist)
            if click == 0:
                return render_template("play.html", song = song, artist= artist)

        if "up_btn" in request.form:
            print("Vol Up")
            try:
                os.system("amixer set Master 2%+")
                track()
            except Exception as e:
                print(str(e))
            if click == 1:
                return render_template("pause.html", song = song, artist= artist)
            if click == 0:
                return render_template("play.html", song = song, artist= artist)
            
        if "down_btn" in request.form:
            print("Vol Down")
            try:
                os.system("amixer set Master 2%-")
                track()
            except Exception as e:
                print(str(e))
            if click == 1:
                return render_template("pause.html", song = song, artist= artist)
            if click == 0:
                return render_template("play.html", song = song, artist= artist)

if __name__ == '__main__':
    openWeb()
    #app.run(debug = True, use_reloader=False, port=8080)
    app.run(debug = True, port=8080)


    
