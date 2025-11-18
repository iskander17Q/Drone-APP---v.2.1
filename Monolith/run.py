# Monolith/run.py
import os
from Monolith.app import create_app  # путь как у тебя

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=True)