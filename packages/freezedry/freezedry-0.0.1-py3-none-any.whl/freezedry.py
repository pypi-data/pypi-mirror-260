import os
import re
import zipfile
from typing import List, Optional, Union
from gitignore_parser import parse_gitignore


def match_git(path: str) -> bool:
    """simple method for determining if a path is a git-related file or directory"""
    return ".git" in path


def match_extra(path: str, extra_ignore: List[str]):
    """simple method for checking if the strings in extra_ignore are contained in path"""
    if not type(extra_ignore) == list:
        raise ValueError(
            f"extra_ignore should be a list of strings, but it is a {type(extra_ignore)}"
        )
    if not all([isinstance(pattern, str) for pattern in extra_ignore]):
        types = list(set([type(pattern).__name__ for pattern in extra_ignore]))
        types_formatted = ", ".join(types)
        raise ValueError(
            f"extra_ignore should be a list of strings, but it contains the following types: {types_formatted}"
        )
    return any([pattern in path for pattern in extra_ignore])


def match_regexp(path: str, regexp_ignore: List[str]):
    """simple method for checking if the regular expressions in regexp_ignore are matched in path"""
    if not type(regexp_ignore) == list:
        raise ValueError(
            f"extra_ignore should be a list of strings, but it is a {type(regexp_ignore)}"
        )
    if not all([isinstance(pattern, str) for pattern in regexp_ignore]):
        types = list(set([type(pattern).__name__ for pattern in regexp_ignore]))
        types_formatted = ", ".join(types)
        raise ValueError(
            f"regexp_ignore should be a list of strings, but it contains the following types: {types_formatted}"
        )
    return any([re.search(pattern, path) for pattern in regexp_ignore])


def check_ignore(
    path: str,
    ignore_git: bool = False,
    gitparser: Optional[object] = None,
    extra_ignore: Optional[List[str]] = None,
    regexp_ignore: Optional[List[str]] = None,
) -> bool:
    if ignore_git:
        if match_git(path):
            return True
    if gitparser is not None:
        if gitparser(path):
            return True
    if extra_ignore is not None:
        if match_extra(path, extra_ignore):
            return True
    if regexp_ignore is not None:
        if match_regexp(path, regexp_ignore):
            return True
    return False


def freezedry(
    directory_path,
    output_path: Optional[str] = None,
    ignore_git: bool = False,
    use_gitignore: bool = False,
    gitignore_path: Optional[Union[str, bytes, os.PathLike]] = None,
    extra_ignore: Optional[List[str]] = None,
    regexp_ignore: Optional[List[str]] = None,
    ignore_by_directory: bool = True,
    **zipfile_kwargs,
):
    """
    Create a zip file of the contents of a directory, with some filtering of files.

    Creates a zip file at <output_path> of the entire directory located at <directory_path>.
    Before making the zip file, will filter the files in <directory_path> based on these rules:

    1. If ignore_git=True, will ignore any files that have the partial string ".git" in the path.
    This is generally used to avoid making a copy of the entire git history.
    2. If use_gitignore, will ignore any files that would be ignored by github as defined in the
    provided .gitignore file (if none provided, will look for one in <directory_path>).
    3. If extra_ignore is provided, will ignore any files that contain the strings inside
    extra_ignore (e.g. if extra_ignore=['hello', 'world'], then 'hello_everyone' would be ignored)
    4. If regexp_ignore is provided, will ignore any files whose path's are matched by the regular
    expressions in regexp_ignore.

    If output path is not provided, will use: <directory_path>/compressed_directory.zip
    If use_gitignore=True and gitignore_path is not provided, will use <directory_path>/.gitignore
    If ignore_by_directory=True, then will ignore any files or directories that are children of a
    directory that meets ignore criterion (otherwise will search in that directory for any files).

    Any extra kwargs will be passed to the zipfile constructor method.
    """
    assert "r" != zipfile_kwargs.get("mode")  # cannot be in read mode for writing a new zipfile
    assert os.path.isdir(directory_path), f"{directory_path} is not a directory"

    if output_path is None:
        output_path = os.path.join(directory_path, "compressed_directory.zip")

    if use_gitignore:
        if gitignore_path is None:
            gitignore_path = os.path.join(directory_path, ".gitignore")
        assert os.path.exists(gitignore_path), f".gitignore file not found at {gitignore_path}"
        gitparser = parse_gitignore(gitignore_path)
    else:
        gitparser = None

    check_arguments = dict(
        ignore_git=ignore_git,
        gitparser=gitparser,
        extra_ignore=extra_ignore,
        regexp_ignore=regexp_ignore,
    )

    # Prepare list for copying files
    files_to_copy = []
    archive_names = []
    for dirpath, dirnames, files in os.walk(directory_path):
        if check_ignore(dirpath, **check_arguments):
            if ignore_by_directory:
                # clear any files from within this path using in-place method
                # to ignore any children files of an ignored directory
                dirnames[:] = []
        else:
            # Filter files based on specified rules
            keep_files = [f for f in files if not check_ignore(f, **check_arguments)]

            # Make full path
            full_files = [os.path.join(dirpath, f) for f in keep_files]
            for file in full_files:
                # Add file to the copy list
                files_to_copy.append(file)
                archive_names.append(os.path.relpath(file, directory_path))

    # create zip file
    zipfile_arguments = dict(mode="w", compression=zipfile.ZIP_DEFLATED).update(zipfile_kwargs)
    with zipfile.ZipFile(output_path, **zipfile_arguments) as zipf:
        # go through directory and write any files
        for file, name in zip(files_to_copy, archive_names):
            zipf.write(file, arcname=name)
