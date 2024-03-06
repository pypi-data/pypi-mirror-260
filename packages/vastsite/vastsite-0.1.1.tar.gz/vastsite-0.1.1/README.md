# Flask Easy

Flask Easy is a simple Python package that simplifies Flask web app development by providing a function to start the server with customizable IP and port.

## Installation

You can install Flask Easy using pip:

```bash
pip install flask_easy
```

## Usage

Import the `start_flask_app` function from `flask_easy` and call it to start a Flask web server with default or custom host and port.

```python
from flask_easy import start_flask_app

# Start Flask app with default host and port
start_flask_app()

# Start Flask app with custom host and port
start_flask_app(host='127.0.0.1', port=8080)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
