# Open Source

There are a lot of corporations, non-profits, higher education institutions, and even governments, that share some of the software they created for themselves under an Open Source license.

In this repository we collect these organizations and then analyze their projects.

Some of the contributions is collecting and curating data that does not require programming. It only requires an understanding of what is a "github organization", what is a yaml file,
and how to send a pull-request.

## Why would information about these open source projects be interesting?

Let's say you are interested in being employed by company XYZ. You can increase your chances of success by making yourself familiar with the company and some of the projects of the company.
Find their open source projects, make yourself familiar with their code, open some issues, send some pull-requests.
If you are lucky they might notice you and offer you a job. Even if that does not happen you can include your contribution in your CV and you can mention it during the ineterview.

Somewhat surprisingly there are many local and country-wise governments around the world that share some of their software under and Open Source license.
We are collecting those too in this list.

Many Universities and other Higher Education Institutions have projects of their own that were released under an Open Source license.
We collect the GitHub organizations of the institutions or that of specific labs or departments of these institutions.

If you know more send a Pull-Request or open an issue with the links.

## What is an "organization"

Unfortunately there is a slight overloading of the world "organization" as it can refer to both a "github-organization"
and a "real-world-organization" and the mapping is not 1-1.

In this project we try to use the expression "real-world-organization" to any corporation, university, colleges, non-profits, government etc.
and "github-organization" to any organization in GitHub that has a page `https://github.com/ORGNAME`.

## Why would you want to contribute to

### Corporations?

There are a lot of corporations that share some of the software they created for themselves under an Open Source license.
It is very interesting to see and also an opportunity to increase your chances of employment. Make yourself familiar with their
code, open some issues, send some pull-requests. If you are lucky they might notice you and offer you a job. Even if that does
not happen you can include your contribution in your CV and you can mention it during the interview.

### Governments?

Somewhat surprisingly there are many local and country-wise governments around the world that share some of their software under and Open Source license. We are collecting them in this list.

### Non-profits?

If they help the world and you help them, then you help the world too, right?

real-world organization

## File format

### `data/github/`

We store information about GitHub-organizations (not about individual GitHub repositories).

Each github-organization that belongs to a real-world-organization will have an entry in this folder.

The name of the file is `github/organization.yaml` where `organization` is the lower case version of the name that comes from the URL: `https://github.com/organization/`.

Required fields: `name` and either `type` or `org`.

Optional fields: `city`, `state`, `country`.

```
org:
name:
```

### `data/organisations/`

Some real-world-organizations have multiple GitHub-organizations. For example in a university each research lab might have its own GitHub organization. In order to store common information about these github-organizations we have a separate folder called `data/organisations/` where we store a YAML file for each such real-world-organization. The YAML files in the `data/github/` folder then will have to refer to this entity by adding the `org:` field.

For example see the `data/organisations/bosch.com.yaml` or `data/organisations/mit.edu.yaml` entries of real-world-organizations.

Here the filename should be the domain name of the real-world-organization.yaml. This is not always the case. We are fixing it now.

Required fields: `type`, `url`.
Optional fields: `city`, `state`, `country`

```
name:
type: corporation university gov non-profit other
url:
city:
state:
country:
```

### Valid values

Valid values for the `type` field can be found in the [config.yaml](config.yaml) file as the keys of the `org_types` section.


## How to find more organization?

1. On GitHub search for the name of a corporation we don't have in our list yet.
1. Check if there is a github-organization that holds project belonging to this corporation
1. Add the appropriate yaml file to our repository.

1. There are several `issues` of our project with links to lists of universities, government institutions etc.

1. On GitHub search for the names of countries, cities, municipalies, etc.



## Local development

* Clone repo

```
git clone git@github.com:OSDC-Code-Maven/open-source-by-organizations.git
cd open-source-by-organizations
```

* Setup virtualenv end install python dependencies

```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt -c constraints.txt
```

* Generate GITHUB token
    * See the [documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

    * Visit [GitHub](https://github.com/) (and log in)
    * Go to [Settings](https://github.com/settings/profile)
    * Go to [Developer Settings](https://github.com/settings/apps)
    * Personal Access tokens / Tokens
    * Generate New token
    * Enable following: notifications, read:org, read:project, read:user, user:email

Then create the environment variable with the value:

```
export MY_GITHUB_TOKEN=.....
```

* Collect **all** the data and generate web site. The following can take several minutest. It might be better to specify a few YAML files and only work with those as in the next command.

```
python generate.py
```

* Collect only information only about these two github organizations.

```
python generate.py data/github/bioinform.yaml data/github/calgaryml.yaml
```

* Start the local web server

```
./app.py
```

Visit the site at http://localhost:5000/

## Dependabot and upgrading dependencies

While we have dependabot enabled it will open PR for each upgrade separately and then the CI won't run for all of them.

Our alternative is to run this once a month:

```
virtualenv -p python3 venv
source venv/bin/activate
pip install -U -r requirements.txt
pytest
pip freeze > constraints.txt
```


