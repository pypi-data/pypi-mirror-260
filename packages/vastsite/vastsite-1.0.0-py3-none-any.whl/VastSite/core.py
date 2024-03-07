from flask import Flask
import socket
import speedtest

def start_flask_app(host, port):
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return 'Hello, World!'

    app.run(host=host, port=port)



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




