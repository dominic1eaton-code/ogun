#!/usr/bin/env python3
"""
pg_utility.py – A comprehensive GitLab management toolkit with CLI support.

Author: Dominic E. (@eatondo)

Commands
--------
  Groups
    list-groups                   List top-level groups (or subgroups of a parent)
    list-projects                 List all projects in a group (incl. subgroups)

  Branches
    list-branches                 List branches in a project
    create-branch                 Create a branch from a source ref
    delete-branch                 Delete a branch from a project
    protect-branch                Protect a branch in one project
    protect-branch-group          Protect a branch across every project in a group
    unprotect-branch              Unprotect a branch in one project
    unprotect-branch-group        Unprotect a branch across a group

  Merge Requests
    list-mrs                      List open merge requests
    create-mr                     Create a merge request
    merge-mr                      Accept / merge an MR
    close-mr                      Close (decline) an MR

  Tags & Releases
    list-tags                     List tags in a project
    create-tag                    Create a tag (with optional release notes)
    delete-tag                    Delete a tag
    create-release                Create a GitLab release on an existing tag

  Members & Permissions
    list-members                  List group or project members
    add-member                    Add a user to a group or project
    remove-member                 Remove a user from a group or project
    set-member-access             Change a member's access level

  CI/CD
    list-pipelines                List recent pipelines for a project
    trigger-pipeline              Trigger a new pipeline
    cancel-pipeline               Cancel a running pipeline
    list-pipeline-jobs            List jobs for a pipeline
    retry-pipeline                Retry a failed pipeline

  Repository
    list-files                    List files/dirs at a path in the repo
    get-file                      Print the content of a single file
    create-file                   Create a new file in the repository
    update-file                   Update an existing file in the repository
    delete-file                   Delete a file from the repository

  Issues
    list-issues                   List open issues for a project
    create-issue                  Create a new issue
    close-issue                   Close an issue

  Users
    get-user                      Look up a user by username

Examples
--------
  python pg_utility.py list-projects --group-id 132780099
  python pg_utility.py protect-branch-group --group-id 132780099 --branch develop
  python pg_utility.py create-mr --project-id 456 --source feature/x --target main \\
      --title "My MR" --description "Fixes #1"
  python pg_utility.py trigger-pipeline --project-id 456 --ref main
  python pg_utility.py add-member --group-id 132780099 --username jdoe --access developer
"""

import argparse
import sys
from pathlib import Path

import gitlab
from gitlab import const as glconst

# ---------------------------------------------------------------------------
# Access-level map (case-insensitive CLI strings → GitLab int values)
# ---------------------------------------------------------------------------
ACCESS_LEVELS: dict[str, int] = {
    "no_access":  glconst.AccessLevel.NO_ACCESS,
    "minimal":    glconst.AccessLevel.MINIMAL_ACCESS,
    "guest":      glconst.AccessLevel.GUEST,
    "reporter":   glconst.AccessLevel.REPORTER,
    "developer":  glconst.AccessLevel.DEVELOPER,
    "maintainer": glconst.AccessLevel.MAINTAINER,
    "owner":      glconst.AccessLevel.OWNER,
}


# ===========================================================================
# Authentication
# ===========================================================================

def authenticate_gitlab() -> gitlab.Gitlab:
    """Authenticate using ~/.python-gitlab.cfg (or env GITLAB_*) via python-gitlab."""
    gl = gitlab.Gitlab.from_config()
    gl.auth()
    return gl


# ===========================================================================
# Groups
# ===========================================================================

