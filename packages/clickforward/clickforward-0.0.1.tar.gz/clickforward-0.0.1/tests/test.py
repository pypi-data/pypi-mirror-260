#!/usr/bin/env python3
import shlex
from typing import Any, List

import click
from click.testing import CliRunner

import clickforward


def invoke(*args, **kwargs):
    return CliRunner(mix_stderr=True).invoke(*args, **kwargs)


def trun(cli, cmd: str, output: Any = None, fail: int = 0):
    r = invoke(cli, shlex.split(cmd))
    info = f"{cli} {input} {r.output}"
    if fail:
        assert r.exit_code != 0, info
    else:
        assert r.exit_code == 0, info
    if output is not None:
        assert r.output == f"{output}\n", info


def test_docker_run():
    @click.group()
    @click.option("-v", "--verbose", is_flag=True)
    def docker(verbose):
        pass

    @docker.command()
    @click.option("-v", "--verbose", is_flag=True)
    @click.option("-u", "--user")
    @click.argument("image")
    @click.argument("command", nargs=-1, type=clickforward.FORWARD)
    def run(verbose, user, image, command):
        cmdline: List[str] = (
            ["docker"]
            + ["run"]
            + ([f"-u{user}"] if user else [])
            + [image]
            + list(command)
        )
        click.echo(" ".join(shlex.quote(x) for x in cmdline))

    trun(docker, "run image sh -h", "docker run image sh -h")
    trun(docker, "run -u user image sh -h", "docker run -uuser image sh -h")
    trun(
        docker,
        "run -u user image sh -h --help -u blabla --anything -u",
        "docker run -uuser image sh -h --help -u blabla --anything -u",
    )
