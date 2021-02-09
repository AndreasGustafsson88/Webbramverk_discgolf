from App.UI import create_app
from config import LiveConfig

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