def cmd_list_groups(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    """List groups.  If --group-id is given, list direct subgroups of that group."""
    if args.group_id:
        group = gl.groups.get(args.group_id, lazy=True)
        groups = group.subgroups.list(get_all=True)
    else:
        groups = gl.groups.list(get_all=True, top_level_only=True)

    print(f"{'ID':<12} {'Full Path':<50} Name")
    print("-" * 80)
    for g in groups:
        print(f"{g.id:<12} {g.full_path:<50} {g.name}")


def cmd_list_projects(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    """List all active projects in a group (recursively through subgroups)."""
    def _recurse(group):
        projects = group.projects.list(get_all=True, archived=False)
        for p in projects:
            if p.marked_for_deletion_on is None:
                print(f"  {p.id:<10} {p.path_with_namespace}")
        for sg in group.subgroups.list(get_all=True):
            sg_obj = gl.groups.get(sg.id, lazy=True)
            _recurse(sg_obj)

    group = gl.groups.get(args.group_id, lazy=True)
    print(f"Projects in group {args.group_id}:\n")
    _recurse(group)


# ===========================================================================
# Branches
# ===========================================================================

def _get_project(gl: gitlab.Gitlab, project_id: int | str):
    return gl.projects.get(project_id)


def cmd_list_branches(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    branches = project.branches.list(get_all=True)
    print(f"{'Name':<40} {'Protected':<12} Last Commit")
    print("-" * 80)
    for b in branches:
        print(f"{b.name:<40} {str(b.protected):<12} {b.commit['short_id']} – {b.commit['title'][:40]}")


def cmd_create_branch(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    branch = project.branches.create({"branch": args.branch, "ref": args.ref})
    print(f"Created branch '{branch.name}' from '{args.ref}' in project {args.project_id}.")


def cmd_delete_branch(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    project.branches.delete(args.branch)
    print(f"Deleted branch '{args.branch}' from project {args.project_id}.")


def _protect_single(project, branch_name: str, merge_level: int, push_level: int) -> None:
    # Remove old protection if it exists
    try:
        project.protectedbranches.delete(branch_name)
    except gitlab.exceptions.GitlabDeleteError:
        pass
    project.protectedbranches.create({
        "name": branch_name,
        "merge_access_level": merge_level,
        "push_access_level": push_level,
        "allow_force_push": False,
    })
    print(f"  [protected] {project.path_with_namespace} → {branch_name}")


def cmd_protect_branch(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    merge_lvl = ACCESS_LEVELS.get(args.merge_access, glconst.AccessLevel.MAINTAINER)
    push_lvl  = ACCESS_LEVELS.get(args.push_access,  glconst.AccessLevel.MAINTAINER)
    project = _get_project(gl, args.project_id)
    _protect_single(project, args.branch, merge_lvl, push_lvl)


def cmd_protect_branch_group(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    merge_lvl = ACCESS_LEVELS.get(args.merge_access, glconst.AccessLevel.MAINTAINER)
    push_lvl  = ACCESS_LEVELS.get(args.push_access,  glconst.AccessLevel.MAINTAINER)
    group = gl.groups.get(args.group_id, lazy=True)
    projects = group.projects.list(get_all=True, archived=False)
    print(f"Protecting '{args.branch}' across {len(projects)} project(s) in group {args.group_id}...\n")
    for gp in projects:
        if gp.marked_for_deletion_on is not None:
            continue
        project = _get_project(gl, gp.id)
        _protect_single(project, args.branch, merge_lvl, push_lvl)


def cmd_unprotect_branch(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    project.protectedbranches.delete(args.branch)
    print(f"Unprotected '{args.branch}' in project {args.project_id}.")


def cmd_unprotect_branch_group(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    group = gl.groups.get(args.group_id, lazy=True)
    projects = group.projects.list(get_all=True, archived=False)
    print(f"Unprotecting '{args.branch}' across {len(projects)} project(s)...\n")
    for gp in projects:
        if gp.marked_for_deletion_on is not None:
            continue
        project = _get_project(gl, gp.id)
        try:
            project.protectedbranches.delete(args.branch)
            print(f"  [unprotected] {project.path_with_namespace}")
        except gitlab.exceptions.GitlabDeleteError:
            print(f"  [skipped]     {project.path_with_namespace} – not protected")


# ===========================================================================
# Merge Requests
# ===========================================================================

def cmd_list_mrs(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    state = args.state or "opened"
    mrs = project.mergerequests.list(state=state, get_all=True)
    print(f"{'IID':<8} {'State':<12} {'Author':<20} Title")
    print("-" * 80)
    for mr in mrs:
        print(f"!{mr.iid:<7} {mr.state:<12} {mr.author['username']:<20} {mr.title[:40]}")


def cmd_create_mr(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    payload = {
        "source_branch": args.source,
        "target_branch": args.target,
        "title": args.title,
    }
    if args.description:
        payload["description"] = args.description
    if args.assignee:
        user = gl.users.list(username=args.assignee)[0]
        payload["assignee_id"] = user.id
    mr = project.mergerequests.create(payload)
    print(f"Created MR !{mr.iid}: {mr.web_url}")


def cmd_merge_mr(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    mr = project.mergerequests.get(args.mr_iid)
    mr.merge()
    print(f"Merged MR !{args.mr_iid} in project {args.project_id}.")


def cmd_close_mr(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    mr = project.mergerequests.get(args.mr_iid)
    mr.state_event = "close"
    mr.save()
    print(f"Closed MR !{args.mr_iid} in project {args.project_id}.")


# ===========================================================================
# Tags & Releases
# ===========================================================================

def cmd_list_tags(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    tags = project.tags.list(get_all=True)
    print(f"{'Name':<30} {'Commit':<12} Message")
    print("-" * 80)
    for t in tags:
        msg = (t.message or "")[:40]
        print(f"{t.name:<30} {t.commit['short_id']:<12} {msg}")


def cmd_create_tag(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    payload: dict = {"tag_name": args.tag, "ref": args.ref}
    if args.message:
        payload["message"] = args.message
    if args.release_description:
        payload["release_description"] = args.release_description
    tag = project.tags.create(payload)
    print(f"Created tag '{tag.name}' at {tag.commit['short_id']}.")


def cmd_delete_tag(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    project.tags.delete(args.tag)
    print(f"Deleted tag '{args.tag}' from project {args.project_id}.")


def cmd_create_release(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    release = project.releases.create({
        "name": args.name or args.tag,
        "tag_name": args.tag,
        "description": args.description or "",
    })
    print(f"Created release '{release.name}' for tag '{args.tag}'.")


# ===========================================================================
# Members & Permissions
# ===========================================================================

def cmd_list_members(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    if args.group_id:
        obj = gl.groups.get(args.group_id)
        members = obj.members.list(get_all=True)
    else:
        obj = _get_project(gl, args.project_id)
        members = obj.members.list(get_all=True)

    access_map = {v: k for k, v in ACCESS_LEVELS.items()}
    print(f"{'ID':<10} {'Username':<25} {'Name':<30} Access")
    print("-" * 80)
    for m in members:
        lvl = access_map.get(m.access_level, str(m.access_level))
        print(f"{m.id:<10} {m.username:<25} {m.name:<30} {lvl}")


def cmd_add_member(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    user_list = gl.users.list(username=args.username)
    if not user_list:
        print(f"User '{args.username}' not found.", file=sys.stderr)
        sys.exit(1)
    user = user_list[0]
    access = ACCESS_LEVELS.get(args.access.lower())
    if access is None:
        print(f"Unknown access level '{args.access}'. Valid: {', '.join(ACCESS_LEVELS)}", file=sys.stderr)
        sys.exit(1)

    if args.group_id:
        obj = gl.groups.get(args.group_id)
    else:
        obj = _get_project(gl, args.project_id)

    obj.members.create({"user_id": user.id, "access_level": access})
    print(f"Added '{args.username}' to {'group' if args.group_id else 'project'} with '{args.access}' access.")


def cmd_remove_member(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    user_list = gl.users.list(username=args.username)
    if not user_list:
        print(f"User '{args.username}' not found.", file=sys.stderr)
        sys.exit(1)
    user = user_list[0]

    if args.group_id:
        obj = gl.groups.get(args.group_id)
    else:
        obj = _get_project(gl, args.project_id)

    obj.members.delete(user.id)
    print(f"Removed '{args.username}' from {'group' if args.group_id else 'project'}.")


def cmd_set_member_access(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    user_list = gl.users.list(username=args.username)
    if not user_list:
        print(f"User '{args.username}' not found.", file=sys.stderr)
        sys.exit(1)
    user = user_list[0]
    access = ACCESS_LEVELS.get(args.access.lower())
    if access is None:
        print(f"Unknown access level '{args.access}'.", file=sys.stderr)
        sys.exit(1)

    if args.group_id:
        obj = gl.groups.get(args.group_id)
    else:
        obj = _get_project(gl, args.project_id)

    member = obj.members.get(user.id)
    member.access_level = access
    member.save()
    print(f"Updated '{args.username}' access to '{args.access}'.")


# ===========================================================================
# CI/CD – Pipelines
# ===========================================================================

def cmd_list_pipelines(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    pipelines = project.pipelines.list(per_page=args.limit or 20)
    print(f"{'ID':<12} {'Status':<12} {'Ref':<30} {'SHA':<12} Created")
    print("-" * 80)
    for p in pipelines:
        print(f"{p.id:<12} {p.status:<12} {p.ref:<30} {p.sha[:8]:<12} {p.created_at}")


def cmd_trigger_pipeline(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    variables = {}
    if args.variables:
        for pair in args.variables:
            k, _, v = pair.partition("=")
            variables[k] = v
    pipeline = project.pipelines.create({"ref": args.ref, "variables": [
        {"key": k, "value": v} for k, v in variables.items()
    ]})
    print(f"Triggered pipeline #{pipeline.id} on ref '{args.ref}': {pipeline.web_url}")


def cmd_cancel_pipeline(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    pipeline = project.pipelines.get(args.pipeline_id)
    pipeline.cancel()
    print(f"Cancelled pipeline #{args.pipeline_id}.")


def cmd_retry_pipeline(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    pipeline = project.pipelines.get(args.pipeline_id)
    pipeline.retry()
    print(f"Retried pipeline #{args.pipeline_id}.")


def cmd_list_pipeline_jobs(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    pipeline = project.pipelines.get(args.pipeline_id)
    jobs = pipeline.jobs.list(get_all=True)
    print(f"{'ID':<12} {'Status':<12} {'Stage':<20} Name")
    print("-" * 80)
    for j in jobs:
        print(f"{j.id:<12} {j.status:<12} {j.stage:<20} {j.name}")


# ===========================================================================
# Repository Files
# ===========================================================================

def cmd_list_files(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    items = project.repository_tree(
        path=args.path or "",
        ref=args.ref or "main",
        get_all=True,
    )
    for item in items:
        icon = "📁" if item["type"] == "tree" else "📄"
        print(f"{icon}  {item['path']}")


def cmd_get_file(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    f = project.files.get(file_path=args.file_path, ref=args.ref or "main")
    print(f.decode().decode("utf-8"))


def cmd_create_file(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    content = args.content or Path(args.content_file).read_text() if args.content_file else ""
    project.files.create({
        "file_path": args.file_path,
        "branch": args.branch,
        "content": content,
        "commit_message": args.message or f"Create {args.file_path}",
    })
    print(f"Created '{args.file_path}' on branch '{args.branch}'.")


def cmd_update_file(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    content = args.content or (Path(args.content_file).read_text() if args.content_file else "")
    f = project.files.get(file_path=args.file_path, ref=args.branch)
    f.content = content
    f.save(branch=args.branch, commit_message=args.message or f"Update {args.file_path}")
    print(f"Updated '{args.file_path}' on branch '{args.branch}'.")


def cmd_delete_file(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    project.files.delete(
        file_path=args.file_path,
        branch=args.branch,
        commit_message=args.message or f"Delete {args.file_path}",
    )
    print(f"Deleted '{args.file_path}' from branch '{args.branch}'.")


# ===========================================================================
# Issues
# ===========================================================================

def cmd_list_issues(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    state = args.state or "opened"
    issues = project.issues.list(state=state, get_all=True)
    print(f"{'IID':<8} {'State':<12} {'Author':<20} Title")
    print("-" * 80)
    for i in issues:
        print(f"#{i.iid:<7} {i.state:<12} {i.author['username']:<20} {i.title[:40]}")


def cmd_create_issue(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    payload: dict = {"title": args.title}
    if args.description:
        payload["description"] = args.description
    if args.labels:
        payload["labels"] = args.labels
    issue = project.issues.create(payload)
    print(f"Created issue #{issue.iid}: {issue.web_url}")


def cmd_close_issue(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    project = _get_project(gl, args.project_id)
    issue = project.issues.get(args.issue_iid)
    issue.state_event = "close"
    issue.save()
    print(f"Closed issue #{args.issue_iid} in project {args.project_id}.")


# ===========================================================================
# Users
# ===========================================================================

def cmd_get_user(gl: gitlab.Gitlab, args: argparse.Namespace) -> None:
    users = gl.users.list(username=args.username)
    if not users:
        print(f"No user found with username '{args.username}'.")
        return
    u = users[0]
    print(f"ID:       {u.id}")
    print(f"Username: {u.username}")
    print(f"Name:     {u.name}")
    print(f"Email:    {getattr(u, 'email', 'N/A')}")
    print(f"State:    {u.state}")
    print(f"Web URL:  {u.web_url}")


# ===========================================================================
# CLI – parser construction
# ===========================================================================

def _add_project_arg(p: argparse.ArgumentParser) -> None:
    p.add_argument("--project-id", required=True, metavar="ID", help="GitLab project ID or path")


def _add_group_arg(p: argparse.ArgumentParser) -> None:
    p.add_argument("--group-id", required=True, metavar="ID", help="GitLab group ID or path")


def _add_branch_arg(p: argparse.ArgumentParser) -> None:
    p.add_argument("--branch", required=True, metavar="BRANCH", help="Branch name")


def _add_access_args(p: argparse.ArgumentParser) -> None:
    levels = list(ACCESS_LEVELS.keys())
    p.add_argument("--merge-access", default="maintainer", choices=levels, help="Merge access level (default: maintainer)")
    p.add_argument("--push-access",  default="maintainer", choices=levels, help="Push access level (default: maintainer)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pg_utility.py",
        description="GitLab management toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")
    sub.required = True

    # ---- Groups ----
    p = sub.add_parser("list-groups", help="List groups")
    p.add_argument("--group-id", metavar="ID", help="Parent group ID (optional; list subgroups)")

    p = sub.add_parser("list-projects", help="List all projects in a group (recursive)")
    _add_group_arg(p)

    # ---- Branches ----
    p = sub.add_parser("list-branches", help="List branches in a project")
    _add_project_arg(p)

    p = sub.add_parser("create-branch", help="Create a branch")
    _add_project_arg(p)
    _add_branch_arg(p)
    p.add_argument("--ref", required=True, metavar="REF", help="Source ref (branch, tag, SHA)")

    p = sub.add_parser("delete-branch", help="Delete a branch")
    _add_project_arg(p)
    _add_branch_arg(p)

    p = sub.add_parser("protect-branch", help="Protect a branch in one project")
    _add_project_arg(p)
    _add_branch_arg(p)
    _add_access_args(p)

    p = sub.add_parser("protect-branch-group", help="Protect a branch across all projects in a group")
    _add_group_arg(p)
    _add_branch_arg(p)
    _add_access_args(p)

    p = sub.add_parser("unprotect-branch", help="Unprotect a branch in one project")
    _add_project_arg(p)
    _add_branch_arg(p)

    p = sub.add_parser("unprotect-branch-group", help="Unprotect a branch across all projects in a group")
    _add_group_arg(p)
    _add_branch_arg(p)

    # ---- Merge Requests ----
    p = sub.add_parser("list-mrs", help="List merge requests")
    _add_project_arg(p)
    p.add_argument("--state", default="opened", choices=["opened", "closed", "merged", "all"])

    p = sub.add_parser("create-mr", help="Create a merge request")
    _add_project_arg(p)
    p.add_argument("--source",      required=True, metavar="BRANCH")
    p.add_argument("--target",      required=True, metavar="BRANCH")
    p.add_argument("--title",       required=True)
    p.add_argument("--description", default="")
    p.add_argument("--assignee",    metavar="USERNAME")

    p = sub.add_parser("merge-mr", help="Accept / merge an MR")
    _add_project_arg(p)
    p.add_argument("--mr-iid", required=True, type=int, metavar="IID")

    p = sub.add_parser("close-mr", help="Close an MR")
    _add_project_arg(p)
    p.add_argument("--mr-iid", required=True, type=int, metavar="IID")

    # ---- Tags & Releases ----
    p = sub.add_parser("list-tags", help="List tags")
    _add_project_arg(p)

    p = sub.add_parser("create-tag", help="Create a tag")
    _add_project_arg(p)
    p.add_argument("--tag",                 required=True, metavar="TAG_NAME")
    p.add_argument("--ref",                 required=True, metavar="REF")
    p.add_argument("--message",             default="",    metavar="MSG")
    p.add_argument("--release-description", default="",    metavar="NOTES")

    p = sub.add_parser("delete-tag", help="Delete a tag")
    _add_project_arg(p)
    p.add_argument("--tag", required=True, metavar="TAG_NAME")

    p = sub.add_parser("create-release", help="Create a release on an existing tag")
    _add_project_arg(p)
    p.add_argument("--tag",         required=True, metavar="TAG_NAME")
    p.add_argument("--name",        default="",    metavar="RELEASE_NAME")
    p.add_argument("--description", default="",    metavar="NOTES")

    # ---- Members ----
    p = sub.add_parser("list-members", help="List members of a group or project")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--group-id",   metavar="ID")
    g.add_argument("--project-id", metavar="ID")

    p = sub.add_parser("add-member", help="Add a user to a group or project")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--group-id",   metavar="ID")
    g.add_argument("--project-id", metavar="ID")
    p.add_argument("--username", required=True)
    p.add_argument("--access",   required=True, choices=list(ACCESS_LEVELS.keys()))

    p = sub.add_parser("remove-member", help="Remove a user from a group or project")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--group-id",   metavar="ID")
    g.add_argument("--project-id", metavar="ID")
    p.add_argument("--username", required=True)

    p = sub.add_parser("set-member-access", help="Change a member's access level")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--group-id",   metavar="ID")
    g.add_argument("--project-id", metavar="ID")
    p.add_argument("--username", required=True)
    p.add_argument("--access",   required=True, choices=list(ACCESS_LEVELS.keys()))

    # ---- CI/CD ----
    p = sub.add_parser("list-pipelines", help="List recent pipelines")
    _add_project_arg(p)
    p.add_argument("--limit", type=int, default=20)

    p = sub.add_parser("trigger-pipeline", help="Trigger a pipeline")
    _add_project_arg(p)
    p.add_argument("--ref",       required=True, metavar="REF")
    p.add_argument("--variables", nargs="*",     metavar="KEY=VALUE")

    p = sub.add_parser("cancel-pipeline", help="Cancel a running pipeline")
    _add_project_arg(p)
    p.add_argument("--pipeline-id", required=True, type=int, metavar="ID")

    p = sub.add_parser("retry-pipeline", help="Retry a failed pipeline")
    _add_project_arg(p)
    p.add_argument("--pipeline-id", required=True, type=int, metavar="ID")

    p = sub.add_parser("list-pipeline-jobs", help="List jobs for a pipeline")
    _add_project_arg(p)
    p.add_argument("--pipeline-id", required=True, type=int, metavar="ID")

    # ---- Repository ----
    p = sub.add_parser("list-files", help="List repository files at a path")
    _add_project_arg(p)
    p.add_argument("--path", default="", metavar="REPO_PATH")
    p.add_argument("--ref",  default="main", metavar="REF")

    p = sub.add_parser("get-file", help="Print file content")
    _add_project_arg(p)
    p.add_argument("--file-path", required=True, metavar="REPO_PATH")
    p.add_argument("--ref",       default="main", metavar="REF")

    p = sub.add_parser("create-file", help="Create a file in the repository")
    _add_project_arg(p)
    p.add_argument("--file-path",    required=True, metavar="REPO_PATH")
    _add_branch_arg(p)
    p.add_argument("--message",      default="",   metavar="COMMIT_MSG")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--content",      metavar="TEXT")
    g.add_argument("--content-file", metavar="LOCAL_PATH")

    p = sub.add_parser("update-file", help="Update a file in the repository")
    _add_project_arg(p)
    p.add_argument("--file-path",    required=True, metavar="REPO_PATH")
    _add_branch_arg(p)
    p.add_argument("--message",      default="",   metavar="COMMIT_MSG")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--content",      metavar="TEXT")
    g.add_argument("--content-file", metavar="LOCAL_PATH")

    p = sub.add_parser("delete-file", help="Delete a file from the repository")
    _add_project_arg(p)
    p.add_argument("--file-path", required=True, metavar="REPO_PATH")
    _add_branch_arg(p)
    p.add_argument("--message",   default="",   metavar="COMMIT_MSG")

    # ---- Issues ----
    p = sub.add_parser("list-issues", help="List issues")
    _add_project_arg(p)
    p.add_argument("--state", default="opened", choices=["opened", "closed", "all"])

    p = sub.add_parser("create-issue", help="Create an issue")
    _add_project_arg(p)
    p.add_argument("--title",       required=True)
    p.add_argument("--description", default="")
    p.add_argument("--labels",      default="",   metavar="label1,label2")

    p = sub.add_parser("close-issue", help="Close an issue")
    _add_project_arg(p)
    p.add_argument("--issue-iid", required=True, type=int, metavar="IID")

    # ---- Users ----
    p = sub.add_parser("get-user", help="Look up a user by username")
    p.add_argument("--username", required=True)

    return parser


# ===========================================================================
# Dispatch table
# ===========================================================================

COMMANDS = {
    "list-groups":          cmd_list_groups,
    "list-projects":        cmd_list_projects,
    "list-branches":        cmd_list_branches,
    "create-branch":        cmd_create_branch,
    "delete-branch":        cmd_delete_branch,
    "protect-branch":       cmd_protect_branch,
    "protect-branch-group": cmd_protect_branch_group,
    "unprotect-branch":     cmd_unprotect_branch,
    "unprotect-branch-group": cmd_unprotect_branch_group,
    "list-mrs":             cmd_list_mrs,
    "create-mr":            cmd_create_mr,
    "merge-mr":             cmd_merge_mr,
    "close-mr":             cmd_close_mr,
    "list-tags":            cmd_list_tags,
    "create-tag":           cmd_create_tag,
    "delete-tag":           cmd_delete_tag,
    "create-release":       cmd_create_release,
    "list-members":         cmd_list_members,
    "add-member":           cmd_add_member,
    "remove-member":        cmd_remove_member,
    "set-member-access":    cmd_set_member_access,
    "list-pipelines":       cmd_list_pipelines,
    "trigger-pipeline":     cmd_trigger_pipeline,
    "cancel-pipeline":      cmd_cancel_pipeline,
    "retry-pipeline":       cmd_retry_pipeline,
    "list-pipeline-jobs":   cmd_list_pipeline_jobs,
    "list-files":           cmd_list_files,
    "get-file":             cmd_get_file,
    "create-file":          cmd_create_file,
    "update-file":          cmd_update_file,
    "delete-file":          cmd_delete_file,
    "list-issues":          cmd_list_issues,
    "create-issue":         cmd_create_issue,
    "close-issue":          cmd_close_issue,
    "get-user":             cmd_get_user,
}


# ===========================================================================
# Entry point
# ===========================================================================

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        gl = authenticate_gitlab()
    except Exception as exc:
        print(f"Authentication failed: {exc}", file=sys.stderr)
        sys.exit(1)

    handler = COMMANDS.get(args.command)
    if handler is None:
        parser.print_help()
        sys.exit(1)

    try:
        handler(gl, args)
    except gitlab.exceptions.GitlabError as exc:
        print(f"GitLab API error: {exc}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nAborted.", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
