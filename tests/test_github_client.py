import httpx
import pytest

from app.clients.github import GitHubClient


@pytest.mark.anyio
async def test_github_client_fetches_all_file_pages():
    requests = []

    def handler(request: httpx.Request):
        requests.append(request)
        page = request.url.params["page"]
        if page == "1":
            return httpx.Response(
                200,
                json=[{"filename": "one.py"}],
                headers={
                    "Link": '<https://api.github.com/repos/example/project/pulls/1/files?page=2>; rel="next"'
                },
            )
        return httpx.Response(200, json=[{"filename": "two.py"}])

    client = GitHubClient(transport=httpx.MockTransport(handler))

    files = await client.get_pull_request_files("example", "project", 1)

    assert [file["filename"] for file in files] == ["one.py", "two.py"]
    assert len(requests) == 2
    assert all(request.url.params["per_page"] == "100" for request in requests)
