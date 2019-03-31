from __future__ import unicode_literals

import argparse

import dvc.logger as logger
from dvc.exceptions import DvcException
from dvc.command.base import CmdBase, append_doc_link


class CmdCommit(CmdBase):
    def run(self):
        if not self.args.targets:
            self.args.targets = [None]

        for target in self.args.targets:
            try:
                self.repo.commit(
                    target,
                    with_deps=self.args.with_deps,
                    recursive=self.args.recursive,
                    force=self.args.force,
                )
            except DvcException:
                logger.error(
                    "failed to commit{}".format(
                        (" " + target) if target else ""
                    )
                )
                return 1
        return 0


def add_parser(subparsers, parent_parser):
    COMMIT_HELP = "Save changed data to cache and update DVC files."

    commit_parser = subparsers.add_parser(
        "commit",
        parents=[parent_parser],
        description=append_doc_link(COMMIT_HELP, "commit"),
        help=COMMIT_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    commit_parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        default=False,
        help="Commit even if checksums for dependencies/outputs changed.",
    )
    commit_parser.add_argument(
        "-d",
        "--with-deps",
        action="store_true",
        default=False,
        help="Commit all dependencies of the specified target.",
    )
    commit_parser.add_argument(
        "-R",
        "--recursive",
        action="store_true",
        default=False,
        help="Commit cache for subdirectories of the specified directory.",
    )
    commit_parser.add_argument(
        "targets", nargs="*", default=None, help="DVC files."
    )
    commit_parser.set_defaults(func=CmdCommit)