#!/usr/bin/env python3

"""
Convert a markdown file to pdf or (if requested) create a tex file

Configuration is possible
- in the header of the markdown file
- thru environment variable settings
- and command line arguments



Environment variables]

- `MD2PDF_TEMPLATE`: location of the template file
- `MD2PDF_LOGO`: location of the logo
- `MD2PDF_AUTHOR_NAME`: author's name
- `MD2PDF_AUTHOR_EMAIL`: author's email
- `MD2PDF_COMPANY`: company name to use

Command line arguments

- `--template`: location of the template file
- `--logo`: location of the logo
- `--logo-width`: log width (default 40)
- `--company`: company name
- `--department`: department name

Header of the markdown file

- the header is in YAML
- may contain the following values
    - `author.name`: required
    - `author.email`: optionalA_A~  !11111111111111111111111111111111111111spt<F4>jhl-===[]
    - `author.affiliation`: optional
    - `title`: required
    - `titlepage`: true or false (required)
    - `subtitle`: true or false (required)
    - `toc`: true or false (required)
    - `date`: required
"""

import os
import sys
import subprocess

from typing import List, Optional
from pathlib import Path

from datetime import date

import typer

import toml


__version__ = '1.1.1'



def version_callback(value: bool) -> None:
    """Print version information """

    if value:
        typer.echo(f'md2pdf Version: {__version__}')
        raise typer.Exit()


class PandocCmd:
    """Class to hold the pandoc command and its parameters

    Some parameters are simply hardcoded others can be set with

    - set_v: which sets `-V` parameters
    - set_m: which sets `-M` parameters
    - append: appends simple parameters
    - extend: adds a list of parameters

    """
    pandoc: List[str]

    def __init__(self, outfile: str) -> None:
        self.pandoc = [
            'pandoc',
            '-o',
            outfile,
            '-f',
            'markdown+smart',
            '--number-sections',
            '-M',
            'colorlinks=true',
            '-V',
            'linkcolor=ForestGreen',
            '-V',
            'classoption=oneside',
            '-V',
            'listings',
            '-M',
            'toc-own-page=true',
            '--highlight-style',
            'pygments',
        ]

    def run(self) -> None:
        """Run pandoc command

        In case of error exit with return code 1
        """

        result = subprocess.run(self.pandoc, check=True).returncode
        if result:
            print(f'pandoc error: {result}')
            sys.exit(1)

    def set_v(self, varname: str, varval: Optional[str]) -> None:
        """Adds a `-V` parmeter.

        We check here if the parameter value is not None

        """

        if varval:
            self.pandoc.append('-V')
            self.pandoc.append(f'{varname}={varval}')

    def set_m(self, varname: str, varval: Optional[str]) -> None:
        """Adds a `-M` parmeter.

        We check here if the parameter value is not None

        """
        if varname:
            self.pandoc.append('-M')
            self.pandoc.append(f'{varname}={varval}')

    def append(self, argument: str) -> None:
        """Adds a single parmeter

        """
        self.pandoc.append(argument)

    def extend(self, mdfiles: List[str]) -> None:
        """Adds a list of parmeters

        """
        self.pandoc.extend(mdfiles)


def main(
    files: List[Path] = typer.Argument(default=None, dir_okay=False, exists=True),
    template: Optional[str] = typer.Option(
        None, '--template', help='Name of template file'
    ),
    logo: Optional[str] = typer.Option(None, '--logo', help='Name of logo file'),
    logo_width: Optional[str] = typer.Option(
        None, '--logo-width', help='Logo width (default 35mm)'
    ),
    no_toc: bool = typer.Option(
        False, '--no-toc', help='table of contents in PDF document'
    ),
    no_title: bool = typer.Option(False, '--no-title', help='title in PDF document'),
    tex_file: bool = typer.Option(
        False, '--tex', help='create TeX file instead of PDF document'
    ),
    company: Optional[str] = typer.Option(None, '--company', help='Name of company'),
    department: Optional[str] = typer.Option(
        None, '--department', help='Name of department'
    ),
    confidential: bool = typer.Option(
        False, '--confidential', help='indicate confidential'
    ),
    debug: bool = typer.Option(False, '--debug', help='turns debugging on'),
    pdf_engine: str = typer.Option(
        'xelatex',
        '--pdf-engine',
        help='Specify pdf engine, one of lualatex, xelatex or tectonic ',
    ),
    _version: bool = typer.Option(
        None, '-V', '--version', callback=version_callback, help='Show version and exit'
    ),
):
    """Create a PDF file from one or more markdown files"""

    if not files:
        typer.echo('Error: Must specify at least one .md file.')
        raise typer.Abort()

    mdfiles: List[str] = [str(md) for md in files]

    template = os.environ.get('MD2PDF_TEMPLATE') or template
    if template is None:
        print('No template specified')
        sys.exit(1)

    email = os.environ.get('MD2PDF_AUTHOR_EMAIL')
    footer_center = ''

    # check correct pdf-engine
    if pdf_engine not in ['xelatex', 'lualatex', 'tectonic']:
        print('--pdf-engine must be one of "xelatex", "lualatex", "tectonic"')
        sys.exit(1)

    ext = '.pdf'
    if tex_file:
        ext = '.tex'

    if len(mdfiles) == 1:
        toml_file = os.path.splitext(mdfiles[0])[0] + '.toml'

        if os.path.exists(toml_file):
            print(f'TOML file {toml_file} found')
            parsed_toml = toml.load(toml_file)
            default_val = parsed_toml.get('default')
            if default_val is None:
                print(f'No file names found in {toml_file}')
            else:
                mdfiles = default_val.get('files')

    for mdf in mdfiles:
        print(f'Compiling {mdf}')

    main_mdfile = os.path.realpath(mdfiles[0])

    outfile = Path(main_mdfile).stem + ext

    year = date.today().year

    company = os.environ.get('MD2PDF_COMPANY') or company
    department = os.environ.get('MD2PDF_DEPARTMENT') or department

    if company:
        if confidential:
            footer_center = f'© Copyright {year} {company}'
        else:
            footer_center = f'{year} {company}'

    pdcmd = PandocCmd(outfile)
    pdcmd.append(f'--template={template}')
    pdcmd.append(f'--pdf-engine={pdf_engine}')

    pdcmd.set_v('footer-center', footer_center)
    pdcmd.set_v('company', company)
    pdcmd.set_v('department', department)

    if no_title:
        pdcmd.set_m('titlepage', 'false')

    logo = os.environ.get('MD2PDF_LOGO') or logo
    pdcmd.set_v('logo', logo)

    logo = os.environ.get('MD2PDF_LOGO_WIDTH') or logo_width
    pdcmd.set_v('logo-width', logo_width)

    pdcmd.set_v('email', email)

    if not no_toc:
        pdcmd.append('--toc')

    pdcmd.extend(mdfiles)

    if debug:
        print(' '.join(pdcmd.pandoc))


    pdcmd.run()


if __name__ == '__main__':
    typer.run(main)
