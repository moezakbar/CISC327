from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def front_page():
    return render_template('front_page.html')

if __name__ == '__main__':
    app.run(debug=True)
