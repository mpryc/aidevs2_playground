# AIdevs2

Small helper lib/app to make AIdevs nicer

## Design

Each solution has it's own file that should implement one and only one function (no typing in return as we don't know what will be the future):

The filename is a task name followed by `.py` and stored in the `solutions` directory.

```py
def get_answer(task_details_response: dict):
    answer = None

    # Do whatever it takes to give answer for a given task info

    return answer
```

## Usage

Couple of examples:

```shell

# Create and activate .venv && install deps
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt

# Export your API_KEY:
$ export AIDEVS_API_KEY=<your API Key>

# For tasks that require OpenAI API Key:
$ export AIDEVS_OPENAI_API_KEY=<your OpenAI API Key>

# Get the task details
$ python main.py -q <task_name>
 # Example
 $ python main.py -q helloapi

# If the task doesn't have endpoint API it also has the option
# to be resolved by talking to OpenAI endpoint, use local flag, example:
$ python main.py -q lesson_3_task_2 -l

# Use solutions/<task_name>.py to sent an answer
$ python main.py -q <task_name> -s
  # Example
  $ python main.py -q helloapi -s

# Use solutions/<task_name>.py to sent an answer, but with using
# cache file which stores token, example:
$ python main.py -q helloapi
$ python main.py -s # max 180s after previous

# Manually provide an answer to a previous task
$ python main.py -q helloapi
  >  INFO:lib.aidevutils:Success response: 
  >	{'code': 0, 'msg': 'please return value of "cookie" field as answer', 'cookie': 'aidevs_494d129d'}
$ python main.py -a aidevs_494d129d # max 180s after previous


# Enable debug, just use -d flag
$ python main.py -q helloapi -d

```