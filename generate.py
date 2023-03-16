import json
import os
import requests
import pathlib
import yaml
from jinja2 import Environment, FileSystemLoader

root = pathlib.Path(__file__).parent

cache = root.joinpath('cache')
cache.mkdir(exist_ok=True)

config_file = root.joinpath('config.yaml')
with open(config_file) as fh:
    config = yaml.load(fh, Loader=yaml.Loader)


def render(template, filename, **args):
    templates_dir = pathlib.Path(__file__).parent.joinpath('templates')
    env = Environment(loader=FileSystemLoader(templates_dir), autoescape=True)
    html_template = env.get_template(template)
    html_content = html_template.render(**args)
    with open(filename, 'w') as fh:
        fh.write(html_content)


def read_organisations(root):
    organisations = {}
    for yaml_file in root.joinpath('organisations').iterdir():
        if yaml_file.suffix != '.yaml':
            exit(f"Invalid file name {yaml_file}")
        with open(yaml_file) as fh:
            data = yaml.load(fh, Loader=yaml.Loader)
        organisations[ yaml_file.parts[-1].replace('.yaml', '') ] = data
    return organisations


def read_github_organisations(root, organisations):
    github_organisations = []
    for yaml_file in root.joinpath('github').iterdir():
        if yaml_file.suffix != '.yaml':
            exit(f"Invalid file name {yaml_file}")
        # print(yaml_file)
        with open(yaml_file) as fh:
            data = yaml.load(fh, Loader=yaml.Loader)

        if 'org' in data:
            if data['org'] not in organisations:
                exit(f"Invalid org '{data['org']}' in {yaml_file}")
            data['org_name']  = organisations[ data['org'] ]['name']
            for field in organisations[ data['org'] ]:
                if field == 'name':
                    continue
                if field in data:
                    exit(f'File has "{field}" field but also inherits it from org in {yaml_file}')
                    continue
                data[field] = organisations[ data['org'] ][field]


        if not 'type' in data:
            exit(f'type is missing from {yaml_file}')
        if data['type'] not in config['org_types'].keys():
            exit(f"Invalid type '{data['type']}' in {yaml_file}")
        if not 'name' in data:
            exit(f'name is missing from {yaml_file}')
        if data['name'] == '':
            exit(f'name is empty in {yaml_file}')
        data['id'] = yaml_file.parts[-1].replace('.yaml', '')

        if 'country' in data:
            if data['country'] not in config['countries']:
                exit(f"Country '{data['country']}'  in {yaml_file} is not in our approved list. Either add it to config.yaml or fix the name if it is a different spelling.")
        #print(data)
        github_organisations.append(data)

    github_organisations.sort(key=lambda org: org['name'].lower())

    return github_organisations

def get_data_from_github(github_organisations):
    token = os.environ.get('MY_GITHUB_TOKEN')
    if not token:
        print('Missing MY_GITHUB_TOKEN. Not collecting data from Github')
        return
    print('Collecting data')

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2022-11-28',
    }

    for org in github_organisations:
        print(org['id'])
        cache_file = cache.joinpath(org['id'].lower() + '.json')
        if not cache_file.exists():
            url = f"https://api.github.com/orgs/{org['id']}"
            # print(url)
            org_data = requests.get(url, headers=headers).json()
            # print(org_data)
            # print(org_data)
            with open(cache_file, 'w') as fh:
                json.dump(org_data, fh)

        with open(cache_file) as fh:
            org['github'] = json.load(fh)


def main():
    out_dir = root.joinpath("_site")
    out_dir.mkdir(exist_ok=True)
    out_dir.joinpath("github").mkdir(exist_ok=True)

    organisations = read_organisations(root)
    # print(organisations)
    github_organisations = read_github_organisations(root, organisations)
    # print(github_organisations)

    get_data_from_github(github_organisations)

    for org in github_organisations:
        render('git-organization.html', out_dir.joinpath('github', f"{org['id']}.html"),
            org = org,
            title = org['name'],
            org_types = config['org_types'],
        )

    render('index.html', out_dir.joinpath('index.html'),
        github_organisations = github_organisations,
        title = 'Open Source by organisations',
        org_types = config['org_types'],
    )
    for org_type, display_name in config['org_types'].items():
        render('index.html', out_dir.joinpath(f'{org_type}.html'),
            github_organisations = [org for org in github_organisations if org['type'] == org_type],
            title = f'Open Source by {display_name}',
            org_types = config['org_types'],
        )


main()
