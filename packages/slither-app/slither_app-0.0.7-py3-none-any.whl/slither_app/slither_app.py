# TODO turn this into a module some day

import argparse as ap
import os
import os.path as p
import typing as typ
import datetime as dt
import pprint
import sys

def attach_to_parser(parser):
    """When supplied with an existing `argparse.ArgumentParser` instance,
    adds arguments associated with run_app to it. Example usage:
    
    .. code:: python
    
        parser = ap.ArgumentParser()
        attach_to_parser(parser)
        args = parser.parse_args()

    :param parser: an initialised argument
        parser
    :type parser: argparse.ArgumentParser
    """
    
    # add run_app arguments to parser
    parser.add_argument(
        '-s','--silent',
        action = 'store_true',
        help='''Suppress all messages made by this program.
            Doesn't suppress python exceptions.''',
        dest='CNF_SILENT',
        default=None
    )

    parser.add_argument(
        '-v','--verbose',
        action = 'store_true',
        help='''Increase verbosity. Shows warnings and diagnostic
            messages in addition to errors, which are displayed by
            default.''',
        dest='CNF_VERBOSE',
        default=None
    )

    parser.add_argument(
        '-d','--debug',
        action = 'store_true',
        help='''Enable diagnostic code. May slow the program down
        considerably, only use if something went wrong. Enables verbosity
        as with --verbose, but also shows debug messages in addition.''',
        dest='CNF_DEBUG',
        default=None
    )

    parser.add_argument(
        '--dir-work',
        action = 'store',
        help = '''Override work directory, for temporary files.''',
        metavar = '/path/to/workdir',
        dest = 'CNF_TMP',
    )

    parser.add_argument(
        '--dir-data',
        action = 'store',
        help = '''Override data directory, for output files''',
        metavar = '/path/to/datadir',
        dest = 'CNF_PRODUCTS',
    )

def create_parser(parse_args: bool =False) -> typ.Tuple[ap.ArgumentParser, typ.Optional[ap.Namespace]]:
    """Creates a parser with run_app arguments. If ``parse_args`` is ``True``,
    parses arguments and returns the parsed argparse.Namespace object
    along with the parser instance. If it is ``False``, returns None
    along with the parser instance.

    :param parse_args: Whether to parse arguments , defaults to False
    :type parse_args: bool, optional
    :return: A tuple containing the argument parser instance and either
        None, or the Namespace object
    :rtype: (`ap.ArgumentParser`, ``None``) or (`ap.ArgumentParser`, `ap.Namespace`)
    """
    
    parser = ap.ArgumentParser()

    attach_to_parser(parser)

    if parse_args:
        args = parser.parse_args()
    else:
        args = None

    return parser, args


class Env_parser():

    def __init__(self,arg_parser=None,parsed_args=None,defaults=None):

        # get parser and parsed args from function arguments
        self.parser = arg_parser
        self.args = parsed_args if parsed_args is not None else ap.Namespace()
        filename = sys.argv[0].split("/")[-1].split(".")[0]

        self.arglist = ['CNF_SILENT','CNF_DEBUG','CNF_VERBOSE','CNF_TMP','CNF_PRODUCTS']
        # set default defaults
        self.defaults = {
            'CNF_SILENT': False,
            'CNF_DEBUG': False,
            'CNF_VERBOSE': False,
            'CNF_TMP': p.expanduser(f'~/work/{filename}'),
            'CNF_PRODUCTS': p.expanduser(f'~/data/{filename}'),
        }

        # if defaults provided, overwrite default defaults with them,
        # but do it key by key, so keys that are not provided still
        # retain the default default.
        if type(defaults) == 'dict':
            for key in defaults.keys():
                self.defaults[key] = defaults[key]

        # if provided defaults is not a dict, raise an error
        elif defaults is not None:
            raise TypeError(
                "Env parser instantiation argument `defaults` must be a "
                "dict. See init function docstring."
                )


    def parse_env(self):

        # create list for bool args so they can be correctly set by env vars
        bools = []

        # fill the list of bool args with the arg variable (destination) names
        # but only if parser is present.
        if self.parser is not None:
            for arg in self.parser.__dict__['_actions']:
                if type(arg) == ap._StoreTrueAction:
                    bools.append(arg.dest)

        # go over each arg
        for arg in self.arglist:

            # if command line argument exists
            if getattr(self.args,arg,None) is not None:
                # let it be, let it be, there will be an answer, let it be
                continue

            # if not, but environment variable exists
            elif os.getenv(arg):
                # override the default value

                # if it's one of the booleans, set True regardless of value (but
                # ignore empty string too, just in case)
                if arg in bools and getattr(self.args,arg) != '':
                    setattr(self.args,arg,True)
                # otherwise use the value
                setattr(self.args,arg,os.getenv(arg))

            # if neither exists, use default
            else:
                setattr(self.args,arg,self.defaults[arg])

    def push_env(self):
        # pushes args back to the env vars
        for arg in self.arglist:
            if arg in self.args.__dict__:
                value = getattr(self.args, arg)
                if value:
                    os.environ[arg] = str(getattr(self.args, arg))
                elif not value:
                    os.environ.pop(arg, None)
            else:
                setattr(self.args,arg,False)
        
########################################################################
# region Default arg/config values
# should mirror argument parser options if they're to have any defaults


# endregion
########################################################################


########################################################################
# region Environment variable parser

# Parses environment variables and makes sure that paths exist.

# Only accepts env vars with a corresponding command line argument. When
# adding env var options, please add a command line arg as well.



#endregion
########################################################################


########################################################################
# region Verbosity handling and other printy stuff

class Loudmouth:
    
    def __init__(self,args):
        
        self.args = args

    def _message(self, message,severity=None):
        """Prints messages to stdout.

        Args:
            `message` (`str`): the message to print
            `severity` (`str`, optional): Indicates the severity of the
            message.
            Either of: `'error'`, `'warning'`. Defaults to `''`.
        """

        stamp = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        severity_string = ' '+severity.upper()+':' if severity else ''
        print(f'[{stamp}] grib_prep:{severity_string} {message}')

    # define message function based on verbosity options
    # nothing if silent, overrides all other verbosity
    
    def message(self, message, severity=None):
        
        if self.args.CNF_SILENT:
            pass
        
        # print everything, overrides verbose
        elif self.args.CNF_DEBUG:
            self._message(message, severity)
            
        # print everything except debug messages if verbose
        elif self.args.CNF_VERBOSE and severity != 'debug':
            self._message(message, severity)
            
        # only errors and warnings by default
        else:
            if severity in ('error','warning'):
                self._message(message, severity)


class Loudmouth_child(Loudmouth):
    
    def __init__(self):
        
        self.envparser = Env_parser()
        self.envparser.parse_env()
        self.args = self.envparser.args
    
# endregion
########################################################################