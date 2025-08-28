from app import create_app
from app.models.user import User

app = create_app()

if __name__ == '__main__':
    app.run(port=5555, debug=True)