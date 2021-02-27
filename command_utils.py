import logging

logger = logging.getLogger('root')

"""Global Utils for command executing"""


def extract_args(command_line, arg_identity):
    """
    :param command_line: the row command args
    :param arg_identity: argument identity (e.g. --script=)
    :return: the argument value if found or '' if not
    """

    if len(command_line) == 0:
        return ''

    command_line = str(command_line[0]).strip()
    found_arg = []
    command_line = command_line.split(' ')
    for param in command_line:
        if param.startswith(arg_identity):
            found_arg = param.split('=')
            break

    if len(found_arg) < 2 or found_arg[1] == '':
        return ''

    return found_arg[1]


def create_csv_result_file(csv_columns, files_report, result_file):
    """
    :param csv_columns: csv columns header as string
    :param files_report: dictionary with the relevant information
    :param result_file: the csv file as the result file
    :return: None
    """
    try:
        with open(result_file, 'w') as f:
            f.writelines(csv_columns)
            for key in files_report.keys():
                f.write("%s,%s\n" % (key, files_report[key]))
    except IOError:
        log_msg = f'unable to write the result file!'
        print(f"Error... {log_msg}")
        logger.error(log_msg)
        return False
    return True


def count_args(args, expected):
    """
    :param args: row command line arguments
    :param expected: how many args it should contains
    :return: 0 if not as expected, 1 if all OK
    """
    args = str(args[0]).split(' ')

    if expected > 0:
        if len(args) == 0 or len(args) > expected or len(args) < expected:
            return False
    return True
