import json

from click.testing import CliRunner

from json_post.cli import cli

ITEMS = [{"id": i, "name": "Name {}".format(i)} for i in range(1, 11)]


def test_single_batch(httpx_mock):
    httpx_mock.add_response(method="POST")
    runner = CliRunner()
    with runner.isolated_filesystem():
        open("items.json", "w").write(json.dumps(ITEMS))
        result = runner.invoke(cli, ["items.json", "https://example.com/"])
        assert result.exit_code == 0

    request = httpx_mock.get_request()
    assert json.loads(request.read()) == ITEMS


def test_multiple_batches(httpx_mock):
    httpx_mock.add_response(method="POST")
    runner = CliRunner()
    with runner.isolated_filesystem():
        open("items.json", "w").write(json.dumps(ITEMS))
        result = runner.invoke(
            cli, ["items.json", "https://example.com/", "--batch-size", 4]
        )
        assert result.exit_code == 0

    requests = httpx_mock.get_requests()
    collected = []
    for request in requests:
        collected.extend(json.loads(request.read()))
    assert collected == ITEMS


def test_filter(httpx_mock):
    httpx_mock.add_response(method="POST")
    runner = CliRunner()
    with runner.isolated_filesystem():
        open("items.json", "w").write(json.dumps(ITEMS))
        result = runner.invoke(
            cli,
            ["items.json", "https://example.com/", "--filter", "item['id'] % 2 == 1"],
        )
        assert result.exit_code == 0

    request = httpx_mock.get_request()
    assert json.loads(request.read()) == [
        {"id": 1, "name": "Name 1"},
        {"id": 3, "name": "Name 3"},
        {"id": 5, "name": "Name 5"},
        {"id": 7, "name": "Name 7"},
        {"id": 9, "name": "Name 9"},
    ]
