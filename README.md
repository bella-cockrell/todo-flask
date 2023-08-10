# TODO APP

A TODO app in both Flask and FastAPI.

## Installation instructions

### Flask
To install the dependencies locally, run:
1. `poetry install`
2. `poetry shell`
3. `make run`
    
The server will then be running locally on http://127.0.0.1:5000

To test out the endpoints, run the following requests in a terminal:
```bash
curl -X POST http://127.0.0.1:5000/3 -H "Content-Type: application/json" -d '{"id": 4,"description": "created","priority": 1}'  

curl -X DELETE http://127.0.0.1:5000/3

curl -X PUT http://127.0.0.1:5000/3 -H "Content-Type: application/json" -d '{"id": 3,"description": "changed","priority": 3}'  

```

## Tools
This app uses Black as a code formatter and isort to arrange imports. Run `make lint` to clean up your code.

