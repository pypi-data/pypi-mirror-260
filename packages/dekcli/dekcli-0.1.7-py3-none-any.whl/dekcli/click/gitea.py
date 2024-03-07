import os
import git
import typer
from getpass import getpass
from dektools.cfg import ObjectCfg
from dektools.file import sure_dir, normal_path
from dektools.yaml import yaml
from ..core.git import giteaapi
from ..core.git.repo import list_repos

cfg = ObjectCfg('dekcli/gitea')

default_name = 'index'

app = typer.Typer(add_completion=False)


@app.command()
def site(url, name=default_name):  # url: {schema}://{host}{port}
    token = getpass(f"Please input token: ")
    cfg.update({name: dict(url=url.rstrip('/ '), token=token.strip())})


@app.command()
def pull(path, name=default_name):
    path = normal_path(path)
    sure_dir(path)
    ins = giteaapi.get_ins(name)
    for org in giteaapi.get_orgs(ins):
        for repo in org.get_repositories():
            path_repo = os.path.join(path, repo.get_full_name())
            sure_dir(path_repo)
            git.Repo.clone_from(repo.ssh_url, path_repo)


@app.command()
def index(path, name=default_name):
    ins = giteaapi.get_ins(name)
    ors = giteaapi.OrgRepoSure(ins)

    path_index = os.path.join(path, 'index.yaml')
    if os.path.isfile(path_index):
        data_index = yaml.load(path_index)
    else:
        data_index = {}

    for org_name, org_data in data_index.get('orgs', {}).items():
        print(f"org: {org_name}", flush=True)
        org, _ = ors.get_org_repos(org_name)
        giteaapi.patch_org(ins, org.name, org_data or {})

    for orn, url in data_index.get('mirrors', {}).items():
        org_name, repo_name = orn.split('/')
        print(f"mirror: {url}", flush=True)
        ors.get_or_mirror(org_name, repo_name, url)

    # tokens = {}
    # for name, scopes in data_index.get('tokens', {}).items():
    #     tokens[name] = giteaapi.create_token(ins, name, scopes)

    for key, variable_value in data_index.get('variables', {}).items():
        org_name, variable_name = key.split('/')
        print(f"variable: {org_name} {variable_name}", flush=True)
        ors.get_org_repos(org_name)

    for key, secret_value in data_index.get('secrets', {}).items():
        org_name, secret_name = key.split('/')
        print(f"secret: {org_name} {secret_name}", flush=True)
        ors.get_org_repos(org_name)


@app.command()
def push(path, name=default_name):
    ins = giteaapi.get_ins(name)
    ors = giteaapi.OrgRepoSure(ins)
    for org_name, org_data in list_repos(path).items():
        for repo_name, repo_data in org_data.items():
            mirror = repo_data['mirror']
            if mirror:
                print(f"mirror: {mirror}", flush=True)
                ors.get_or_mirror(org_name, repo_name, mirror)
            else:
                print(f"enter: {repo_data['path']}", flush=True)
                repo = ors.get_or_create(org_name, repo_name, repo_data['branches'][0])
                git_repo = git.Repo(repo_data['path'])
                origin = git_repo.create_remote('origin', repo.ssh_url)
                print(f"pushing: {repo.ssh_url}", flush=True)
                for name in repo_data['branches']:
                    origin.push(refspec=f"{name}:{name}")
                tags = repo_data['tags']
                for tag in tags[:-1]:
                    origin.push(tag)
                if tags:
                    giteaapi.patch_repo(ins, org_name, repo_name, dict(has_actions=True))
                    origin.push(tags[-1])
