from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from handler.PartHandler import PartHandler
from handler.UserHandler import UserHandler
app = Flask(__name__)

CORS(app)

@app.route('/')
def greeting():
    return 'This is a DB test' #left for testing purposes

@app.route('/parts', methods=['GET', 'POST'])
def getAllParts():
    if request.method == 'POST': #adds a part
        return PartHandler().addPart(request.args) #I think request.args is the solution? worked so far
    else:
        return PartHandler().getAllParts() #returns all parts
@app.route('/parts/<int:p_id>', methods=['GET', 'PUT', 'DELETE']) #Get, Update, and Delete parts
def getPart(p_id):
    if request.method == 'GET': #returns part by id
        return PartHandler().getPart(p_id)
    elif request.method == 'PUT': #updates part by id
        return PartHandler().updatePart(p_id, request.args)
    elif request.method == 'DELETE': #deletes part by id
        return PartHandler().deletePart(p_id)
    else: #catches any other methods
        return jsonify(Error="Method not allowed."), 405


@app.route('/wUser', methods=['GET', 'POST'])
def getAllUsers():
    if request.method == 'POST':
        return UserHandler().addUser(request.args)
    else:
        return UserHandler().getAllUsers()

if __name__ == '__main__':
    app.run(debug=True)



