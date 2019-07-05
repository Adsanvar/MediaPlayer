import os
from flask import Flask, render_template, request, flash
app = Flask(__name__)

click = 0

@app.route('/', methods=['GET', 'POST'])
def MediaPlayer():
    global click
    if request.method == 'GET':
        return render_template("play.html")
    else:
        if "prev_btn" in request.form:
            print("Prev Clicked")
            os.system("sudo dbus-send --system --print-reply --dest=org.bluez /org/bluez/hci0/dev_D0_D2_B0_0D_1A_8E org.bluez.MediaControl1.Previous")
            if click == 1:
                return render_template("pause.html")
            if click == 0:
                return render_template("play.html")
        if "play_btn" in request.form:
            print("Play Clicked")
          
            if click == 0:
                click += 1
                print(click)
                return render_template("pause.html")
            if click == 1:
                click = 0
                print(click)
                return render_template("play.html")

        if "next_btn" in request.form:
            print("Next Clicked")
            os.system("sudo dbus-send --system --print-reply --dest=org.bluez /org/bluez/hci0/dev_D0_D2_B0_0D_1A_8E org.bluez.MediaControl1.Next")
            if click == 1:
                return render_template("pause.html")
            if click == 0:
                return render_template("play.html")


if __name__ == '__main__':
    app.run(debug = True, port=8080)
