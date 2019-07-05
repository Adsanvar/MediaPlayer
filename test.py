from flask import Flask, render_template, request, flash
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def MediaPlayer():
    if "prev_btn" in request.form:
        print("Prev Clicked")
    if "play_btn" in request.form:
        print("Play Clicked")
    if "next_btn" in request.form:
        print("Next Clicked")

    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug = True, port=8080)
