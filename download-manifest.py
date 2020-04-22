#!/usr/bin/env python3
""" script to download manifests from Docker hub """
import sys
import json

import requests


LOGIN_URL = "https://auth.docker.io/token?service=registry.docker.io&scope=repository:{repository}:pull"
MANIFEST_URL = "https://registry.hub.docker.com/v2/{repository}/manifests/{tag}"
ACCEPT_TYPES = "application/vnd.docker.distribution.manifest.list.v2+json,application/vnd.docker.distribution.manifestv2+json"


def pretty_print(obj):
    """ print indented JSONified version of given object """
    print(json.dumps(obj, indent=2))


def download_manifest_for_repo(repo, tag):
    """
    repo: string, repository (e.g. 'library/fedora')
    tag:  string, tag of the repository (e.g. 'latest')
    """
    response = requests.get(LOGIN_URL.format(repository=repo), json=True)
    response_json = response.json()
    token = response_json["token"]
    response = requests.get(
        MANIFEST_URL.format(repository=repo, tag=tag),
        headers={"Authorization": "Bearer {}".format(token), "accept": ACCEPT_TYPES},
        json=True,
    )
    manifest = response.json()
    if not response.status_code == requests.codes.ok:
        pretty_print(dict(response.headers))
    return manifest


def main():
    """ entrypoint for command-line execution, returns exit code """
    repos = sys.argv[1:]
    if not repos:
        print(
            (
                "Usage: {self} <[namespace/]repository[:tag]> [...]\n"
                "Example: {self} fedora:23"
            ).format(self=sys.argv[0])
        )
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
