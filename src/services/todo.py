from flask import request, Response
from bson import ObjectId
from bson.errors import InvalidId
import json

from config.mongodb import mongo

def json_response(data, status=200):
    return Response(
        json.dumps(data, ensure_ascii=False),
        status=status,
        mimetype='application/json; charset=utf-8'
    )

def create_todo_service():
    data = request.get_json()
    title = data.get('title', None)
    description = data.get('description', None)

    if not title:
        return json_response({'error': 'Title is required'}, 400)

    try:
        result = mongo.db.todos.insert_one({
            'title': title,
            'description': description or '',
            'done': False
        })

        todo = {
            '_id': str(result.inserted_id),
            'title': title,
            'description': description or '',
            'done': False
        }
        return json_response(todo, 201)
    except Exception as e:
        return json_response({'error': str(e)}, 500)

def get_todos_service():
    try:
        todos = list(mongo.db.todos.find())
        for todo in todos:
            todo['_id'] = str(todo['_id'])
        return json_response(todos)
    except Exception as e:
        return json_response({'error': str(e)}, 500)

def get_todo_service(id):
    try:
        todo = mongo.db.todos.find_one({'_id': ObjectId(id)})
        if todo is None:
            return json_response({'error': 'Todo not found'}, 404)
        todo['_id'] = str(todo['_id'])
        return json_response(todo)
    except InvalidId:
        return json_response({'error': 'Invalid ID format'}, 400)
    except Exception as e:
        return json_response({'error': str(e)}, 500)

def update_todo_service(id):
    try:
        data = request.get_json()
        if not data or len(data) == 0:
            return json_response({'error': 'Invalid payload'}, 400)

        result = mongo.db.todos.update_one(
            {'_id': ObjectId(id)},
            {'$set': data}
        )

        if result.matched_count == 0:
            return json_response({'error': 'Todo not found'}, 404)

        return json_response({'message': 'Todo updated successfully'}, 200)
    except InvalidId:
        return json_response({'error': 'Invalid ID format'}, 400)
    except Exception as e:
        return json_response({'error': str(e)}, 500)

def delete_todo_service(id):
    try:
        result = mongo.db.todos.delete_one({'_id': ObjectId(id)})

        if result.deleted_count == 0:
            return json_response({'error': 'Todo not found'}, 404)

        return json_response({'message': 'Todo deleted successfully'}, 200)
    except InvalidId:
        return json_response({'error': 'Invalid ID format'}, 400)
    except Exception as e:
        return json_response({'error': str(e)}, 500)
