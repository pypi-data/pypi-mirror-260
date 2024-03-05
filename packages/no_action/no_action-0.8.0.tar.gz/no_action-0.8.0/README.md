# no_action

An incremental automation library to eliminate toil in processes.

## Description

Ideologically based on Dan Slimmon's [Do-nothing scripting][dns] article from 2019. `no_action`
provides a `Step` class that can be sub-classed and customized as well as a `Prodecure` class that
wraps a series of ordered steps.

First, one writes a series of Steps with the manual details in their docstring and the procedure
prints the docstrings, a glorified checklist. Over time though, with each Step encapsulated in
a discrete class, Steps of a procedure can be automated by writing code that actually does what is
described in the docstring (override the `Step.execute()` method). Soon, your procedures are fully
automated and can be hooked into an Internal Developer Platform (IDP), a runner, or other automation
orchestration system.

[dns]: https://blog.danslimmon.com/2019/07/15/do-nothing-scripting-the-key-to-gradual-automation/#

## Installation

This library can be found on PyPI. Run the following command to install the library into your
project.

`python3 -m pip install no-action`

<!--
## Usage

Use examples liberally, and show the expected output if you can. It's helpful to have inline the
smallest example of usage that you can demonstrate, while providing links to more sophisticated
examples if they are too long to reasonably include in the README.

## Support

Tell people where they can go to for help. It can be any combination of an issue tracker, a chat
room, an email address, etc.
-->

## License

This project is licensed under the GNU GPL 3. See;

- [LICENSE](https://gitlab.com/Skoretz/no_action/-/blob/main/LICENSE) for the preamble.
- [COPYING](https://gitlab.com/Skoretz/no_action/-/blob/main/COPYING) for the full text.
