#!/usr/bin/env python3

import sys

from pathlib import Path
from typing import List
from types import SimpleNamespace


scripts_dir_path = Path(__file__).parent.resolve()  # containing directory
sys.path.insert(0, str(scripts_dir_path))

from Shared.certoraLogging import LoggingManager
from Shared import certoraUtils as Util

from Mutate import mutateApp as App
from Mutate import mutateValidate as Mv


def mutate_entry_point() -> None:
    run_mutate(sys.argv[1:])


# signature same as run_certora -> second args only for polymorphism
def run_mutate(sys_args: List[str], _: bool = False) -> None:
    logging_manager = LoggingManager()
    if '--debug' in sys_args:
        logging_manager.set_log_level_and_format(debug=True)

    mutate_app = App.MutateApp()
    mutate_app.get_args(sys_args)
    # args = Attr.get_args(sys_args)
    # mutate_app = App.MutateApp(**args)

    mutate_app.read_conf_file()
    mutate_app.set_defaults()

    if mutate_app.orig_run:
        mutate_app.read_conf_from_orig_run()

    mutate_app.settings_post_parsing()
    Util.check_packages_arguments(SimpleNamespace(**mutate_app.prover_dict))

    validator = Mv.MutateValidator(mutate_app)
    validator.validate()
    mutate_app.validate_args()

    if mutate_app.test == str(Util.TestValue.CHECK_ARGS):
        raise Util.TestResultsReady(mutate_app)

    # default mode is async. That is, we both _submit_ and _collect_
    if mutate_app.sync:
        App.check_key_exists()
        # sync mode means we submit, then we poll for the specified amount of minutes
        # todo - to validate vvvv
        # if not mutate_app.prover_conf and not mutate_app.orig_run:
        #     # sync mode means we submit + collect. If the user just wants to collect, do not add --sync
        #     raise Util.CertoraUserInputError("Must provide a conf file in sync mode. If you wish to poll on a "
        #                                      "previous submission, omit `--sync`.")
        mutate_app.submit()
        mutate_app.poll_collect()
    else:
        # if the user did not supply a conf file or a link to an original run,
        # we will check whether there is a collect file and poll it
        # todo vvvv
        if not mutate_app.conf and not mutate_app.orig_run:
            assert mutate_app.collect_file, \
                "You must use either a prover configuration file, a collect file, or an original run link"
            ready = mutate_app.collect()
            if not ready:
                raise Util.CertoraUserInputError("The report might broken because some "
                                                 "results could not be fetched. "
                                                 f"Check the {mutate_app.collect_file} file to investigate.")
        else:
            App.check_key_exists()
            mutate_app.submit()


if __name__ == '__main__':
    mutate_entry_point()
