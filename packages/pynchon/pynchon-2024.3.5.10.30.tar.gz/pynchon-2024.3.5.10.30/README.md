<table>
  <tr>
    <td colspan=2><strong>
    pynchon
      </strong>&nbsp;&nbsp;&nbsp;&nbsp;
      <small><small>
      </small></small>
    </td>
  </tr>
  <tr>
    <td width=15%><img src=img/icon.png style="width:150px"></td>
    <td>
      Placeholder
      <br/><br/>
      <a href=https://pypi.python.org/pypi/pynchon/><img src="https://img.shields.io/pypi/l/pynchon.svg"></a>
      <a href=https://pypi.python.org/pypi/pynchon/><img src="https://badge.fury.io/py/pynchon.svg"></a>
      <a href="https://github.com/elo-enterprises/pynchon/actions/workflows/python-test.yml"><img src="https://github.com/elo-enterprises/pynchon/actions/workflows/python-test.yml/badge.svg"></a>
    </td>
  </tr>
</table>

---------------------------------------------------------------------------------

  * [Overview](#overview)
  * [Motivation &amp; Design](#motivation--design)
  * [Quick Start](#quick-start)
* [Pynchon as a Suite of Utilities](#pynchon-as-a-suite-of-utilities)
  * [pynchon.util](#pynchonutil)
    * [pynchon.util.os](#pynchonutilos)
    * [pynchon.util.files](#pynchonutilfiles)
    * [pynchon.util.loadf](#pynchonutilloadf)
    * [pynchon.util.jinja](#pynchonutiljinja)
    * [pynchon.util.splitvt](#pynchonutilsplitvt)
    * [pynchon.util.ansible](#pynchonutilansible)
    * [pynchon.util.json](#pynchonutiljson)
    * [pynchon.util.pydash](#pynchonutilpydash)
    * [pynchon.util.shfmt](#pynchonutilshfmt)
    * [pynchon.util.grip](#pynchonutilgrip)
* [Pynchon as a Framework](#pynchon-as-a-framework)
  * [Plugins](#plugins)
    * [Plugin Priority](#plugin-priority)
    * [Plugin Config](#plugin-config)
      * [User Config](#user-config)
      * [Config Defaults](#config-defaults)
      * [Lazy Config](#lazy-config)
      * [Dynamic Config](#dynamic-config)
      * [Syntactic Sugar](#syntactic-sugar)
    * [Plugin CLIs](#plugin-clis)
      * [CLI Aliases](#cli-aliases)
      * [Hidden Commands](#hidden-commands)
    * [Plugin Types](#plugin-types)
      * [Core-Plugins](#core-plugins)
      * [Provider-Plugins](#provider-plugins)
      * [Planner-Plugins](#planner-plugins)
      * [Manager-Plugins](#manager-plugins)
      * [Tool-Plugins](#tool-plugins)
      * [Nested-Plugins](#nested-plugins)
      * [Namespaces](#namespaces)
  * [Rendering Engine](#rendering-engine)
  * [Projects &amp; Subprojects](#projects--subprojects)
  * [Data vs Display](#data-vs-display)
  * [Hooks &amp; Events](#hooks--events)
  * [Pynchon as a Library](#pynchon-as-a-library)
    * [Planners](#planners)
    * [Solvers](#solvers)
    * [Tagging &amp; Typing](#tagging--typing)
    * [Orchestration](#orchestration)
    * [CLI Framework](#cli-framework)
    * [Application Framework](#application-framework)
    * [OOP Framework](#oop-framework)
    * [Event Framework](#event-framework)
  * [Example Usage](#example-usage)
  * [Packaging &amp; Releases](#packaging--releases)
  * [Dependencies](#dependencies)
  * [Related Work](#related-work)
  * [Workflows](#workflows)
    * [Workflow: Bug Reports or Feature Requests](#workflow-bug-reports-or-feature-requests)
    * [Workflow: Finding a Release](#workflow-finding-a-release)
    * [Workflow: Installation for Library Developers](#workflow-installation-for-library-developers)
  * [Implementation Notes](#implementation-notes)
    * [Python Plugins](#python-plugins)
  * [Known Issues](#known-issues)


---------------------------------------------------------------------------------

<table>
  <tr>
    <td colspan=2><strong>
    pynchon
      </strong>&nbsp;&nbsp;&nbsp;&nbsp;
      <small><small>
      </small></small>
    </td>
  </tr>
  <tr>
    <td width=15%><img src=img/icon.png style="width:150px"></td>
    <td>
    pynchon
    </td>
  </tr>
</table>

* [Pynchon as a Suite of Utilities](#pynchon-as-a-suite-of-utilities)
  * [pynchon.util](#pynchonutil)
    * [pynchon.util.os](#pynchonutilos)
    * [pynchon.util.files](#pynchonutilfiles)
    * [pynchon.util.loadf](#pynchonutilloadf)
    * [pynchon.util.jinja](#pynchonutiljinja)
    * [pynchon.util.splitvt](#pynchonutilsplitvt)
    * [pynchon.util.ansible](#pynchonutilansible)
    * [pynchon.util.json](#pynchonutiljson)
    * [pynchon.util.pydash](#pynchonutilpydash)
    * [pynchon.util.shfmt](#pynchonutilshfmt)
    * [pynchon.util.grip](#pynchonutilgrip)
* [Pynchon as a Framework](#pynchon-as-a-framework)
  * [Plugins](#plugins)
    * [Plugin Priority](#plugin-priority)
    * [Plugin Config](#plugin-config)
      * [User Config](#user-config)
      * [Config Defaults](#config-defaults)
      * [Lazy Config](#lazy-config)
      * [Dynamic Config](#dynamic-config)
      * [Syntactic Sugar](#syntactic-sugar)
    * [Plugin CLIs](#plugin-clis)
      * [CLI Aliases](#cli-aliases)
      * [Hidden Commands](#hidden-commands)
    * [Plugin Types](#plugin-types)
      * [Core-Plugins](#core-plugins)
      * [Provider-Plugins](#provider-plugins)
      * [Planner-Plugins](#planner-plugins)
      * [Manager-Plugins](#manager-plugins)
      * [Tool-Plugins](#tool-plugins)
      * [Nested-Plugins](#nested-plugins)
      * [Namespaces](#namespaces)
  * [Rendering Engine](#rendering-engine)
  * [Projects &amp; Subprojects](#projects--subprojects)
  * [Data vs Display](#data-vs-display)
  * [Hooks &amp; Events](#hooks--events)
  * [Pynchon as a Library](#pynchon-as-a-library)
    * [Parsers](#parsers)
    * [Planners](#planners)
    * [Solvers](#solvers)
    * [Tagging &amp; Typing](#tagging--typing)
    * [Orchestration](#orchestration)
    * [CLI Framework](#cli-framework)
    * [Application Framework](#application-framework)
    * [OOP Framework](#oop-framework)
    * [Event Framework](#event-framework)
  * [Example Usage](#example-usage)
  * [Packaging &amp; Releases](#packaging--releases)
  * [Dependencies](#dependencies)
  * [Related Work](#related-work)
  * [Workflows](#workflows)
    * [Workflow: Bug Reports or Feature Requests](#workflow-bug-reports-or-feature-requests)
    * [Workflow: Finding a Release](#workflow-finding-a-release)
    * [Workflow: Installation for Library Developers](#workflow-installation-for-library-developers)
  * [Implementation Notes](#implementation-notes)
  * [Known Issues](#known-issues)


---------------------------------------------------------------------------------

## Overview

Pynchon is a library, tool, and extensible framework for project management.  It's useful in general, but also specializes in autogenerating documentation for python projects.

## Motivation & Design

This project exists because frameworks like [sphinx](#), [pydoc](#), and [mkdocs](#), and [pandoc](#) do a lot, but require quite a bit of opinionated /fragile setup, and in the end it's often pretty difficult to do basic stuff.  

If you get basic stuff working and want slight customization, then you're quickly deep into the guts of one of these systems and running into a need for trying different versions or building containers with customized tool-chains.  

Stack-overflow is full of examples of this sort of thing, but here's a quick list of typical complaints:

* You want table-of-contents generation for markdown, then try to do things the "right way" with sophisticated tools, but eventually [hit a wall](https://stackoverflow.com/questions/73965242/pandoc-how-to-generate-github-markdown-table-of-content-toc). This is the third approach you've looked at too.  You wanted to be cool.. but to get work done you'll retreat to using a [bash script](https://github.com/ekalinin/github-markdown-toc) that just works.
* You build out a docker-container for pandoc/tex trying to put together a math-markdown to pdf pipeline, then find that the pandoc filter you needed all this for just fails silently??  You read about panflute for 3 days and finally just have to skip the pretty equations and dump tex gibberish in a doc string.
* You have lots of choices, [but module docs are still hard](https://stackoverflow.com/questions/36237477/python-docstrings-to-github-readme-md)
* You can import your code, [but your docs framework can't](https://stackoverflow.com/questions/17368747/will-sphinx-work-with-code-that-doesnt-import-well).
* [grip](https://pypi.org/project/grip/) is a lifesaver if you're serious about docs on github, but what a pity that you need another tab with `file:///...` to view coverage HTML.
* You have some almost-working docs pipeline, but you still need orchestration.  Orchestration [is subtle](https://github.com/sphinx-doc/sphinx/issues/8437) and [orchestration boilerplate](https://gist.github.com/kristopherjohnson/7466917) begins to clutter your project.  Even worse, that hard-earned boilerplate tends to be very difficult to reuse across projects.


For obvious reasons, popular docs-frameworks also stop short of managing things *besides* docs; but code-gen or code-annotation is a pretty similar task.  After you start thinking about stuff like this, you notice that API-docs generation probably can't succeed anyway as long as you have syntax errors, so why not lint files before or during scan, and make sure the spec for lint/docs-gen are using the same source-tree config in a way that's [DRY](#)?  Annotations along the lines of type-checks or [contract verification](https://github.com/life4/deal) in many projects are also done gradually before they are enforced in builds or runtimes anyway. Since unenforced "informational" content from a CI server is usually just ignored, why not at least organize/publish this data alongside documentation?

But.. *pynchon is not a build tool, it's a project tool.*  The approach is spiritually related to things like [pandoc](#), [helm](#), [jinja](#), [tox](#), [cog](#), [make](#), [cruft](https://cruft.github.io/cruft/), [cookie-cutter](#), or [pyscaffold](#).  But pynchon is much likely to orchestrate *across* these things than try to replace them.

Management / generation tasks in source-repositories are usually on-going and iterative processes.  For this kind of work, pynchon's interface choices are heavily influenced by the design of [terraform](#): most things are using a plan/apply workflow, where all the context information is arrived at via optional "providers".  After that basic model is established, a plugin/config system then allows for easy expansion.

## Quick Start

Pynchon is on PyPI, so to get the latest:

```
pip install pynchon
```

Or, for developers:

```
git clone ..FIXME..
pip install -e .
```

---------------------------------------------------------------------------------

# Pynchon as a Suite of Utilities

The modules inside the pynchon library publish several stand-alone tools.

## pynchon.util
### pynchon.util.os
### pynchon.util.files
### pynchon.util.loadf
### pynchon.util.jinja
### pynchon.util.splitvt
### pynchon.util.ansible
### pynchon.util.json
### pynchon.util.pydash
### pynchon.util.shfmt
### pynchon.util.grip

---------------------------------------------------------------------------------

# Pynchon as a Framework

## Plugins
### Plugin Priority

### Plugin Config
#### User Config
#### Config Defaults
#### Lazy Config
#### Dynamic Config
#### Syntactic Sugar

### Plugin CLIs
#### CLI Aliases
#### Hidden Commands

### Plugin Types
#### Core-Plugins
#### Provider-Plugins
#### Planner-Plugins
#### Manager-Plugins
#### Tool-Plugins
#### Nested-Plugins
#### Namespaces
## Rendering Engine
## Projects & Subprojects
## Data vs Display
## Hooks & Events

---------------------------------------------------------------------------------

## Pynchon as a Library

### Planners

### Solvers

### Tagging & Typing

### Orchestration

System Command Invocation

### CLI Framework

### Application Framework

### OOP Framework

### Event Framework



---------------------------------------------------------------------------------

## Example Usage

```
```

---------------------------------------------------------------------------------

## Packaging & Releases

---------------------------------------------------------------------------------

## Dependencies

---------------------------------------------------------------------------------

## Related Work

---------------------------------------------------------------------------------

## Workflows

### Workflow: Bug Reports or Feature Requests

### Workflow: Finding a Release

### Workflow: Installation for Library Developers

---------------------------------------------------------------------------------

## Implementation Notes


### Python Plugins

For auto-discovery of things like "name of this package" or "entry-points for this package" `pynchon` assumes by default that it is working inside the source-tree for a modern python project.

If your project is using older packaging standards, or you're working on a group of files that's not a proper python project, you can usually work around this by passing information in directly instead of relying on auto-discovery.  Use the `pkg_name` top-level config key.


Pynchon relies heavily on [griffe](https://pypi.org/project/griffe/) for parsing and for [AST-walking](https://docs.python.org/3/library/ast.html).

For cyclomatic complexity, pynchon relies on the [mccabe library](https://github.com/PyCQA/mccabe).

---------------------------------------------------------------------------------

## Known Issues

* Use the [griffe-agent / plugin framework](#FIXME)?
* See [FIXME.md](docs/FIXME.md)
* See [TODO.md](docs/TODO.md)

---------------------------------------------------------------------------------

