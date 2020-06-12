#!C:\Users\thimna.alves\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0\python.exe
"""Autoconfigure a Django project from on a github URL.

- downloads the repo
- creates a virtualenv and installs django 1.x (or detects a requirements.txt if available)
- creates webapp via api
- creates django wsgi configuration file
- adds static files config

Usage:
  pa_autoconfigure_django.py <git-repo-url> [--domain=<domain> --python=<python-version>] [--nuke]

Options:
  --domain=<domain>         Domain name, eg www.mydomain.com   [default: your-username.pythonanywhere.com]
  --python=<python-version> Python version, eg "3.8"    [default: 3.6]
  --nuke                    *Irrevocably* delete any existing web app config on this domain. Irrevocably.
"""

from docopt import docopt

from pythonanywhere.django_project import DjangoProject
from pythonanywhere.snakesay import snakesay
from pythonanywhere.utils import ensure_domain


def main(repo_url, domain, python_version, nuke):
    domain = ensure_domain(domain)
    project = DjangoProject(domain, python_version)
    project.sanity_checks(nuke=nuke)
    project.download_repo(repo_url, nuke=nuke),
    project.create_virtualenv(nuke=nuke)
    project.create_webapp(nuke=nuke)
    project.add_static_file_mappings()
    project.find_django_files()
    project.update_wsgi_file()
    project.update_settings_file()
    project.run_collectstatic()
    project.run_migrate()
    project.webapp.reload()
    print(snakesay(f'All done!  Your site is now live at https://{domain}'))
    print()
    project.start_bash()


if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(arguments['<git-repo-url>'], arguments['--domain'], arguments['--python'], nuke=arguments.get('--nuke'))
