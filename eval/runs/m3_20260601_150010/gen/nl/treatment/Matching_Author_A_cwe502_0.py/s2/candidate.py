from flask import Flask, request
import marshal

app = Flask(__name__)

@app.route('/unmarshal', methods=['GET', 'POST'])
def unmarshal():
    try:
        hex_data = request.args.get('data') or request.form.get('data')
        if not hex_data:
            return {"error": "No data parameter provided"}, 400

        bytes_data = bytes.fromhex(hex_data)
        result = marshal.loads(bytes_data)
        return {"result": result}
    except ValueError as e:
        return {"error": f"Invalid hex encoding: {str(e)}"}, 400
    except Exception as e:
        return {"error": f"Unmarshal error: {str(e)}"}, 400

if __name__ == '__main__':
    app.run(debug=True)
