""" pynchon.plugins.markdown
"""

import marko
from fleks import tagging
from marko.ast_renderer import ASTRenderer

from pynchon import abcs, api, cli, events, models  # noqa
from pynchon.util import lme, typing  # noqa

LOGGER = lme.get_logger(__name__)

ElementList = typing.List[typing.Dict]
# from pynchon.plugins.tests import DocTestSuite
# markdown_suite = DocTestSuite(
#     suite_name="markdown",
# )


class Markdown(models.CliPlugin):
    """Markdown"""

    class config_class(abcs.Config):
        config_key: typing.ClassVar[str] = "markdown"
        goals: typing.List[str] = typing.Field(default=[])
        include_patterns: typing.List[str] = typing.Field(default=[])
        exclude_patterns: typing.List[str] = typing.Field(default=[])
        root: typing.Union[str, abcs.Path, None] = typing.Field(default=None)
        # tests: DocTestSuite = typing.Field(default=markdown_suite)

    name = "markdown"
    # @cli.click.flag("-p", "--python", help="only python codeblocks")
    cli_name = "markdown"
    priority = 0

    @cli.click.flag("-p", "--python", help="only python codeblocks")
    @cli.click.flag("-b", "--bash", help="only bash codeblocks")
    @cli.click.argument("file")
    def doctest(
        self,
        file: str = None,
        python: bool = False,
        bash: bool = False,
    ) -> ElementList:
        assert python or bash
        element_lst = self.parse(file=file, python=python, bash=bash)
        if not element_lst:
            LOGGER.critical(f"filtered element list is empty! {element_lst}")

        def _doctest(element):
            LOGGER.critical(element)
            child = element["children"][0]
            assert child["element"] == "raw_text"
            script: str = child["children"]
            raise Exception(script)
            # return #shil.invoke(script,...))

        for el in element_lst:
            el.update(_doctest(el))
        return element_lst

    @tagging.tags(click_aliases=["parse.markdown"])
    @cli.click.flag("-c", "--codeblocks", help="only codeblocks")
    @cli.click.flag("-p", "--python", help="only python codeblocks")
    @cli.click.flag("-b", "--bash", help="only bash codeblocks")
    @cli.click.argument("file")
    def parse(
        self,
        file: str = None,
        codeblocks: bool = False,
        python: bool = False,
        bash: bool = False,
    ) -> ElementList:
        """parses given markdown file into json"""
        codeblocks = codeblocks or python or bash
        assert file
        with open(file) as fhandle:
            content = fhandle.read()

        parsed = marko.Markdown(renderer=ASTRenderer)(content)
        # def walk(thing):
        #     LOGGER.critical(thing)
        #     if isinstance(thing, (dict,)):
        #         children = thing.pop('children', [])
        #         if isinstance(children,(str,)):
        #             return children
        #         if not children:
        #             return thing
        #         else:
        #             return [walk(ch) for ch in children]
        #     if isinstance(thing, (list,)):
        #         return [walk(x) for x in thing]
        #     else:
        #         return thing
        #
        children = parsed["children"]
        out = []
        for child in children:
            if child.get("element") == "fenced_code":
                lang = child.get("lang")
                if lang is not None:
                    out.append(child)
        LOGGER.critical(child)
        if python:
            out = [ch for ch in out if child.get("lang") == "python"]
        if bash:
            out = [ch for ch in out if child.get("lang") == "bash"]
        # out=[]
        # for child in children:
        #     if bash and lang=='bash':
        #         child['code'] = ''.join([
        #             x['children'] for x in tmp ])
        #         out.append(child)
        #     elif python and lang=='python':
        #         child['code'] = ''.join([
        #             x['children'] for x in tmp ])
        #         out.append(child)

        return out
        # for child in children:
        #     result import pydash
        # flat = pydash.flatten_deep(children)
        # flat = [pydash.flatten_deep(x) for x in flat]
        # if codeblocks:
        #     result = [x for x in flat if x.get("element") == "fenced_code"]
        # if python:
        #     assert not bash
        #     result = [x for x in result if x.get("lang") == "python"]
        # if bash:
        #     assert not python
        #     result = [x for x in result if x.get("lang") == "bash"]
        # import IPython; IPython.embed()
        # return result

    # plan=None
    # def plan(self, config=None):
    #     """Describe plan for this plugin"""
    #     plan = super().plan(config=config)
    #     return plan
    # resources = [abcs.Path(fsrc) for fsrc in self.list()]
    # self.logger.warning("Adding user-provided goals")
    # for g in self["goals"]:
    #     plan.append(self.goal(command=g, resource="?", type="user-config"))
    #
    # self.logger.warning("Adding file-header related goals")
    # cmd_t = "python -mpynchon.util.files prepend --clean "
    # loop = self._get_missing_headers(resources)
    # for rsrc in loop["files"]:
    #     if rsrc.match_any_glob(self["exclude_patterns"::[]]):
    #         continue
    #     ext = rsrc.full_extension()
    #     ext = ext[1:] if ext.startswith(".") else ext
    #     # fhdr = header_files[ext]
    #     fhdr = self._render_header_file(rsrc)
    #     plan.append(
    #         self.goal(
    #             resource=rsrc,
    #             type="change",
    #             label=f"Adding file header for '{ext}'",
    #             command=f"{cmd_t} {fhdr} {rsrc}",
    #         )
    #     )
