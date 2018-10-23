from argparse import ArgumentParser
import os.path


class InputHelper(object):
    @staticmethod
    def readable_file(parser, arg):
        if not os.path.exists(arg):
            parser.error("The file %s does not exist!" % arg)
        else:
            return open(arg, 'r')  # return an open file handle

    @staticmethod
    def process_targets(arguments):
        targets = set()

        if arguments.target:
            targets.add(arguments.target)
        else:
            for target in arguments.target_list:
                targets.add(target.strip())

        return targets

    @staticmethod
    def process_commands(arguments):
        commands = set()

        if arguments.command:
            commands.add(arguments.target)
        else:
            for command in arguments.command_list:
                commands.add(command.strip())

        return commands

class InputParser(object):
    def __init__(self):
        self._parser = self.setup_parser()

    def parse(self, argv):
        return self._parser.parse_args(argv)

    @staticmethod
    def setup_parser():
        parser = ArgumentParser()

        targets = parser.add_mutually_exclusive_group(required=True)

        targets.add_argument(
            '-t', dest='target', required=False,
            help='Specify a target or domain name.'
        )

        targets.add_argument(
            '-tL', dest='target_list', required=False,
            help='Specify a list of targets or domain names.',
            metavar="FILE",
            type=lambda x: InputHelper.readable_file(parser, x)
        )

        commands = parser.add_mutually_exclusive_group(required=True)
        commands.add_argument(
            '-c', dest='command',
            help='Specify a single command to execute.'
        )

        commands.add_argument(
            '-cL', dest='command_list', required=False,
            help='Specify a list of commands to execute',
            metavar="FILE",
            type=lambda x: InputHelper.readable_file(parser, x)
        )

        output = parser.add_mutually_exclusive_group()
        output.add_argument(
            '-oN', dest='output_normal',
            help='Normal output printed to a file when the -oN option is '
                 'specified with a filename argument.'
        )

        output.add_argument(
            '-oJ', dest='output_json',
            help='JSON output printed to a file when the -oJ option is '
                 'specified with a filename argument.'
        )

        output.add_argument(
            '-oG', dest='output_grepable',
            help='Grepable output printed to a file when the -oG option is '
                 'specified with a filename argument.'
        )


        parser.add_argument(
            '--no-color', dest='nocolor', action='store_true', default=False,
            help='If set then any foreground or background colours will be '
                 'stripped out.'
        )

        output_types = parser.add_mutually_exclusive_group()
        output_types.add_argument(
            '-v', '--verbose', dest='verbose', action='store_true', default=False,
            help='If set then verbose output will be displayed in the terminal.'
        )
        output_types.add_argument(
            '--silent', dest='silent', action='store_true', default=False,
            help='If set only findings will be displayed and banners '
                 'and other information will be redacted.'
        )

        return parser
