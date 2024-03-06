""" pynchon.plugins.jinja
"""

from fleks import tagging

from pynchon import abcs, api, cli, models

from pynchon.util import files, lme, text, typing  # noqa

LOGGER = lme.get_logger(__name__)


@tagging.tags(click_aliases=["j"])
class Jinja(models.Planner):
    """Renders files with {jinja.template_includes}"""

    # diff --color --minimal -w --side-by-side /etc/bash.bashrc <(bash --pretty-print /etc/bash.bashrc )

    class config_class(abcs.Config):
        config_key: typing.ClassVar[str] = "jinja"
        template_includes: typing.List[str] = typing.Field(default=[])
        exclude_patterns: typing.List[str] = typing.Field()

        # @tagging.tagged_property(conflict_strategy="override")
        @property
        def exclude_patterns(self):
            from pynchon.config import globals

            # globals = plugin_util.get_plugin("globals").get_current_config()
            global_ex = globals.exclude_patterns
            my_ex = self.__dict__.get("exclude_patterns", [])
            return list(set(global_ex + my_ex + ["**/pynchon/templates/includes/**"]))

    name = "jinja"
    priority = 7
    COMMAND_TEMPLATE = (
        "python -mpynchon.util.text render jinja "
        "{src} --context-file {context_file} "
        "--output {output} {template_args}"
    )

    # cli_subsumes: typing.List[typing.Callable] = [
    #     # render_main.j2cli,
    #     # render_main.jinja_file,
    # ]

    def _get_jinja_context(self):
        """ """
        fname = ".tmp.jinja.ctx.json"
        with open(fname, "w") as fhandle:
            fhandle.write(text.to_json(self.project_config))
        return f"{fname}"

    @property
    def _include_folders(self):
        includes = self.project_config.jinja["template_includes"]
        from pynchon import api

        includes = api.render.get_jinja_includes(*includes)
        return includes

    @cli.click.flag("--local")
    def list_includes(
        self,
        local: bool = False,
    ):
        """Lists full path of each include-file"""
        includes = self._include_folders
        if local:
            includes.remove(api.render.PYNCHON_CORE_INCLUDES)
        includes = [abcs.Path(t) / "**/*.j2" for t in includes]
        LOGGER.warning(includes)
        matches = files.find_globs(includes)
        return matches

    @cli.click.flag("--local")
    def list_include_args(
        self,
        local: bool = False,
    ):
        """
        Lists all usable {% include ... %} values
        """
        includes = self.list_includes(local=local)
        out = []
        for fname in includes:
            fname = abcs.Path(fname)
            for inc in self._include_folders:
                try:
                    fname = fname.relative_to(inc)
                except ValueError:
                    continue
                else:
                    out.append(fname)
                break
            else:
                pass
        return out

    @tagging.tags(click_aliases=["ls"])
    def list(self, changes=False):
        """
        Lists affected resources for this project
        """
        default = self[:"project"]
        proj_conf = self[:"project.subproject":default]
        project_root = proj_conf.get("root", None) or self[:"git.root":"."]
        # project_root = proj_conf.get("root", None) or '.'
        globs = [
            abcs.Path(project_root).joinpath("**/*.j2"),
        ]
        self.logger.debug(f"search patterns are {globs}")
        result = files.find_globs(globs)
        self.logger.debug(f"found {len(result)} j2 files (pre-filter)")
        excludes = self["exclude_patterns"]
        self.logger.debug(f"filtering search with {len(excludes)} excludes")
        result = [p for p in result if not p.match_any_glob(excludes)]
        self.logger.debug(f"found {len(result)} j2 files (post-filter)")
        if not result:
            err = f"{self.__class__.__name__} is active, but found no .j2 files!"
            self.logger.critical(err)
        return result

    def plan(
        self,
        config=None,
    ) -> typing.List:
        """Creates a plan for this plugin"""

        def _get_template_args():
            """ """
            # import IPython; IPython.embed()
            templates = self["template_includes"]
            templates = [t for t in templates]
            templates = [f"--include {t}" for t in templates]
            templates = " ".join(templates)
            return templates

        plan = super(self.__class__, self).plan()
        jctx = self._get_jinja_context()
        templates = _get_template_args()
        for src in self.list():
            output = str(src).replace(".j2", "")
            plan.append(
                self.goal(
                    type="render",
                    resource=output,
                    command=self.COMMAND_TEMPLATE.format(
                        src=src,
                        context_file=jctx,
                        template_args=templates,
                        output=output,
                    ),
                )
            )
        return plan.finalize()
