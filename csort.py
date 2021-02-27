from command import CommandFactory, CommandBase
from os import path
import command_utils
import os
import pathlib
import shutil
import logging

logger = logging.getLogger('root')


@CommandFactory.register('sort')
class Sort(CommandBase):
    def execute(self, args):
        self.__command_sort(args)

    @classmethod
    def __do_sort(cls, directory):
        files_dictionary = {}
        if not directory.endswith(os.sep):
            directory = directory + os.sep

        for f in os.listdir(directory):
            if not os.path.isfile(directory + f):
                continue

            file_extension = pathlib.Path(f).suffix
            file_extension = file_extension[1:]  # remove the .
            if not path.exists(directory + file_extension):
                os.makedirs(directory + file_extension)
            try:
                shutil.move(directory + f, directory + file_extension)
                if file_extension not in files_dictionary:
                    files_dictionary[file_extension] = 1
                else:
                    count = files_dictionary[file_extension]
                    files_dictionary[file_extension] = count + 1
            except shutil.Error:
                log_msg = f'Unable to move the {directory + f} file'
                # print(f"Error... {log_msg}")
                logger.error(log_msg)

        return files_dictionary

    @classmethod
    def __command_sort(cls, *args):
        """
        :param args: <path/to/the/files/directory>
                     --hash=<path/to/the/results/file>
        :return: None
        """
        if not command_utils.count_args(args, 2):
            log_msg = 'Unable to execute stat command with the given parameters'
            print(f"Error... {log_msg}")
            logger.error(log_msg)
            return

        given_file_dir = str(args[0]).strip().split()[0]
        given_result_file = command_utils.extract_args(args, '--hash=')
        if given_result_file == '':
            log_msg = 'hash file parameter is missing'
            print(f"Error... {log_msg}")
            logger.error(log_msg)
            return

        if os.path.exists(given_file_dir) and os.path.exists(os.path.dirname(given_result_file)):
            files_report = cls.__do_sort(given_file_dir)
            csv_columns = 'File Type,Count\n'
        else:
            log_msg = 'unable to find the given directory'
            print(f"Error... {log_msg}")
            logger.error(log_msg)
            return
        if command_utils.create_csv_result_file(csv_columns, files_report, given_result_file):
            logging.info('sort command executed successfully')
        else:
            log_msg = 'unable to save the report file'
            print(f"Error... {log_msg}")
            logger.error(log_msg)
            return

    @classmethod
    def get_help(cls):
        print('\n'.join(['Sort files in specific directory and create files information on csv file. ',
                         'Usage: sort <path/to/files/directory> --hash=<path/to/the/results/file>',
                         ]))


if __name__ == '__main__':
    test_file_dir = r'T:\GM\test\mixed'
    test_result_file = r'T:\GM\test\result.csv'
    sort1 = Sort()
    sort1.execute(f'{test_file_dir} --hash={test_result_file}')
