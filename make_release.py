import argparse
import sys
import textwrap

from github import Github

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
    args = parser.parse_args()
    
    g = Github(args.token)
    user = g.get_user()
 
    found = False
    for repo in user.get_repos():
        if repo.name == args.repository:
            found = True
            break
    if not found:
        print("Not found repository '{}'.".format(args.repository))
        sys.exit(1)

    print(repo)
    # TODO: make message
    message = args.changelog
    print("Creating release: {}.".format(args.tag))
    print(textwrap.indent(message, "    "))
    print()
    try:
        release = repo.create_git_release(args.tag, args.tag, message)
    except Exception as e:
        print(e)
        print("Failed to create release, does the tag exist?")
        sys.exit(1)

    if artifacts is not None:
        for artifact in args.artifacts:
            print("Adding {}.".format(artifact))
            release.upload_asset(asset)

if __name__ == "__main__":
    main()
