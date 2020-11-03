from flask import Flask, json, request
from index import StartProcess

startProcess = StartProcess()
api = Flask(__name__)

@api.route('/userText', methods=['POST'])
def post_userText():
  userText = request.get_json()
  response = startProcess.dataProcess(userText)
  print("Returning response")
  return json.dumps(response), 201

if __name__ == '__main__':
    api.run()