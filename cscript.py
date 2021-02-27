from command import CommandFactory, CommandBase
import os
import logging
import command_utils

logger = logging.getLogger('root')


@CommandFactory.register('script')
class Script(CommandBase):

    def execute(self, args):
        list_of_commands = self.__command_script(args)
        if list_of_commands:
            return list_of_commands
        else:
            return []

    @classmethod
    def __do_script(cls, script_file_to_execute):
        script_commands = []
        try:
            with open(script_file_to_execute, 'r') as script:
                for command in script:
                    script_commands.append(command)
        except IOError:
            logger.error('Unable to open the script file!')

        return script_commands

    @classmethod
    def __command_script(cls, *args):
        """
        :param args: --script=<script name>
        :return: None
        """
        if not command_utils.count_args(args, 1):
            log_msg = 'Unable to execute stat command with the given parameters'
            print(f"Error... {log_msg}")
            logger.error(log_msg)
            return
        given_script_file = command_utils.extract_args(args, '--script=')
        if given_script_file == '':
            log_msg = 'script file parameter is missing'
            print(f"Error... {log_msg}")
            logger.error(log_msg)
            return
        if os.path.exists(given_script_file):
            return cls.__do_script(given_script_file)
        else:
            log_msg = 'script file was not found'
            print(f"Error... {log_msg}")
            logger.error(log_msg)
            return

    @classmethod
    def get_help(cls):
        print('\n'.join(['Run a Mini Terminal Script file.',
                         'Usage: script --script=<path/to/script/file>',
                         ]))


if __name__ == '__main__':
    script_file = r'T:\GM\test\myscript.txt'
    script1 = Script()
    script1.execute(f'--script={script_file}')
