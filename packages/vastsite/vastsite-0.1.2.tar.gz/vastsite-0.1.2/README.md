# VastSite

VastSite is a simple Python package that simplifies Flask web app development by providing a function to start the server with customizable IP and port.

## Installation

You can install Vast Site using pip:

```bash
pip install vastsite
```

## Usage

Import the `start_flask_app` function from `vastsite` and call it to start a Flask web server with default or custom host and port.

```python
from vastsite import start_flask_app

# Start Flask app with default host and port
start_flask_app()

# Start Flask app with custom host and port
start_flask_app(host='127.0.0.1', port=8080)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
