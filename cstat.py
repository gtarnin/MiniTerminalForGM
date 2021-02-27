from command import CommandFactory, CommandBase
import os
import command_utils
import logging

logger = logging.getLogger('root')

# log format:
LOG_DATE = 0
LOG_RESULT = 1
LOG_COMMAND = 2
LOG_TEXT = 3
LOG_LINE_IS_VALID = 4


# log file format
# 2021-02-25-10:30:58:2000 ERROR DOING_SOMETHING1 text text text text text text text ....
# 2021-02-25-10:30:59:3222 OK DOING_SOMETHING2 text text text text text text text ....


@CommandFactory.register('stat')
class Stat(CommandBase):

    def execute(self, args):
        self.__command_stat(args)

    @classmethod
    def __get_command_stat(cls, dic):
        max_failed = 0
        most_usage = 0
        lease_usage = -1
        most_failed = ''
        most_usage_command = ''
        lease_usage_command = ''

        for command in dic:
            if lease_usage == -1 or dic[command][0] <= lease_usage:
                lease_usage = dic[command][0]
                lease_usage_command = command
            if dic[command][0] >= most_usage:
                most_usage = dic[command][0]
                most_usage_command = command
            if dic[command][1] >= max_failed:
                max_failed = dic[command][1]
                most_failed = command

        return {'Most Failed Command': most_failed,
                'Most frequently used command': most_usage_command,
                'Least frequently used command': lease_usage_command}

    @classmethod
    def __get_file_stat(cls, logfile):
        local_dictionary = {}
        with open(logfile, 'r') as f:
            for log_line in f:
                split_line = log_line.split(" ")
                if len(split_line) < LOG_LINE_IS_VALID:
                    continue
                command = split_line[LOG_COMMAND]
                result = split_line[LOG_RESULT]
                if command not in local_dictionary:
                    # init new command with 0 usage and 0 failed
                    local_dictionary[command] = [0, 0]

                count = local_dictionary[command][0]
                local_dictionary[command][0] = count + 1

                if result != 'OK':
                    failed = local_dictionary[command][1]
                    local_dictionary[command][1] = failed + 1

        return local_dictionary

    @classmethod
    def __do_stat(cls, directory, csv_result_file, timestamp):
        if not directory.endswith(os.sep):
            directory = directory + os.sep

        stat_dictionary = {}
        merged_dictionary = {}

        for logfile in os.listdir(directory):
            if not os.path.isfile(directory + logfile):
                continue

            if os.stat(directory + logfile).st_mtime >= float(timestamp):
                merged_dictionary = stat_dictionary | cls.__get_file_stat(directory + logfile)
                stat_dictionary = merged_dictionary

        # need to do here dic sorting instead of dic searching
        csv_header = 'Subject,Command\n'
        if command_utils.create_csv_result_file(csv_header, cls.__get_command_stat(merged_dictionary), csv_result_file):
            logging.info('stat command executed successfully')
        else:
            log_msg = 'unable to save the results file'
            # print(f"Error... {log_msg}")
            logger.error(log_msg)

    @classmethod
    def __command_stat(cls, *args):
        """
        :param args: <path/to/the/logs/directory>
                     --csv=<path/to/the/statistic/file>
                     --ts=<timestamp to start from>
        :return: None
        """
        if not command_utils.count_args(args, 3):
            log_msg = 'Unable to execute stat command with the given parameters'
            print(f"Error... {log_msg}")
            logger.error(log_msg)
            return

        logs_dir = str(args[0]).strip().split(' ')
        logs_dir = logs_dir[0]

        given_csv_file = command_utils.extract_args(args, '--csv=')
        if given_csv_file == '':
            log_msg = 'csv file parameter is missing'
            print(f"Error... {log_msg}")
            logger.error(log_msg)
            return

        given_timestamp = command_utils.extract_args(args, '--ts=')
        if given_timestamp == '':
            log_msg = 'time stamp parameter is missing'
            print(f"Error... {log_msg}")
            logger.error(log_msg)
            return

        if os.path.exists(logs_dir):
            cls.__do_stat(logs_dir, given_csv_file, given_timestamp)
        else:
            log_msg = 'invalid logs directory'
            print(f"Error... {log_msg}")
            logger.error(log_msg)
            return

    @classmethod
    def get_help(cls):
        print('\n'.join(['Go over the logs files, collect statistic from given time stamp and keep it on csv file. ',
                         'Usage: stat <path/to/logs/directory> --csv=<path/to/the/statistic/file> '
                         '--ts=<timestamp to start from>',
                         ]))


if __name__ == '__main__':
    log_dir = r'T:\GM\test\log'
    time_to_check = 1614236436.2065954
    csv_file = r'T:\GM\test\stat_res.csv'
    stat1 = Stat()
    stat1.execute(f'{log_dir} --csv={csv_file} --ts={time_to_check}')
