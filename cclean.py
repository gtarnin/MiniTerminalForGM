import os
import logging
import command_utils
from command import CommandFactory, CommandBase


logger = logging.getLogger('root')
windows_size = 5
# didn't understand the meaning/usage of this parameter
deletion_threshold = 0


@CommandFactory.register('clean')
class Clean(CommandBase):
    def execute(self, args):
        self.__command_clean(args)

    @classmethod
    def __command_clean(cls, *args):
        """
        :param args: <path/to/the/logs/directory>
        :return: None
        """
        if not command_utils.count_args(args, 1):
            log_msg = 'Unable to execute stat command with the given parameters'
            print(f"Error... {log_msg}")
            logger.error(log_msg)
            return

        log_directory = str(args[0]).strip()
        if log_directory == '':
            log_msg = 'log directory parameter is missing'
            print(f"Error... {log_msg}")
            logger.error(log_msg)
            return

        if not os.path.exists(log_directory):
            log_msg = 'log directory were not found'
            print(f"Error... {log_msg}")
            logger.error(log_msg)
            return

        if not log_directory.endswith(os.sep):
            log_directory = log_directory + os.sep

        log_file_list = []
        for logfile in os.listdir(log_directory):
            if not os.path.isfile(log_directory + logfile):
                continue
            log_file_list.append((logfile, os.stat(log_directory + logfile).st_mtime))

        if len(log_file_list) > windows_size:
            sorted_log_file_list = sorted(log_file_list, key=lambda x: x[1])
            while len(sorted_log_file_list) > windows_size:
                try:
                    os.remove(log_directory + sorted_log_file_list[0][0])
                    sorted_log_file_list.remove(sorted_log_file_list[0])
                except OSError as err:
                    log_msg = f'unable to remove log file error: {err}'
                    print(f"Error... {log_msg}")
                    logger.error(log_msg)
                    return

        logging.info('clean command executed successfully')

    @classmethod
    def get_help(cls):
        print('\n'.join(['Clean old logs file and keep the latest 5 logs files.',
                         'Usage: clean <path/to/logs/directory>',
                         ]))


if __name__ == '__main__':
    log_dir = r'T:\GM\test\log'
    clean1 = Clean()
    clean1.execute(f'{log_dir}')
