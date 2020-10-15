from api.app import app
from config.config import PROD, API_PORT


def run_api():
    """
    Function to be called by gunicorn
    """
    if PROD:
        app.run(host='0.0.0.0', port=API_PORT, debug=False)
    else:
        app.run(host='0.0.0.0', port=API_PORT, debug=True)


if __name__ == '__main__':
    run_api()
