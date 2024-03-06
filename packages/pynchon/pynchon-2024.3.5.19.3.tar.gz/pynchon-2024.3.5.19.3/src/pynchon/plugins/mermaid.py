""" pynchon.plugins.mermaid
"""

import os

from fleks import cli, tagging

from pynchon.util.os import invoke

from pynchon import abcs, events, models  # noqa
from pynchon.util import files, lme, typing  # noqa

LOGGER = lme.get_logger(__name__)
IMG = "ghcr.io/mermaid-js/mermaid-cli/mermaid-cli"


class Mermaid(models.Planner):
    """Mermaid Plugin"""

    class config_class(abcs.Config):
        config_key: typing.ClassVar[str] = "mermaid"
        apply_hooks: typing.List[str] = typing.Field(default=["open-after"])

    name = "mermaid"
    cli_name = "mermaid"

    @tagging.tags(click_aliases=["ls"])
    def list(self):
        """
        Find mermaid diagrams under `{{project_root}}/**/*.mmd`
        """
        includes = "**/*.mmd"
        search = [
            abcs.Path(self.project_root).joinpath(includes),
        ]
        self.logger.debug(f"search pattern is {search}")
        result = files.find_globs(search)
        return result

    @cli.options.output
    @cli.click.option("--img", default="nshine/dot")
    # @cli.click.option("--output-mode")
    @cli.click.argument("file", nargs=1)
    def render(
        self,
        img: str = "??",
        file: str = "",
        # output_mode: str = "",
        output: str = "",
    ):
        """
        Renders mermaid diagram to image
        """
        assert output
        wd = self.working_dir
        file = abcs.Path(file).absolute().relative_to(wd)
        output = abcs.Path(output)
        output = output.absolute().relative_to(wd)
        uid = os.getuid()
        cmd = (
            f"docker run -v {wd}:/workspace "
            f"-w /workspace -u {uid} {IMG} -i {file} "
            f"-o {output} --backgroundColor efefef"
        )
        LOGGER.critical(cmd)
        result = invoke(cmd, strict=True)
        return True

    @property
    def output_root(self):
        return abcs.Path(self[:"git.root":]) / "img"

    def plan(
        self,
        config=None,
    ) -> models.Plan:
        """Run planning for this plugin"""
        plan = super(self.__class__, self).plan(config=config)
        self.logger.debug("planning for rendering for .mmd mermaid files..")
        output_mode = "png"
        for inp in self.list():
            rsrc = inp.parents[0] / inp.stem
            rsrc = f"{rsrc}.{output_mode}"
            plan.append(
                self.goal(
                    resource=rsrc,
                    command=(
                        f"pynchon {self.cli_name} " f"render {inp} --output {rsrc} "
                    ),
                    type="render",
                )
            )
        return plan

    # cli_label = "Tool"
    # def run(self):


# mmdc -i input.mmd -o output.png -t dark -b transparent
# https://github.com/mermaid-js/mermaid-cli
