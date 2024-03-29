def get_answer(task_details_response: dict):	
    answer = {
        'name': "addUser",
        'description': "Function that adds a new user",
        'parameters': {
            'type': 'object',
            'properties': {
                'name': {"type": "string", "description": "name"},
                'surname': {"type": "string", "description": "surname"},
                'year': {"type": "integer", "description": "year of birth"}
            }
        }
    }
    return answer
