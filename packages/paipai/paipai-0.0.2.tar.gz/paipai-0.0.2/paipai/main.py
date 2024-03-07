# This is a sample Python script.
import locale
import os
import sys


from pip._internal.cli.autocompletion import autocomplete
from pip._internal.cli.main_parser import parse_command, create_main_parser
from pip._internal.commands import create_command
from pip._internal.commands.install import InstallCommand
from pip._internal.exceptions import PipError
from pip._internal.utils import deprecation


def cmd_install(args:list):
    pass
def cmd_uninsatll(args:list):
    pass

def main1(args=None):
    # type: (Optional[List[str]]) -> int
    if args is None:
        args = sys.argv[1:]
    # Configure our deprecation warnings to be sent through loggers
    deprecation.install_warning_logger()
    autocomplete()
    try:
        cmd_name, cmd_args = parse_command(args)
        # Needed for locale.getpreferredencoding(False) to work
        # in _pip._internal.utils.encoding.auto_decode
        try:
            locale.setlocale(locale.LC_ALL, '')
        except locale.Error as e:
            # setlocale can apparently crash if locale are uninitialized
            # logger.debug("Ignoring error %s when setting locale", e)
            print(e)
        command = create_command(cmd_name, isolated=("--isolated" in cmd_args))
        options, args = command.parse_args(cmd_args)

        if command == 'install':
            cmd_install(args)

        if command == 'uninstall':
            cmd_uninsatll(args)

    except PipError as exc:
        sys.stderr.write("ERROR: %s" % exc)
        sys.stderr.write(os.linesep)

def main():
    print(sys.argv)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #args = ['install','-i','https://www.baidi.com','arrow']
    print(sys.argv)
    #for arg in sys.argv:
    #    print(arg)