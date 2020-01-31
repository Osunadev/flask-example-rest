#   EXAMPLE OF A SIMPLE ENDPOINT
@app.route('/', methods=['GET'])
def someCallbackName():
    return jsonify({ 'msg': 'Hello World' })