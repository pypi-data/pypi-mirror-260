import sys
from dataclasses import dataclass
from enum import unique
from pathlib import Path
from typing import List, Dict

scripts_dir_path = Path(__file__).parent.resolve()  # containing directory
sys.path.insert(0, str(scripts_dir_path))

from Shared import certoraValidateFuncs as Vf
from Shared import certoraUtils as Util
from Shared import certoraAttrUtil as AttrUtil

@dataclass
class MutateArgument(AttrUtil.BaseArgument):
    pass

@unique
class MutateAttribute(AttrUtil.BaseAttribute):

    CONF = MutateArgument(
        help_msg="Settings for both the prover and the mutation engine",
        attr_validation_func=Vf.validate_json5_file,
        argparse_args={
            'type': Path,
            'action': AttrUtil.UniqueStore,
            'required': True
        }
    )

    ORIG_RUN = MutateArgument(
        help_msg="Link to a previous run of the prover on the original program.",
        attr_validation_func=Vf.validate_orig_run,
        argparse_args={
            'action': AttrUtil.UniqueStore
        }
    )

    MSG = MutateArgument(
        help_msg="Add a message to identify the certoraMutate run.",
        attr_validation_func=Vf.validate_msg,
        argparse_args={
            'action': AttrUtil.UniqueStore
        }
    )

    SERVER = MutateArgument(
        argparse_args={
            'action': AttrUtil.UniqueStore
        }
    )

    DEBUG = MutateArgument(
        arg_type=AttrUtil.AttrArgType.BOOLEAN,
        help_msg="Turn on verbose debug prints.",
        argparse_args={
            'action': AttrUtil.STORE_TRUE
        }
    )

    ORIG_RUN_DIR = MutateArgument(
        help_msg="The folder where the files will be downloaded from the original run link.",
        # attr_validation_func=Vf.validate_writable_path,
        argparse_args={
            'type': Path,
            'action': AttrUtil.UniqueStore
        }
    )

    OUTDIR = MutateArgument(
        help_msg="Specify output directory for all gambit runs (defaults to gambit_out)",
        # attr_validation_func=Vf.validate_writable_path,
        argparse_args={
            'type': Path,
            'action': AttrUtil.UniqueStore
        }
    )

    GAMBIT_ONLY = MutateArgument(
        arg_type=AttrUtil.AttrArgType.BOOLEAN,
        help_msg="Stop processing after generating mutations.",
        argparse_args={
            'action': AttrUtil.STORE_TRUE
        }
    )

    DUMP_FAILED_COLLECTS = MutateArgument(
        # attr_validation_func=Vf.validate_writable_path,
        help_msg="Path to the log file capturing mutant collection failures.",
        argparse_args={
            'type': Path,
            'action': AttrUtil.UniqueStore
        }
    )

    # Sets a file that will store the object sent to mutation testing UI (useful for testing)
    UI_OUT = MutateArgument(
        argparse_args={
            'type': Path,
            'action': AttrUtil.UniqueStore
        }
    )

    DUMP_LINK = MutateArgument(
        help_msg="Write the UI report link to a file.",
        argparse_args={
            'type': Path,
            'action': AttrUtil.UniqueStore
        }
    )

    DUMP_CSV = MutateArgument(
        attr_validation_func=Vf.validate_writable_path,
        argparse_args={
            'type': Path,
            'action': AttrUtil.UniqueStore
        }
    )

    # Synchronous mode
    # Run the tool synchronously in shell
    SYNC = MutateArgument(
        arg_type=AttrUtil.AttrArgType.BOOLEAN,
        argparse_args={
            'action': AttrUtil.STORE_TRUE
        }
    )

    '''
    The file containing the links holding certoraRun report outputs.
    In async mode, run this tool with only this option.
    '''
    COLLECT_FILE = MutateArgument(
        flag='--collect_file',    # added to prevent dup with DUMP_CSV
        # attr_validation_func=Vf.validate_readable_file,
        argparse_args={
            'type': Path,
            'action': AttrUtil.UniqueStore
        }
    )

    '''
   The max number of minutes to poll after submission was completed,
    and before giving up on synchronously getting mutation testing results
   '''
    POLL_TIMEOUT = MutateArgument(
        flag='--poll_timeout',    # added to prevent dup with REQUEST_TIMEOUT
        attr_validation_func=Vf.validate_positive_integer,
        arg_type=AttrUtil.AttrArgType.INT,
        argparse_args={
            'action': AttrUtil.UniqueStore
        }
    )

    # The maximum number of retries a web request is attempted
    MAX_TIMEOUT_ATTEMPTS_COUNT = MutateArgument(
        arg_type=AttrUtil.AttrArgType.INT,
        argparse_args={
            'action': AttrUtil.UniqueStore
        }
    )

    # The timeout in seconds for a web request
    REQUEST_TIMEOUT = MutateArgument(
        attr_validation_func=Vf.validate_positive_integer,
        arg_type=AttrUtil.AttrArgType.INT,
        argparse_args={
            'action': AttrUtil.UniqueStore
        }
    )

    GAMBIT = MutateArgument(
        arg_type=AttrUtil.AttrArgType.MAP,
        argparse_args={
            'action': AttrUtil.NotAllowed
        }
    )
    # todo vvvv - parse_manual_mutations, change warnings to exceptions
    MANUAL_MUTANTS = MutateArgument(
        arg_type=AttrUtil.AttrArgType.MAP,
        flag='--manual_mutants',  # added to prevent dup with GAMBIT
        argparse_args={
            'action': AttrUtil.NotAllowed
        }
    )

    '''
    Add this if you do not wish to wait for the results of the original verification.
    Why not to use it:
    - Wastes resources - all the mutations will be ignored if the original fails
    - We cannot use the solver data from the original run to reduce the run time of the mutants
    Why to use it:
    - Much shorter as everything will be run in parallel
    '''
    #
    OPTIMISTIC_ORIGINAL_RUN = MutateArgument(
        arg_type=AttrUtil.AttrArgType.BOOLEAN,
        flag='--optimistic_original_run',
        argparse_args={
            'action': AttrUtil.STORE_TRUE
        }
    )

    TEST = MutateArgument(
        attr_validation_func=Vf.validate_test_value,
        argparse_args={
            'action': AttrUtil.UniqueStore
        }
    )

    def get_flag(self) -> str:
        return '--' + str(self)

    #  TODO - Move to base (rahav)
    def validate_value(self, value: str) -> None:
        if self.value.attr_validation_func is not None:
            try:
                self.value.attr_validation_func(value)
            except Util.CertoraUserInputError as e:
                msg = f'{self.get_flag()}: {e}'
                if isinstance(value, str) and value.strip()[0] == '-':
                    flag_error = f'{value}: Please remember, CLI flags should be preceded with double dashes. ' \
                                 f'{Util.NEW_LINE}For more help run the tool with the option --help'
                    msg = flag_error + msg
                raise Util.CertoraUserInputError(msg) from None


def get_args(args_list: List[str]) -> Dict:

    parser = AttrUtil.CertoraArgumentParser(prog="certora-mutate CLI arguments and options", allow_abbrev=False)
    args = list(MutateAttribute)

    for arg in args:
        flag = arg.get_flag()
        if arg.value.arg_type == AttrUtil.AttrArgType.INT:
            parser.add_argument(flag, help=arg.value.help_msg, type=int, **arg.value.argparse_args)
        else:
            parser.add_argument(flag, help=arg.value.help_msg, **arg.value.argparse_args)
    return vars(parser.parse_args(args_list))
