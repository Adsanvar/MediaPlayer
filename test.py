import os
from flask import Flask, render_template, request, flash
app = Flask(__name__)
#sudo dbus-send --system --print-reply --dest=org.bluez /org/bluez/hci0/dev_D0_D2_B0_0D_1A_8E/player2 org.freedesktop.DBus.Properties.Get string:org.bluez.MediaPlayer1 string:Track
click = 0

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


if __name__ == '__main__':
    app.run(debug = True, port=8080)
