# Mini Terminal For GM As Home Assignment


## Features

- Support the folowing commands: help, quit, stat, sort, clean and script
- You can type help to get the supported command or help <command> to get help about the command
- terminal.log will created at the project directory
- It is possbile to add commands using command factory and register design pattern


## Design

- This project using the OOP and register design pattern to add new commands to the terminal app
- Each command inherted from command base class and register to the command factory using decoration pattern
- Project includes log.py to take care the logs and command utils to take care common
- Project includes command_utils.py to hold common utils that required by the commands
- The main module is terminal.py which take care of the cli loop and script executing loop

# Requierment
This project required Python 3.9 and above, no other modules required

# Usage
After clonning this project, open command line or terminal in the project directory
```sh
python3 terminal.py
```

# Things to take into consideration
The stat command works with log format as the example in the project files:
```sh
2021-02-25-09:30:58:2000 ERROR DOING_SOMETHING2 text text text text text text text ....
2021-02-25-09:30:59:3222 OK DOING_SOMETHING3 text text text text text text text ....
```
