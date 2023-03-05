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

def main():
    root = pathlib.Path(__file__).parent
    out_dir = root.joinpath("_site")
    out_dir.mkdir(exist_ok=True)

    organizations = []
    for yaml_file in root.joinpath('github').iterdir():
        # print(yaml_file)
        with open(yaml_file) as fh:
            data = yaml.load(fh, Loader=yaml.Loader)
            data['id'] = yaml_file.parts[-1].replace('.yaml', '')
            #print(data)
            organizations.append(data)

    render('index.html', out_dir.joinpath('index.html'),
        organizations = organizations,
        title = 'Open Source by Organizations',
    )

main()
