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

