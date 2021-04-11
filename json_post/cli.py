import click
import httpx
import json
import random


@click.command()
@click.version_option()
@click.argument("json_file", type=click.File("r"))
@click.argument("url")
@click.option(
    "-h",
    "--header",
    "headers",
    type=(str, str),
    multiple=True,
    help="Extra HTTP headers to send, e.g. for Authorization",
)
@click.option(
    "--log",
    type=click.File("w"),
    help="Log response bodies as newline-JSON to this file",
)
@click.option(
    "--batch-size",
    type=int,
    help="Break it into batches of this size",
)
@click.option(
    "--stop-after",
    type=int,
    help="Stop running after this many items",
)
@click.option(
    "--reverse",
    is_flag=True,
    help="Import in reverse order",
)
@click.option(
    "--shuffle",
    is_flag=True,
    help="Import in random order",
)
@click.option(
    "--http-read-timeout",
    help="Timeout (in seconds) for network read operations",
    type=int,
)
@click.option(
    "--filter",
    "filter",
    help="Python expression accepting 'item' that returns True or False for if it should be included"
)
def cli(
    json_file,
    url,
    headers,
    log,
    batch_size,
    stop_after,
    reverse,
    shuffle,
    http_read_timeout,
    filter,
):
    "Tool for posting JSON to an API, broken into pages"
    items = json.load(json_file)
    if reverse:
        items = list(reversed(items))
    if shuffle:
        random.shuffle(items)
    if stop_after:
        items = items[:stop_after]
    if filter:
        if "\n" not in filter and not filter.strip().startswith("return "):
            filter = "return {}".format(filter)
        # Compile the code into a function body called fn(value)
        new_code = ["def fn(value):"]
        for line in filter.split("\n"):
            new_code.append("    {}".format(line))
        code_o = compile("\n".join(new_code), "<string>", "exec")
        locals = {}
        globals = {}
        exec(code_o, globals, locals)
        fn = locals["fn"]
        items = [item for item in items if fn(item)]
    if batch_size:
        batches = chunks(items, batch_size)
    else:
        batches = [items]
    if http_read_timeout:
        client = httpx.Client(timeout=httpx.Timeout(5, read=http_read_timeout))
    else:
        client = httpx
    with click.progressbar(length=len(items)) as bar:
        for batch in batches:
            response = client.post(url, json=batch, headers=dict(headers))
            if response.status_code != 200:
                click.echo(response.content, err=True)
            if log:
                log.write(json.dumps(response.json()) + "\n")
            bar.update(len(batch))


def chunks(items, chunk_size):
    # looping till length l
    for i in range(0, len(items), chunk_size):
        yield items[i : i + chunk_size]
