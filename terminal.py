import log
from command import CommandFactory
from cscript import Script
from csort import Sort
from cstat import Stat
from cclean import Clean


def show_welcome():
    print('Mini Terminal by gtarnin Feb 2021. Type help to see supported commands, Type quit to quit\n')


def show_goodbye():
    print('Thanks for using Mini Terminal by gtarnin. Goodbye!\n')


def show_help(help_command=''):
    reg_commands = CommandFactory.get_registered_commands()
    if help_command == '':
        print('The following command are supported:  (Type help <command> for more information about the command)')
        for reg_cmd in reg_commands:
            print(f'{reg_cmd}  ', end='')
        print('')
    else:
        if help_command in reg_commands:
            cmd_ref = CommandFactory.create_command(help_command)
            if cmd_ref:
                cmd_ref.get_help()
            else:
                show_unknown_command(help_command)
        else:
            show_unknown_command(help_command)


def show_unknown_command(unknown_cmd=''):
    if unknown_cmd != '':
        unknown_cmd = f' {unknown_cmd}'
    print(f'Unknown command{unknown_cmd}.\n')


def get_command_from_input(command_line):
    # in case of help, just strip and return the command
    if command_line.strip() == 'help' or command_line.strip() == 'quit':
        return command_line.strip()

    # try to split by space
    split_command = command_line.strip().split(' ')
    if len(split_command) > 1:
        return split_command[0]
    else:
        return ''


def get_args_from_input(command_line):
    # try to split by space
    split_command = command_line.strip().split(' ')
    if len(split_command) > 1:
        try:
            argument = command_line.strip().split(f'{split_command[0]} ')
        except IndexError:
            return ''

        return argument[1].strip()
    return ''


if __name__ == '__main__':
    logger = log.setup_custom_logger('root')
    script = Script()
    sort = Sort()
    stat = Stat()
    clean = Clean()

    prompt = 'miniter# '
    show_welcome()
    while True:
        user_input = input(prompt)
        script_is_executing = False
        script_commands = []
        command_counter = 0
        # script loop, in case the command is not script, we break from it
        while True:
            if user_input:
                command = get_command_from_input(user_input)
            else:
                break
            if command == 'help':
                show_help(get_args_from_input(user_input))
                break
            elif command == 'quit':
                show_goodbye()
                exit(0)
            elif command == '':
                show_unknown_command()
                break
            else:
                cmd = CommandFactory.create_command(command)
                if cmd:
                    if command != 'script':
                        cmd_out = cmd.execute(get_args_from_input(user_input))
                        if script_is_executing and command_counter > 0:
                            user_input = script_commands[len(script_commands)-command_counter]
                            command_counter = command_counter - 1
                        else:
                            break
                    else:
                        if script_is_executing:
                            print('Unable to execute script from a script!')
                            break
                        elif len(script_commands) == 0:
                            script_commands = cmd.execute(get_args_from_input(user_input))
                            command_counter = len(script_commands)
                            script_is_executing = True
                            if command_counter == 0:
                                break
                            else:
                                user_input = script_commands[len(script_commands) - command_counter]
                                command_counter = command_counter - 1

                else:
                    show_unknown_command(command)
                    break
