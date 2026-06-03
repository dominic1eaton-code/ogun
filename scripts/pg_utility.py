#!/usr/bin/env python3
# @brief: This script interacts with the GitLab API to manage projects and branches. It includes functions to list all 
#         projects in a group, list projects in subgroups, create protected branches, and protect branches across all 
#         projects in a group. The script uses the python-gitlab library for API interactions.
# @author: Dominic E. (@eatondo)
import gitlab
from pathlib import Path


def authenticate_gitlab():
    # Get the home directory Path object
    home_dir = Path.home()
    gl = gitlab.Gitlab.from_config()
    return gl

# Authenticate with your GitLab instance
gl = authenticate_gitlab()


def list_all_projects(group_id):
    # Get the group object (lazy=True avoids an extra API call)
    group = gl.groups.get(group_id, lazy=True)
    # Fetch ALL projects directly under this group
    # 'get_all=True' or 'iterator=True' forces pagination to load everything
    projects = group.projects.list(get_all=True, archived=False, iterator=True)
    active_projects = []
    for project in projects:
        # Check if the project is NOT scheduled for deletion
        if project.marked_for_deletion_on is None:
            active_projects.append(project)
    return active_projects

def list_projects_in_subgroups(group):
    # Fetch projects in the current group
    projects = group.projects.list(get_all=True)
    for project in projects:
        print(f"Path: {project.path_with_namespace} | ID: {project.id}")
    # Recursively fetch subgroups and their projects
    subgroups = group.subgroups.list(get_all=True)
    for subgroup in subgroups:
        subgroup_obj = gl.groups.get(subgroup.id, lazy=True)
        list_projects_in_subgroups(subgroup_obj)
    return subgroups


def create_protected_branch(project_id, branch_name):
    project = gl.projects.get(project_id)
    # Check if a specific branch exists and is protected
    try:
        branch = project.branches.get('main')
        if branch.protected:
            print("The branch is protected.")
        else:
            print("The branch exists but is not protected.")
    except gitlab.exceptions.GitlabGetError:
        print("The branch does not exist.")
        project.protectedbranches.create({
            "name": branch_name,
            "merge_access_level": gitlab.const.AccessLevel.MAINTAINER,
            "push_access_level": gitlab.const.AccessLevel.MAINTAINER,
            "allow_force_push": False,
        })
    try:
        # Try to fetch the branch to check if it exists
        branch = project.branches.get(branch_name)
        print(f"Branch '{branch_name}' already exists.")
    except gitlab.GitlabGetError as e:
        # If a 404 error occurs, the branch does not exist
        if e.response_code == 404:
            print(f"Branch '{branch_name}' does not exist. Creating it now...")
            source_branch = 'main'  # You can change this to 'develop' or any existing branch
            # Create the new branch
            new_branch = project.branches.create({
                'branch': branch_name,
                'ref': source_branch
            })
            print(f"Successfully created branch '{new_branch.name}' from '{source_branch}'.")
        else:
            # Re-raise the exception if it's a different GitLab error (e.g., 403 Forbidden)
            raise e

def protect_branch_in_group(group_id, branch_name):
    group = gl.groups.get(group_id)
    projects = list_all_projects(group_id)
    for project in projects:
        print(f"Protecting branch '{branch_name}' in project '{project.name}' (ID: {project.id})")
        create_protected_branch(project.id, branch_name)

if __name__ == "__main__":
    # Example usage:
    group_id = '132780099' # https://gitlab.com/ogun-foundation
    branch_name = 'develop'  # or 'main' or any branch you want to protect
    protect_branch_in_group(group_id, branch_name)
