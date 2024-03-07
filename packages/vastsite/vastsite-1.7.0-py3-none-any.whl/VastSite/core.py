from flask import Flask, render_template, request, redirect
import socket
import speedtest
import os

def start_flask_app(host='0.0.0.0', port=5000, directory="/", htmlfile="index.html"):
    app = Flask(__name__)

    @app.route(directory)
    def hello():
        return render_template(htmlfile)

    app.run(host=host, port=port)

def create_readme():
  with open("readme.md", "w") as f:
    f.write("""

# Flask Tutorial
This tutorial will show you how to create a simple Flask application.
## Prerequisites
You will need the following software installed:
* Python 3
* Flask
* A text editor
## Creating a New Flask Application
To create a new Flask application, you can use the following command:
flask new myapp



This will create a new directory called `myapp` that contains the following files:
* `myapp.py` - The main Flask application file
* `templates/` - The directory where you will store your HTML templates
* `static/` - The directory where you will store your static files (e.g., CSS, JavaScript)
## Running Your Flask Application
To run your Flask application, you can use the following command:
python myapp.py


This will start the Flask development server on port 5000. You can then visit `http://localhost:5000` in your browser to see your application.
## Loading Templates
To load a template in your Flask application, you can use the `render_template()` function. The `render_template()` function takes the name of the template as its first argument, and any additional arguments that you want to pass to the template as its remaining arguments.
For example, the following code would load the `index.html` template and pass the `name` variable to it:

```python
@app.route("/")
def index():
return render_template("index.html", name="John")
```
## Creating a Template
To create a template, you can create a new file in the `templates/` directory. The file extension should be `.html`.
For example, the following code would create a new template called `index.html`:
```html
<!DOCTYPE html> <html> <head> <title>My Flask App</title> </head> <body> <h1>Hello, {{ name }}!</h1> </body> </html> 
```

## Static, CSS, and templates foulders
If you have not seen it already, by running `boot()`, it creates crucial starting files that are required from Flask to run. 

Here is a rundown what they do:
 - *`templates`* - HTML files are stored here, as it is the default point of access from Flask to read from to load in templates.
- *`static`* - Javascript files are in here, the name if because the files stored here are static, meaning that they don't need a backend server to manage logic (e.g. CSS)
- *`CSS`* - Within the *`static`* foulder, as the name states, it is used to store CSS files.
""")

def boot():
      create_readme()
      if not os.path.exists("templates"):
        os.mkdir("templates")

      if not os.path.exists("static"):
        os.mkdir("static")

      if not os.path.exists("static/css"):
        os.mkdir("static/css")



def internet_connection():
    """
    Function to check if the system is connected to the internet.

    Returns:
        bool: True if connected to the internet, False otherwise.
    """
    try:
        # Try connecting to a well-known internet host (Google's DNS server)
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        pass
    return False





def measure_wifi_speed():
    """
    Function to measure WiFi speed using speedtest.net.

    Returns:
        dict: A dictionary containing the download speed, upload speed, and ping.
    """
    st = speedtest.Speedtest()

    # Perform speed test
    st.get_best_server()
    download_speed = st.download() / 1024 / 1024  # Convert to Mbps
    upload_speed = st.upload() / 1024 / 1024  # Convert to Mbps
    ping = st.results.ping

    return {
        'download_speed': download_speed,
        'upload_speed': upload_speed,
        'ping': ping
    }


# Example usage:
"""
wifi_speed = measure_wifi_speed()
print("Wifi speed is: ", wifi_speed)
print("Download Speed: {:.2f} Mbps".format(wifi_speed['download_speed']))
print("Upload Speed: {:.2f} Mbps".format(wifi_speed['upload_speed']))
print("Ping: {} ms".format(wifi_speed['ping']))
"""




