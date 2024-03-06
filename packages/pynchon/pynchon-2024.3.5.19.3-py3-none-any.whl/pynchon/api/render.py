""" pynchon.api.render

    Basically this is core jinja stuff.
    Looking for CLI entrypoints?  See pynchon.util.text.render
    Looking for the JinjaPlugin?  See pynchon.plugins.jinja
"""

import os
import functools

from jinja2 import Environment  # Template,; UndefinedError,
from jinja2 import FileSystemLoader, StrictUndefined

import pynchon
from pynchon import abcs, constants, events
from pynchon.util.os import invoke

import jinja2  # noqa

from pynchon.util import lme, typing  # noqa

LOGGER = lme.get_logger(__name__)


def is_templated(txt: str = "") -> bool:
    """ """
    return txt is not None and ("{{" in txt and "}}" in txt)


def dictionary(input, context):
    """
    :param context:
    """
    from pynchon.abcs.visitor import JinjaDict

    return JinjaDict(input).render(context)


@functools.lru_cache(maxsize=None)
def get_jinja_filters():
    return dict(
        Path=abcs.Path,
    )


@functools.lru_cache(maxsize=None)
def get_jinja_globals():
    """ """
    events.lifecycle.send(__name__, msg="finalizing jinja globals")

    def invoke_helper(*args, **kwargs) -> typing.StringMaybe:
        """A jinja filter/extension"""
        out = invoke(*args, **kwargs)
        assert out.succeeded
        return out.stdout

    def markdown_toc(fname: str, level=None):
        """ """
        assert fname
        fname = abcs.Path(fname)
        assert fname.exists()
        script = abcs.Path(pynchon.__file__).parents[0] / "scripts" / "gh-md-toc.sh"
        result = invoke(
            f"cat {fname} | bash {script} -", command_logger=LOGGER.critical
        )
        assert result.succeeded
        return result.stdout

    return dict(
        sh=invoke_helper,
        bash=invoke_helper,
        invoke=invoke_helper,
        map=map,
        markdown_toc=markdown_toc,
        eval=eval,
        env=os.getenv,
    )


def get_jinja_includes(*includes):
    """ """
    includes = list(includes)
    includes += list(constants.PYNCHON_CORE_INCLUDES_DIRS)

    return [abcs.Path(t) for t in includes]


@functools.lru_cache(maxsize=None)
def get_jinja_env(*includes, quiet: bool = False):
    """ """
    events.lifecycle.send(__name__, msg="finalizing jinja-Env")
    includes = get_jinja_includes(*includes)
    for template_dir in includes:
        if not template_dir.exists:
            err = f"template directory @ `{template_dir}` does not exist"
            raise ValueError(err)
    # includes and (not quiet) and LOGGER.warning(f"Includes: {includes}")
    env = Environment(
        loader=FileSystemLoader([str(t) for t in includes]),
        undefined=StrictUndefined,
    )
    env.filters.update(**get_jinja_filters())
    env.pynchon_includes = includes

    env.globals.update(**get_jinja_globals())

    known_templates = list(map(abcs.Path, set(env.loader.list_templates())))

    if known_templates:
        from pynchon.util import text as util_text

        msg = "Known template search paths (includes folders only): "
        tmp = list({p.parents[0] for p in known_templates})
        LOGGER.info(msg + util_text.to_json(tmp))
    return env


def get_template_from_string(
    content,
    env=None,
):
    """
    :param env=None:
    :param content:
    """
    env = env or get_jinja_env()
    return env.from_string(content)


def get_template_from_file(
    file: str = None,
    **kwargs,
):
    """
    :param file: str = None:
    :param **kwargs:
    """
    with open(file) as fhandle:
        content = fhandle.read()
    return get_template_from_string(content, **kwargs)


def get_template(
    template_name: typing.Union[str, abcs.Path] = None,
    env=None,
    from_string: str = None,
):
    """ """
    env = env or get_jinja_env()
    if isinstance(template_name, (abcs.Path,)):
        template_name = str(template_name)
    try:
        if from_string:
            template = env.from_string(from_string)
        else:
            LOGGER.info(f"Looking up {template_name}")
            template = env.get_template(template_name)
    except (jinja2.exceptions.TemplateNotFound,) as exc:
        LOGGER.critical(f"Template exception: {exc}")
        LOGGER.critical(f"Jinja-includes: {env.pynchon_includes}")
        err = getattr(exc, "templates", exc.message)
        LOGGER.critical(f"Problem template: {err}")
        raise
    template.render = functools.partial(template.render, __template__=template_name)
    return template


def clean_whitespace(txt: str):
    # return txt
    return "\n".join([x for x in txt.split("\n") if x.strip()])
