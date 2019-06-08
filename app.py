from config import app
from server.routes import authors, books, root, users, wishes, ideas

if __name__ == "__main__":
    app.run(debug=True)