from flask import Flask, request
from pathlib import Path

app = Flask(__name__)

@app.route('/open_file')
def open_file():
    try:
        filename = request.args.get('filename') or request.form.get('filename')

        if not filename:
            return None

        base_dir = Path.cwd()
        requested_path = (base_dir / filename).resolve()

        requested_path.relative_to(base_dir)

        return open(requested_path, 'r')

    except (FileNotFoundError, OSError, IOError, ValueError):
        return None
