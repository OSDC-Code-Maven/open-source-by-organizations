# Open Source

There are a lot of corporations, non-profits, higher education institutions, and even governments, that share some of the software they created for themselves under an Open Source license.

It is very interesting to see and also an opportunity to increase your chances of employment. Make yourself familiar with their code, open some issues, send some pull-requests. If you are lucky they might notice you and offer you a job. Even if that does not happen you can include your contribution in your CV and you can mention it during the ineterview.

Somewhat surprisingly there are many local and country-wise governments around the world that share some of their software under and Open Source license. We are collecting them in this list.

The following Universities and other Higher Education Institutions have projects of their own that were released under an Open Source license.
Here you can find links to the GitHub organizations of the institutions or that of specific labs or departments of these institutions.

If you know more send a Pull-Request or open an issue with the links.

In this repository we collect these organizations.

## File format

### `organisations/`

Some corporation and universities have multiple GitHub organizations. For example in a university each research lab might have its own GitHub organization. In order to have store common information about these we have a separate folder called `organisations/` where we have a YAML file for each such corporation or university. The YAML files in the `github/` folder can refer to this entity by adding the `org:` field.

For example see the `Bosch` entries.

Required fields: `type`, `url`.
Optional fields: `city`, `state`, `country`


### `github/`

We store information about GitHub organizations (not about individual GitHub repositories).
The name of the file is `github/ORGA.yaml` where ORGA is the exact same name as `https://github.com/ORGA/`. The exact case will be used to display the name of the repository.

Required fields: `name` and either `type` or `org`.

Optional field: `city`, `state`, `country`.

### Valid values

Valid values for the `type` field can be found in the [config.yaml](config.yaml) file as the keys of the `org_types` section.

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
python generate.py github/bioinform.yaml github/calgaryml.yaml
```

* Start the local web server

```
./app.py
```

Visit the site at http://localhost:5000/


