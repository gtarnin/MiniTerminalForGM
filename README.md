# Mini Terminal For GM As Home Assignment


## Features

- Support the following commands: help, quit, stat, sort, clean, and script
- You can type help to get the supported command or help <command> to get help about the command
- terminal.log will create in the project directory
- It is possible to add commands using command factory and register design pattern


## Design

- This project using the OOP and register design pattern to add new commands to the terminal app
- Each command inherited from the command base class and register to the command factory using a decoration pattern
- Project includes log.py to take care of the logs and command_utils.py with common utils for the commands
- Project includes command_utils.py to hold common utils that required by the commands
- The main module is terminal.py which take care of the CLI loop and script executing loop

## Requierments
This project required Python 3.9 and above, no other modules are required.

## Usage
After cloning this project, open a command line or a terminal in the project directory
```sh
python3 terminal.py
```

## Things to take into consideration
The stat command works with log format as the example in the project files run1.log:
```sh
2021-02-25-09:30:58:2000 ERROR DOING_SOMETHING2 text text text text text text text ....
2021-02-25-09:30:59:3222 OK DOING_SOMETHING3 text text text text text text text ....
```

## Author notes
cmd module is an optimal command-line tool for Python. it also supports Auto-Completion and more nice features for a command-line program like this.
But, when using the cmd tool you are losing the OOP and register design pattern. therefore, I used simple input command.

although it looks like the registered pattern is easy to use, still, there is needed to create all commands instance at the terminal.py to make them register
as it looks like you don't need to do these commands instance if you work on the same module.
