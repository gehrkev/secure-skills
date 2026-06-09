from flask import request, Response, Flask

app = Flask(__name__)


@app.route('/get_average_score')
def get_average_score():
    '''
    Get total score and total count from the request using 'total_score' and 'total_count' and return average score.
    '''
    total_score = request.args.get('total_score') or (request.json and request.json.get('total_score'))
    total_count = request.args.get('total_count') or (request.json and request.json.get('total_count'))

    if total_score is None or total_count is None:
        return Response('Missing required parameters', status=400)

    try:
        total_score = float(total_score)
        total_count = float(total_count)
    except (ValueError, TypeError):
        return Response('Invalid numeric values provided', status=400)

    if total_count == 0:
        return Response('Division by zero error: total_count cannot be zero', status=400)

    average = total_score / total_count
    return Response(str(average), status=200)
