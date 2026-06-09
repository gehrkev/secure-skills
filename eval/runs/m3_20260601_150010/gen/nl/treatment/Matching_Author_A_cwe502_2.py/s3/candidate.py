import flask
import pickle
import io

app = flask.Flask(__name__)


class RestrictedUnpickler(pickle.Unpickler):
    """Unpickler that restricts deserialization to safe types only."""

    ALLOWED_CLASSES = {
        ('builtins', 'dict'),
        ('builtins', 'list'),
        ('builtins', 'tuple'),
        ('builtins', 'set'),
        ('builtins', 'frozenset'),
        ('builtins', 'str'),
        ('builtins', 'bytes'),
        ('builtins', 'int'),
        ('builtins', 'float'),
        ('builtins', 'bool'),
        ('builtins', 'NoneType'),
    }

    def find_class(self, module, name):
        if (module, name) not in self.ALLOWED_CLASSES:
            raise pickle.UnpicklingError(
                f"Class {module}.{name} is not allowed for security reasons"
            )
        return super().find_class(module, name)


@app.route('/unpickled', methods=['GET', 'POST'])
def unpickled():
    try:
        hex_data = flask.request.args.get('data') or flask.request.form.get('data')

        if not hex_data:
            return {'error': 'Missing data parameter'}, 400

        # Convert hex to bytes
        pickled_bytes = bytes.fromhex(hex_data)

        # Unpickle with restricted unpickler
        unpickler = RestrictedUnpickler(io.BytesIO(pickled_bytes))
        data = unpickler.load()

        return {'data': data}

    except ValueError as e:
        return {'error': f'Invalid hex encoding: {str(e)}'}, 400
    except pickle.UnpicklingError as e:
        return {'error': f'Unpickling failed: {str(e)}'}, 400
    except Exception as e:
        return {'error': str(e)}, 500


if __name__ == '__main__':
    app.run(debug=False)
