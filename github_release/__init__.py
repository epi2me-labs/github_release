#!/usr/bin/env python3

import argparse
import re
import sys
import textwrap

from github import Github

__version__ = "0.0.4"

def changelog_parser(changelog):
    releases = dict()
    version = None
    buf = list()
    with open(changelog, 'r') as log:
        for line in log.readlines():
            m = re.match('## \[(.*)\]', line)
            if m:
                if version is not None:
                    releases[version] = ''.join(buf)
                    buf = list()
                version = m.group(1)
            elif version is not None:
                buf.append(line)
        if version is not None:
            releases[version] = ''.join(buf)
    return releases


def main():
    parser = argparse.ArgumentParser('Make a github release')
    parser.add_argument(
        'repository', help='The repository for which to make a release.')
    parser.add_argument(
        'tag', help='Tag from which to make release (should exist)')
    parser.add_argument(
        'changelog', help='A changelog file according to '
            'https://keepachangelog.com/en/1.0.0/. The entry '
            'corresponding to `tag` will be used as the Github Release')
    parser.add_argument(
        'token', help='Github OAuth token')
    parser.add_argument(
        '--artifacts', nargs='+', help='Filepaths or artifacts to upload.')
    parser.add_argument(
        '--update', action='store_true',
        help='Update (delete and recreate) an existing release.')
    args = parser.parse_args()
    
    g = Github(args.token)
    user = g.get_user()

    changelogs = changelog_parser(args.changelog)
    try:
        message = changelogs[args.tag]
    except KeyError:
        print("No entry for '{}' in changelog file.".format(args.tag))
        sys.exit(1)

    found = False
    for repo in user.get_repos():
        if repo.name == args.repository:
            found = True
            break
    if not found:
        print("Not found repository '{}'.".format(args.repository))
        sys.exit(1)

    print("Creating release: {}.".format(args.tag))
    print(textwrap.indent(message, "    "))
    print()
    try:
        if not args.update:
            release = repo.create_git_release(args.tag, args.tag, message)
            print("Created release.")
        else:
            release = repo.get_release(args.tag)
            release.delete_release()
            release = repo.create_git_release(args.tag, args.tag, message)
            print("Deleted and recreated release.")
    except Exception as e:
        print(e)
        print("Failed to create release:")
        print(" * does the tag exist?\n * does the user have access?")
        sys.exit(1)
    print()

    if args.artifacts is not None:
        print("Uploading artifacts")
        for artifact in args.artifacts:
            print(" Adding {}.".format(artifact))
            release.upload_asset(artifact)
    else:
        print("No artifacts to upload.")


if __name__ == "__main__":
    main()
