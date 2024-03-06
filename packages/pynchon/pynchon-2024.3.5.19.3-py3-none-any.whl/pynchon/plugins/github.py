""" pynchon.plugins.github
"""

import webbrowser

import shimport
from fleks import cli, tagging

from pynchon import abcs, events, models  # noqa
from pynchon.util import lme, typing  # noqa

LOGGER = lme.get_logger(__name__)
config = shimport.lazy("pynchon.config")
option_api_token = cli.click.option(
    "--api-token", "-t", "token", default="", help="defaults to $GITHUB_API_TOKEN"
)


@tagging.tags(click_aliases=["gh"])
class GitHub(models.ToolPlugin):
    """Tools for working with GitHub"""

    class config_class(abcs.Config):
        config_key: typing.ClassVar[str] = "github"
        enterprise: bool = typing.Field(default=False)
        org_name: str = typing.Field(default=None)
        org_url: str = typing.Field(default=None)
        repo_url: str = typing.Field(default=None)
        actions: typing.List[abcs.Path] = typing.Field(default=[None])
        raw_url: str = typing.Field(default=None)

        @property
        def raw_url(self):
            return f"https://raw.githubusercontent.com/{self.org_name}/{config.git.repo_name}"

        @property
        def actions(self) -> typing.List[typing.Dict]:
            """ """
            wflows = abcs.Path(config.git.root) / ".github" / "workflows"
            if wflows.exists():
                return [
                    dict(
                        name=fname,
                        file=wflows / fname,
                        url=f"{self.repo_url}/actions/workflows/{fname}",
                    )
                    for fname in wflows.list()
                ]
            else:
                return []

        @property
        def repo_url(self):
            return config.git.repo_url

        @property
        def org_url(self):
            return f"https://github.com/{self.org_name}"

        @property
        def org_name(self):
            return config.git.github_org

    name = "github"
    cli_name = "github"
    cli_aliases = []

    @cli.click.option("--org", "-o")
    def open(self, org=None):
        """Opens org/repo github in a webbrowser

        :param org: Default value = None)

        """
        org_name = self["org_name"]
        url = self["org_url"]
        if not org:
            repo_name = self[:"git.repo_name":]
            url = f"{url}/{repo_name}"
        return webbrowser.open(url)

    @cli.options.org_name
    @option_api_token
    def clone_org(self, org_name: str = None, token: str = None):  # noqa
        """Clones an entire github-org

        :param org_name: str:  (Default value = None)
        :param token: str:  (Default value = None)
        :param org_name: str:  (Default value = None)
        :param token: str:  (Default value = None)

        """
        raise NotImplementedError()

    @cli.click.argument("repo")
    @option_api_token
    def clone(self, repo: str, token: str = None):  # noqa
        """Clones a single repo from this project's org

        :param repo: str:
        :param token: str:  (Default value = None)
        :param repo: str:
        :param token: str:  (Default value = None)

        """
        raise NotImplementedError()

    # @cli.click.argument('repo')
    @tagging.tags(click_aliases=["pr"])
    @option_api_token
    def pull_request(self, repo: str, token: str = None):  # noqa
        """Creates a pull-request from this branch

        :param repo: str:
        :param token: str:  (Default value = None)
        :param repo: str:
        :param token: str:  (Default value = None)

        """
        raise NotImplementedError()

    @tagging.tags(click_aliases=["codeowners"])
    # @option_api_token
    def code_owners(self, repo: str, token: str = None):  # noqa
        """Describes code-owners for changes or for working-dir

        :param repo: str:
        :param token: str:  (Default value = None)
        :param repo: str:
        :param token: str:  (Default value = None)

        """
        raise NotImplementedError()
