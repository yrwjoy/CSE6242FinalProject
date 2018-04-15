from flask import Flask, render_template, request, json, jsonify
app = Flask(__name__)

@app.route("/")
def homepage():
    return render_template('homepage.html')
@app.route("/mainpage")
def mainpage():
    return render_template('index3.html')
if __name__ == "__main__":
    app.run()
