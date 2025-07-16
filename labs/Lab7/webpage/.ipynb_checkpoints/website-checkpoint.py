from flask import Flask

my320app = Flask("example-server")

# Global counter for /donate.html visits
donate_visits = 0

def count_donate():
    global donate_visits
    donate_visits += 1
    print("VISITOR", donate_visits)

@my320app.route("/")
def home():
    # Read in the HTML template
    with open("index.html") as f:
        html = f.read()
    # Replace the lowercase 'xyz' in <b>xyz</b> with the current count
    html = html.replace("xyz", str(donate_visits))
    return html

@my320app.route("/donate.html")
def donate():
    # Increment counter on each hit
    count_donate()
    return """<html><body style="background-color:lightblue">
              <h1>Donations</h1>
              Please make one!
              </body></html>"""

if __name__ == '__main__':
    # Listen on all interfaces port 5000
    my320app.run("0.0.0.0", 5000, debug=True, threaded=False)
