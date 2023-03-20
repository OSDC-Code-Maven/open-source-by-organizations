import json
import os
import requests
import pathlib
import shutil
import yaml
from jinja2 import Environment, FileSystemLoader

root = pathlib.Path(__file__).parent

cache = root.joinpath('cache')
cache.mkdir(exist_ok=True)
cache.joinpath('repos').mkdir(exist_ok=True)

config_file = root.joinpath('config.yaml')
with open(config_file) as fh:
    config = yaml.load(fh, Loader=yaml.Loader)

locations = dict({ display_name.lower().replace(' ', '-') : display_name  for display_name in config['countries']})


def render(template, filename, **args):
    templates_dir = pathlib.Path(__file__).parent.joinpath('templates')
    env = Environment(loader=FileSystemLoader(templates_dir), autoescape=True)
    html_template = env.get_template(template)
    html_content = html_template.render(**args, org_types=config['org_types'], locations=locations)
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

def get_from_github(url, cache_file, expected=0, pages=False):
    token = os.environ.get('MY_GITHUB_TOKEN')
    if not token:
        print('Missing MY_GITHUB_TOKEN. Not collecting data from Github')
        return

    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2022-11-28',
    }

    if pages:
        per_page = 100 # default is 30 max is 100
        page = 1
        all_data = []
        while True:
            real_url = f"{url}?per_page={per_page}&page={page}"
            print(f"Fetching from {real_url}")
            data = requests.get(real_url, headers=headers).json()
            all_data.extend(data)
            print(f"Received {len(data)} Total {len(all_data)} out of an expected {expected}")
            page += 1
            if len(data) < per_page:
                break
    else:
        print(f"Fetching from {url}")
        all_data = requests.get(url, headers=headers).json()


    # print(data)
    with open(cache_file, 'w') as fh:
        json.dump(all_data, fh)



def get_data_from_github(github_organisations):

    for org in github_organisations:
        # print(org['id'])
        cache_file = cache.joinpath(org['id'].lower() + '.json')
        if not cache_file.exists():
            get_from_github(f"https://api.github.com/orgs/{org['id']}", cache_file)

        if cache_file.exists():
            with cache_file.open() as fh:
                org['github'] = json.load(fh)

        if org['github'].get('message', '') == "Not Found":
            print(f"Not Found {org['id']}")
            continue

        # Get list of repos
        cache_file = cache.joinpath('repos', org['id'].lower() + '.json')
        if not cache_file.exists():
            get_from_github(f"https://api.github.com/orgs/{org['id']}/repos", cache_file, expected=org['github']['public_repos'], pages=True)

        if cache_file.exists():
            with cache_file.open() as fh:
                org['github']['repos'] = json.load(fh)


def generate_html_pages(github_organisations):
    out_dir = root.joinpath("_site")
    out_dir.mkdir(exist_ok=True)

    ci = os.environ.get('CI')
    # In the local environment we imitate the same URL as will be in the deployment on https://osdc.code-maven.com/
    if not ci:
        with out_dir.joinpath('index.html').open('w') as fh:
            fh.write('<a href="/open-source-by-organizations/">site</a>')
        out_dir = out_dir.joinpath('open-source-by-organizations')
        out_dir.mkdir(exist_ok=True)

    js_dir = out_dir.joinpath('js')
    js_dir.mkdir(exist_ok=True)
    shutil.copy(pathlib.Path(__file__).parent.joinpath('js', 'osdc.js'), js_dir.joinpath('osdc.js'))

    out_dir.joinpath("github").mkdir(exist_ok=True)
    for org in github_organisations:
        render('git-organization.html', out_dir.joinpath('github', f"{org['id'].lower()}.html"),
            org = org,
            title = org['name'],
        )
    stats = {
        'by_type': {}
    }

    for org_type, display_name in config['org_types'].items():
        organisations = [org for org in github_organisations if org['type'] == org_type]
        stats['by_type'][org_type] = len(organisations)
        render('list.html', out_dir.joinpath(f'{org_type}.html'),
            github_organisations = organisations,
            title = f'Open Source by {display_name}',
        )

    out_dir.joinpath("loc").mkdir(exist_ok=True)
    for path, display_name in locations.items():
        render('list.html', out_dir.joinpath('loc', f'{path}.html'),
            github_organisations = [org for org in github_organisations if org.get('country', '') == display_name],
            title = f'Open Source in {display_name}',
        )

    render('index.html', out_dir.joinpath('index.html'),
        title = 'Open Source by organisations',
        stats = stats,
    )



def main():
    organisations = read_organisations(root)
    # print(organisations)
    github_organisations = read_github_organisations(root, organisations)
    # print(github_organisations)

    get_data_from_github(github_organisations)

    generate_html_pages(github_organisations)


main()
