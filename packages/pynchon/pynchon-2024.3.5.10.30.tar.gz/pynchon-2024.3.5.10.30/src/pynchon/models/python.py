""" pynchon.models.python
"""

from fleks.models import BaseModel

from pynchon import abcs
from pynchon.util import lme, typing

LOGGER = lme.get_logger(__name__)


class EntrypointMetadata(BaseModel):
    is_click: bool = typing.Field(help="", required=False, default=False)
    is_package: bool = typing.Field(help="", required=False, default=False)
    is_module: bool = typing.Field(help="", required=False, default=True)
    bin_name: typing.StringMaybe = typing.Field(
        help="Name for this console script. (Nil if module-entrypoint)",
        required=False,
        default=None,
    )
    help_command: typing.StringMaybe = typing.Field(
        help="Command that returns help for this entrypoint",
        required=False,
        default=None,
    )
    dotpath: str = typing.Field(
        help="",
        required=True,
    )
    file: str = typing.Field(
        help="",
        required=True,
    )
    resource: abcs.Path = typing.Field(help="", required=True)
    path: abcs.Path = typing.Field(help="", required=True)
    entrypoints: typing.List = typing.Field(help="", required=False, default=[])
    src_root: abcs.Path = typing.Field(required=True)

    @property
    def src_url(self) -> str:
        return "/" + str(self.path.relative_to(self.src_root.parent))
        # return abcs.Path(path).absolute().relative_to(abcs.Path(git_root).absolute())

    @property
    def help_invocation(self):
        if self.help_command is not None:
            return self.help_command
        elif self.is_module:
            return f"python -m{self.dotpath} --help"
        # if self.is_package:
        #     return f""
        raise ValueError(f"Cannot determine help_invocation for {self}")

    @property
    def help_output(self):
        """
        Computes help-output given help-invocation.
        WARNING: obviously this has side-effects;
        if help-invocation is not safe to run, then it should be set to `None`
        """
        from pynchon.util.os import invoke

        if self.help_invocation:
            cmd = invoke(self.help_invocation)
            if cmd.succeeded:
                help = cmd.stdout.lstrip().strip()
                help = f"$ {self.help_invocation}\n\n{help}"
            else:
                LOGGER.critical(
                    f"ERROR: failure executing command (cannot extract help!)\n\ncommand='{self.help_invocation}'\n\nerror follows:\n\n{cmd.stderr}"
                )
                help = f"Failed to capture help from command `{self.help_invocation}`"
            return help
        else:
            import IPython

            IPython.embed()
            raise Exception(self)

    @property
    def module(self):
        return (
            f"{self.dotpath}.__main__"
            if str(self.file).endswith("__main__.py")
            else self.dotpath
        )
