# Github Release Maker

Simple program to make Github Releases from existing tags

### Installation

    pip install -r requirements

### Usage


    make_release [-h] [--artifacts ARTIFACTS [ARTIFACTS ...]]
                 [--update]
                 repository tag changelog token
    
    positional arguments:
      repository            The repository for which to make a release.
      tag                   Tag from which to make release (should exist)
      changelog             A changelog file according to
                            https://keepachangelog.com/en/1.0.0/. The entry
                            corresponding to `tag` will be used as the Github
                            Release
      token                 Github OAuth token
    
    optional arguments:
      -h, --help            show this help message and exit
      --artifacts ARTIFACTS [ARTIFACTS ...]
                            Filepaths or artifacts to upload.
      --update              Update (delete and recreate) an existing release.
