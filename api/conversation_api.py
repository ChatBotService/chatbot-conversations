import flask
from flask_restful import Resource
from flask import request, jsonify, redirect, Response
from models.models import *


class ConversationAPI(Resource):
    def get(self):
        if "id" in request.args:
            conversations = ConversationFile.query.filter_by(id=request.args["id"]).first()
            conversation_schema = ConversationFileSchema(many=False)
            return jsonify(conversation_schema.dump(conversations))
        elif "user_id" in request.args:
            conversations = ConversationFile.query.filter_by(user_id=request.args["user_id"]).all()
            conversation_schema = ConversationFileSchema(many=True)
            return jsonify(conversation_schema.dump(conversations))
        else:
            conversations = ConversationFile.query.all()
            conversation_schema = ConversationFileSchema(many=True)
            return jsonify(conversation_schema.dump(conversations))
        
    def post(self):
        if request.files:
            uploaded_file = request.files["conversation-file"]
            print("Uploaded file", flush=True)
            print(uploaded_file, flush=True)
            file_blob = uploaded_file.read()
            conversation_file = ConversationFile(
                name=uploaded_file.filename,
                data=file_blob,
                data_size=len(file_blob),
                user_id = 1) #TODO: Hardcoded user id
            db.session.add(conversation_file)
            db.session.commit()
        return Response(status=200)
    
    def delete(self):
        id = request.args.get("id")
        if id:
            ConversationFile.query.filter_by(id=id).delete()
            db.session.commit()
        return Response(status=200)