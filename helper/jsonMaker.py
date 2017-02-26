from flask import jsonify

def make(data, fieldNames):
    returnResult = []
    for entry in data:
        returnResult.append(dict(zip(fieldNames, entry)))

    return jsonify(returnResult)