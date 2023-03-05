import pathlib
import yaml
from jinja2 import Environment, FileSystemLoader


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
        with open(yaml_file) as fh:
            data = yaml.load(fh, Loader=yaml.Loader)
        organisations[ yaml_file.parts[-1].replace('.yaml', '') ] = data
    return organisations

def read_github_organisation(root, organisations):
    github_organisations = []
    for yaml_file in root.joinpath('github').iterdir():
        # print(yaml_file)
        with open(yaml_file) as fh:
            data = yaml.load(fh, Loader=yaml.Loader)
        if not 'type' in data:
            exit(f'type is missing from {yaml_file}')
        if data['type'] not in ['corporation', 'non-profit']:
            exit(f'Invalid type in {yaml_file}')
        if not 'name' in data:
            exit(f'name is missing from {yaml_file}')
        if 'org' in data:
            if data['org'] not in organisations:
                exit(f"Invalid org '{data['org']}' in {yaml_file}")
            data['org']  = organisations[ data['org'] ]
        data['id'] = yaml_file.parts[-1].replace('.yaml', '')
        #print(data)
        github_organisations.append(data)

    github_organisations.sort(key=lambda org: org['name'].lower())

    return github_organisations


def main():
    root = pathlib.Path(__file__).parent
    out_dir = root.joinpath("_site")
    out_dir.mkdir(exist_ok=True)

    organisations = read_organisations(root)
    # print(organisations)
    github_organisations = read_github_organisation(root, organisations)
    # print(github_organisations)

    render('index.html', out_dir.joinpath('index.html'),
        github_organisations = github_organisations,
        title = 'Open Source by organisations',
    )

main()
