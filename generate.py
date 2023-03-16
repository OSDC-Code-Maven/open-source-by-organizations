import pathlib
import yaml
from jinja2 import Environment, FileSystemLoader

org_types = ['corporation', 'non-profit', 'university', 'other', 'gov']

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

def read_github_organisation(root, organisations):
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
        if data['type'] not in org_types:
            exit(f"Invalid type '{data['type']}' in {yaml_file}")
        if not 'name' in data:
            exit(f'name is missing from {yaml_file}')
        if data['name'] == '':
            exit(f'name is empty in {yaml_file}')
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
        org_types = org_types,
    )
    for org_type in org_types:
        render('index.html', out_dir.joinpath(f'{org_type}.html'),
            github_organisations = [org for org in github_organisations if org['type'] == org_type],
            title = f'Open Source by {org_type}',
            org_types = org_types,
        )


main()
