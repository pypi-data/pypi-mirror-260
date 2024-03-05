#!/usr/bin/env python3
import argparse
import regex as re
import git
import pathlib
from glob import glob

script_path = pathlib.Path(__file__).parent.absolute()

__version__ = "0.0.1"


def get_git_root(path: str) -> str:
    git_repo = git.Repo(path, search_parent_directories=True)
    git_root = git_repo.git.rev_parse("--show-toplevel")
    return git_root


def args_parser_init() -> argparse.Namespace:
    """Get user inputs"""
    parser = argparse.ArgumentParser(
        description="""A tool for updating task versions in imports""",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-w",
        "--input-wdl",
        type=str,
        required=True,
        help="The path to updated .wdl file",
    )
    parser.add_argument(
        "-r",
        "--repository",
        type=str,
        required=False,
        default=get_git_root(script_path),
        help="A path to catalog containing .git file",
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s {}".format(__version__)
    )

    args = parser.parse_args()
    return args


def get_wdl_content(input_wdl: str) -> str:
    with open(input_wdl, "r") as wdl_file:
        return wdl_file.read()


def get_task_version(wdl_content: str) -> str:
    pattern = r'(?<=(?:String\s)(?:task|module|pipeline)(?:_version\s=\s))"([^"]*)"'
    result = re.findall(pattern, wdl_content)[0]

    return result


def get_task_name(wdl_content: str) -> str:
    pattern = r'(?<=(?:String\s)(?:task|module|pipeline)(?:_name\s=\s))"([^"]*)"'
    result = re.findall(pattern, wdl_content)[0]
    result = result.replace("_", "-")

    return result


def get_git_repository(repository_path: str):
    return git.Repo(repository_path)


def fetch_all_remotes(git_repository: git.Repo):
    for remote in git_repository.remotes:
        remote.fetch()
        print(f"Fetched: {remote}")


def get_and_sort_tags(git_repository: git.Repo) -> list:
    referenced_ = git_repository.tags
    return sorted(referenced_, key=lambda t: t.commit.committed_datetime)


def check_if_tag_exist(referenced_tags: list, tag: str) -> bool:
    str_tags = [str(t) for t in referenced_tags]

    return tag in str_tags


def replace_if_imports_task(tag: str, filename: str, task_name: str) -> None:
    with open(filename, "r+") as wdl_file:
        workflow_content = wdl_file.read()
        pattern = rf"(?<=import\s.*\".*/){task_name}@\w+\.\w+\.\w+(?<=/.*)"
        result = re.findall(pattern, workflow_content)
        if result and tag != result[0]:
            print(f"Changing the import from {result[0]} to {tag} in {filename}")
            workflow_content = workflow_content.replace(result[0], tag, 1)
            wdl_file.seek(0)
            wdl_file.write(workflow_content)


def main():
    args = args_parser_init()
    wdl_content = get_wdl_content(args.input_wdl)

    task_ver = get_task_version(wdl_content)
    task_name = get_task_name(wdl_content)
    if not task_ver or not task_name:
        raise NameError(
            "Task name or task version are not properly implemented in .wdl file"
        )

    git_repository = get_git_repository(args.repository)
    print(f"Git repository: [{git_repository}]")
    fetch_all_remotes(git_repository)

    referenced_tags = get_and_sort_tags(git_repository)
    tag = f"{task_name}@{task_ver}"

    if check_if_tag_exist(referenced_tags, tag):
        print(f"{tag} exists in tags. Comparing with imports in workflows...")
        wdls_dirs = f"{args.repository}/src/main/wdl"
        modules = f"{wdls_dirs}/modules"
        pipelines = f"{wdls_dirs}/pipelines"
        importable_dirs = [modules, pipelines]

        for dir in importable_dirs:
            for filename in glob(f"{dir}/**/*.wdl", recursive=True):
                replace_if_imports_task(tag, filename, task_name)

    else:
        print("No existing tag found. Exiting...")


if __name__ == "__main__":
    main()
