""" pynchon.plugins.pandoc
"""

from fleks import cli

from fleks.util import tagging  # noqa

from pynchon import abcs, events, models  # noqa
from pynchon.util import lme, typing  # noqa

LOGGER = lme.get_logger(__name__)


class Pandoc(models.Planner):
    """Tool for working with Pandoc"""

    class config_class(abcs.Config):
        config_key: typing.ClassVar[str] = "pandoc"
        docker_image: str = typing.Field(default="pandoc/latex:latest")
        pdf_args: typing.List = typing.Field(
            default=["--toc", "--variable fontsize=10pt"]
        )

    name = "pandoc"
    cli_name = "pandoc"
    cli_label = "Tool"
    contribute_plan_apply = False

    # def plan(self, **kwargs):
    #     plan = super().plan()
    # @cli.click.flag("-b", "--bash", help="only bash codeblocks")
    @tagging.tags(click_aliases=["markdown.to-pdf"])
    @cli.options.output_file
    @cli.click.argument("file")
    def md_to_pdf(
        self,
        file: str = None,
        output: str = None,
    ):
        # -> ElementList:
        """
        Converts markdown files to PDF with pandoc
        """
        output = abcs.Path(output or f"{abcs.Path(file).stem}.pdf")
        pandoc_docker = self["docker_image"]
        docker_image = self["docker_image"]
        pdf_args = " ".join(self["pdf_args"])
        cmd = f"docker run -v `pwd`:/workspace -w /workspace {docker_image} {file} {pdf_args} -o {output}"
        plan = super().plan()
        plan.append(self.goal(resource=output.absolute(), type="render", command=cmd))
        return self.apply(plan=plan)
