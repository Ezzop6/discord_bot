from app import app
from app.config import Config

if __name__ == "__main__":
    app.run(port=Config.port, host='0.0.0.0')  # type: ignore
