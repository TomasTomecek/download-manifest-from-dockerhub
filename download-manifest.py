#!/usr/bin/python3
import sys
import json

import requests


login_template = "https://auth.docker.io/token?service=registry.docker.io&scope=repository:{repository}:pull"
get_manifest_template = "https://registry.hub.docker.com/v2/{repository}/manifests/{tag}"
accept_types = "application/vnd.docker.distribution.manifest.list.v2+json,application/vnd.docker.distribution.manifestv2+json"


def pretty_print(d):
    print(json.dumps(d, indent=2))


def download_manifest_for_repo(repo, tag):
    """
    repo: string, repository (e.g. 'library/fedora')
    tag:  string, tag of the repository (e.g. 'latest')
    """
    response = requests.get(login_template.format(repository=repo), json=True)
    response_json = response.json()
    token = response_json["token"]
    response = requests.get(
        get_manifest_template.format(repository=repo, tag=tag),
        headers={"Authorization": "Bearer {}".format(token), "accept": accept_types},
        json=True
    )
    manifest = response.json()
    if not response.status_code == requests.codes.ok:
        pretty_print(dict(response.headers))
    return manifest


def main():
    repos = sys.argv[1:]
    if not repos:
        print("Usage: {} <[namespace/]repository[:tag]> [<[namespace/]repository[:tag]>...]".format(sys.argv[0]) +
              "\nExample: {} fedora:23".format(sys.argv[0]))
        return 1
    for repo_tag in repos:
        if ":" in repo_tag:
            repo, tag = repo_tag.split(":")
        else:
            repo, tag = repo_tag, "latest"
        if "/" not in repo:
            repo = "library/" + repo
        pretty_print(download_manifest_for_repo(repo, tag))
    return 0


if __name__ == "__main__":
    sys.exit(main())

