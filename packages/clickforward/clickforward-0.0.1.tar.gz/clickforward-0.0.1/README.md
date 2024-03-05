# clickforward

Forward all click arguments without any parsing and any options from the first
non-option positional argument.

See https://github.com/pallets/click/pull/2686

# Usage

This change introduces a new `clickforward.FORWARD` argument type, which
stops the parser from further parsing arguments. Is it now possible to
forward arguments without any parsing.

Set the `argument` with `nargs=-1` and `type=clickforward.FORWARD` to
perfectly capture all arguments.

Example implementation of docker run` command:

```
import clickforward
import click


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


docker()
```

Allows for forwarding `sh --help -u -v` to the docker container.

```
$ python ./docker.py -v run -u kamil alpine sh --help -u -v
['docker', 'run', '-ukamil', 'alpine', 'sh', '--help', '-u', '-v']
```

# How it works

The act of importing the module __replaces__ the `click.parser.OptionParser`
parsing function of arguments with custom logic.

I have only tested with click==8.1.7.

# Epilogue

Written by Kamil Cukrowski

