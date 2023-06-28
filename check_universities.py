import json
import os
import re
import yaml

# Clone the University domain list next to where you cloned our repository
# git clone https://github.com/Hipo/university-domains-list.git

# then this path should be valid:
filename = os.path.join('..', 'university-domains-list', 'world_universities_and_domains.json')

def get_all_the_domains_we_already_have():
    organizations = set([name[0:-5] for name in os.listdir(os.path.join('data', 'organisations'))])
    print(sorted(organizations))
    for github_file in os.listdir(os.path.join('data', 'github')):
        #print(github_file)
        with open(os.path.join('data', 'github', github_file)) as fh:
            data = yaml.load(fh, Loader=yaml.Loader)
            if 'url' in data:
                #print(data['url'])
                url = re.sub(r'/$', '', re.sub(r'https?://(www\.)?', '', data['url']))
                #print(url)
                organizations.add(url)
    #print(organizations)
    return organizations


def main():
    get_all_the_domains_we_already_have()

    # go over the domain in the other list and print the ones we are missing
    #with open(filename) as fh:
    #    universities = json.load(fh)

    #    for univ in universities:
    #        for domain in univ['domains']:
    #            if not os.path.exists('data/organisations/{domain}.yaml'):
    #                print(domain)

main()
