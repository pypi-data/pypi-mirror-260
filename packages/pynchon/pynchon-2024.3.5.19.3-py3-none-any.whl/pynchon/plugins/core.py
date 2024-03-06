""" pynchon.plugins.Core
"""

import fleks
from fleks import tagging

from pynchon import abcs, api, cli, models
from pynchon.bin import entry
from pynchon.core import Config as CoreConfig
from pynchon.util import lme
from pynchon.models import planning

LOGGER = lme.get_logger(" ")

classproperty = fleks.util.typing.classproperty


@tagging.tags(click_aliases=["c"])
class Core(models.Planner):
    """Core Plugin"""

    name = "core"
    priority = -1
    config_class = CoreConfig

    # NB: prevents recursion when `pynchon plan` is used!
    contribute_plan_apply = False

    @classproperty
    def click_group(kls):
        """ """
        kls._finalized_click_groups[kls] = entry
        return kls._finalized_click_groups[kls]

    @classmethod
    def get_current_config(kls):
        """ """
        from pynchon import config as config_mod

        result = getattr(config_mod, kls.get_config_key())
        return result

    def cfg(self):
        """Show current project config (with templating/interpolation)"""
        tmp = self.project_config
        return tmp

    @cli.click.flag("--bash", help="bootstrap bash")
    @cli.click.flag("--bashrc", help="bootstrap bashrc")
    @cli.click.flag("--bash-completions", help="bootstrap completions")
    @cli.click.flag("--pynchon", help="bootstrap .pynchon.json5")
    @cli.click.flag("--makefile", help="bootstrap Makefile")
    @cli.click.flag("--tox", help="bootstrap tox")
    def bootstrap(
        self,
        pynchon: bool = False,
        bash: bool = False,
        bash_completions: bool = False,
        bashrc: bool = False,  # noqa
        makefile: bool = False,
        tox: bool = False,
    ) -> None:
        """Bootstrap for shell integration, etc"""
        template_prefix = f"{self.plugin_templates_prefix}/bootstrap"
        pynchon_completions_script = ".tmp.pynchon.completions.sh"
        bashrc_snippet = ".tmp.pynchon.bashrc"
        if bash_completions:
            pass

            gr = self.__class__.click_entry
            all_known_subcommands = [
                " ".join(x.split()[1:])
                for x in cli.click.subcommand_tree(
                    gr, mode="text", path=tuple(["pynchon"]), hidden=False
                ).keys()
            ]
            # head = [x for x in all_known_subcommands if len(x.split()) == 1]
            # rest = [x for x in all_known_subcommands if x not in head]
            # tmp = collections.defaultdict(list)
            # for phrase in rest:
            #     bits = phrase.split()
            #     k = bits.pop(0)
            #     tmp[k] += bits
            # print(list(tmp.keys()))
            print(all_known_subcommands)
            return
        #   if bash:
        #       rest = [
        #           f"""    '{k}'*)
        #         while read -r; do COMPREPLY+=( "$REPLY" ); done < <( compgen -W "$(_pynchon_completions_filter "{' '.join(subs)}")" -- "$cur" )
        #         ;;
        #       """
        #           for k, subs in tmp.items()
        #       ]
        #       rest += [
        #           f"""    *)
        # while read -r; do COMPREPLY+=( "$REPLY" ); done < <( compgen -W "$(_pynchon_completions_filter "{' '.join(head)}")" -- "$cur" )
        # ;;"""
        #       ]
        #       # LOGGER.warning("This is intended to be run through a pipe, as in:")
        #       # LOGGER.critical("pynchon bootstrap --bash | bash")
        #       tmpl = api.render.get_template(f"{template_prefix}/bash.sh")
        #       content = tmpl.render(head=head, rest="\n".join(rest), **self.config)
        #       files.dumps(content=content, file=pynchon_completions_script)
        #       LOGGER.warning(
        #           f"To refresh your shell, run: `source {pynchon_completions_script}`"
        #       )
        #       return dict()
        # if bashrc:
        #     LOGGER.critical(
        #         "To use completion hints every time they are "
        #         "present in a folder, adding this to .bashrc:"
        #     )
        #     tmpl = api.render.get_template(f"{template_prefix}/bashrc.sh")
        #     content = tmpl.render(pynchon_completions_script=pynchon_completions_script)
        #     files.dumps(content=content, file=bashrc_snippet, logger=LOGGER.info)
        #     return files.block_in_file(
        #         target_file=abcs.Path("~/.bashrc").expanduser(),
        #         block_file=bashrc_snippet,
        #     )
        elif pynchon:
            tmp = abcs.Path(".") / ".pynchon.json5"
            if tmp.exists():
                err = f"Cowardly refusing to recreate {tmp}"
                LOGGER.critical(err)
                raise SystemExit(1)
            else:
                print("pynchon pattern sync . docs --plan")
        elif bash:
            this_cmd = "pynchon bootstrap --bash"  # FIXME: get from click-ctx
            LOGGER.debug("collecting `shell_aliases` from all plugins")
            out = self.siblings.collect_config_dict("shell_aliases")
            out = "\n".join([f"alias {k}='{v}';" for k, v in out.items()])
            print(out)
            LOGGER.warning(f'for this session, use "source <({this_cmd})"')
            LOGGER.warning(f'for it to be permanent, use "{this_cmd} >> ~/.bashrc"')
        elif tox or makefile:
            tail = "Makefile" if makefile else "tox.ini"
            tmpl = api.render.get_template(f"{template_prefix}/{tail}")
            content = tmpl.render(**self.project_config.dict())
            print(content)

    def raw(self) -> None:
        """
        Returns (almost) raw config, without interpolation
        """
        from pynchon.config import RAW  # noqa

        print(RAW.json())

    @property
    def sorted_plugins(self):
        plugins = self.siblings.values()
        plugins = [
            p
            for p in plugins
            if isinstance(p, models.AbstractPlanner) and p.contribute_plan_apply
        ]
        plugins = sorted(plugins, key=lambda p: p.priority)
        return plugins

    def plan(
        self,
        config=None,
        flattened=True,
    ) -> models.Plan:
        """Runs plan for all plugins"""

        config = config or self.project_config
        plan = super(self.__class__, self).plan(config)
        plans = [] if not flattened else None
        plugins = self.sorted_plugins
        self.logger.critical(f"Planning on behalf of: {[p.name for p in plugins]}")
        for plugin_obj in plugins:
            subplan = plugin_obj.plan()
            if not subplan:
                self.logger.warning(
                    f"subplan for '{plugin_obj.__class__.__name__}' is empty!"
                )
            else:
                if flattened:
                    for g in subplan.goals:
                        self.logger.info(f"{plugin_obj} contributes {g}")
                        plan.append(g)
                else:
                    plans.append(subplan)
        return plan.finalize() if flattened else plans

    @cli.click.option("--parallelism", "-p", default="1", help="Paralellism")
    @cli.click.flag("--fail-fast", default=False, help="fail fast")
    @cli.click.flag("--quiet", "-q", default=False, help="Disable JSON output")
    def apply(
        self,
        plan: planning.Plan = None,
        parallelism: str = "1",
        quiet: bool = False,
        fail_fast: bool = False,
    ) -> planning.ApplyResults:
        """
        Executes the plan for this plugin
        """
        parallelism = int(parallelism)
        plans = plan or self.plan(flattened=False)
        for plan in plans:
            results = plan.apply(parallelism=parallelism, git=self.siblings["git"])
            LOGGER.critical(
                f"Finished apply for subplan ({len(results.actions)}/{len(results.goals)} goals)"
            )
        # self.dispatch_apply_hooks(results)
        return results if not quiet else None
