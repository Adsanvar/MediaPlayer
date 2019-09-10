import os, threading, webbrowser, subprocess
from flask import Flask, render_template, request, flash
app = Flask(__name__)
#sudo dbus-send --system --print-reply --dest=org.bluez /org/bluez/hci0/dev_D0_D2_B0_0D_1A_8E/player2 org.freedesktop.DBus.Properties.Get string:org.bluez.MediaPlayer1 string:Track
click = 0

def openWeb():
    port = 8080
    url = "http://127.0.0.1:"+str(port)
    print("~~~~~~~~~~~~~~~~~~~~~~~Openning~~~~~~~~~~~~~~~~~")
    threading.Timer(1.25, lambda: webbrowser.open(url)).start()

def processTrack():
    return
    
def processPlayer(s):
    count = 0 
    for e in s:
        count += 1
        if( e == "\""):
            print(str(count))
            return count
    
@app.route('/', methods=['GET', 'POST'])
def MediaPlayer():
    global click
    if request.method == 'GET':
        return render_template("play.html")
    else:
        if "prev_btn" in request.form:
            print("Prev Clicked")
            try:
                os.system("sudo dbus-send --system --print-reply --dest=org.bluez /org/bluez/hci0/dev_D0_D2_B0_0D_1A_8E org.bluez.MediaControl1.Previous")
            except Exception as e:
                print(str(e))
            if click == 1:
                return render_template("pause.html")
            if click == 0:
                return render_template("play.html")
        if "play_btn" in request.form:
            print("Play Clicked")
        
            if click == 0:
                click += 1
                print(click)
                try:
                   os.system("sudo dbus-send --system --print-reply --dest=org.bluez /org/bluez/hci0/dev_D0_D2_B0_0D_1A_8E org.bluez.MediaControl1.Play")
                   #cmd = "sudo dbus-send --system --print-reply --dest=org.bluez /org/bluez/hci0/dev_D0_D2_B0_0D_1A_8E/player0 org.freedesktop.DBus.Properties.Get string:org.bluez.MediaPlayer1 string:Track"
                   #cmd ="sudo dbus-send --system --print-reply --dest=org.bluez /org/bluez/hci0/dev_D0_D2_B0_0D_1A_8E org.freedesktop.DBus.Properties.Get string:org.bluez.MediaPlayer1 string:Track"
                   cmd = "sudo dbus-send --system --print-reply --dest=org.bluez /org/bluez/hci0/dev_D0_D2_B0_0D_1A_8E org.freedesktop.DBus.Properties.Get string:org.bluez.MediaControl1 string:Player"
                   other = subprocess.check_output(cmd, shell=True)
                   
                   #test = os.popen(cmd).read()
                   print("~~~~~~~~~~~~~~~OPEN:\n" + str(processPlayer(other)))
                   #print("\n~~~~~~~~~~SUB:::" + str(other))
                except Exception as e:
                    print(str(e))
                return render_template("pause.html")
            if click == 1:
                click = 0
                print(click)
                try:
                    os.system("sudo dbus-send --system --print-reply --dest=org.bluez /org/bluez/hci0/dev_D0_D2_B0_0D_1A_8E org.bluez.MediaControl1.Pause")
                except Exception as e:
                    print(str(e))
                return render_template("play.html")

        if "next_btn" in request.form:
            print("Next Clicked")
            try:
                os.system("sudo dbus-send --system --print-reply --dest=org.bluez /org/bluez/hci0/dev_D0_D2_B0_0D_1A_8E org.bluez.MediaControl1.Next")
            except Exception as e:
                print(str(e))
            if click == 1:
                return render_template("pause.html")
            if click == 0:
                return render_template("play.html")

        if "up_btn" in request.form:
            print("Vol Up")
            try:
                os.system("amixer set Master 2%+")
            except Exception as e:
                print(str(e))
            if click == 1:
                return render_template("pause.html")
            if click == 0:
                return render_template("play.html")
            
        if "down_btn" in request.form:
            print("Vol Down")
            try:
                os.system("amixer set Master 2%-")
            except Exception as e:
                print(str(e))
            if click == 1:
                return render_template("pause.html")
            if click == 0:
                return render_template("play.html")


if __name__ == '__main__':
    openWeb()
    app.run(debug = True, port=8080)

