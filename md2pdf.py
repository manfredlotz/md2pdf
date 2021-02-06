#!/usr/bin/env python3

"""
Convert a markdown file to pdf or (if requested) create a tex file

Configuration is in either
- `$HOME/.md2pdf.toml`
- `$HOME/.config/md2pdf/config.toml`

One of those must exist.

"""

import os
import sys
import subprocess

import toml
from pathlib import Path
from typing import List, Dict, Optional
from pydantic import BaseModel
from enum import Enum, auto

import re
import typer

from datetime import date


__version__ = "1.1.1"

class Severity(Enum):
     OK = auto()
     WARN = auto()
     ERROR = auto()
     FATAL = auto()

class Md2pdfResponse(BaseModel):
    status: Severity
    msg: Optional[str]

    def to_dict(self):
        return {
            "status": self.status,
            "msg": msg,
        }

    @staticmethod
    def from_dict(response):
        return Md2pdfResponse(
            status=response['status'],
            msg=response['msg'],
        )

def version_callback(value: bool) -> None:
    if value:
        typer.echo(f"md2pdf Version: {__version__}")
        raise typer.Exit()

def print_error(msg):
    print(msg)
    print('Exiting with errors...')
    sys.exit(1)

def find_config() -> str:
    """Find name of config file

    Either given by
    - given by setting of environ variable `MD2PDF_CONFIG`, or
    - or `$HOME/.md2pdf.toml`
    - or `$HOME/.config/md2pdf/config.toml`
    """

    if config := os.environ.get('MD2PDF_CONFIG'):
        if not os.path.isfile(config):
            return Md2pdfResponse(status=Severity.FATAL, msg=f"Config file {config} doesn't exist")
        return Md2pdfResponse(status=Severity.OK, msg=config)

    config = f'{home}/.md2pdf.toml'
    if os.path.isfile(config):
        return Md2pdfResponse(status=Severity.OK, msg=config)

    config = f'{home}/.config/md2pdf/config.toml'
    if os.path.isfile(config):
        return Md2pdfResponse(status=Severity.OK, msg=config)

    return Md2pdfResponse(status=Severity.FATAL, msg="No config file found")

class Config(BaseModel):
    template: str
    email: str
    name: str

def read_config(config_file: str) -> Dict[str,str]:
    global toml
    toml = toml.load(config_file)
    return toml


def main(files: List[Path] = typer.Argument(default=None, dir_okay=False, exists=True),
         config_section: str = typer.Option(None, '-s', '--section', help='Section in TOML config to use'),
         no_toc: bool = typer.Option(False, '--no-toc', help='table of contents in PDF document'),
         no_title: bool = typer.Option(False, '--no-title', help='title in PDF document'),
         tex_file: bool = typer.Option(False, '--tex', help='create TeX file instead of PDF document'),
         gsd: bool = typer.Option(False, '--gsd', help='indicate `GSD Platform Services`'),
         ibm_confidential: bool = typer.Option(False, '--ibm-confidential', help='indicate `IBM confidential` document'),
         ibm: bool = typer.Option(False, '--ibm', help='indicate IBM document'),
         debug: bool = typer.Option(False, '--debug', help='turns debugging on'),
         pdf_engine: str = typer.Option('xelatex', '--pdf-engine',
                                        help='Specify pdf engine, one of lualatex, xelatex or tectonic '),
         version: bool = typer.Option(None, '-V', "--version", callback=version_callback, help='Show version and exit'),
):

    if not files:
        typer.echo("Error: Must specify at least one .md file.")
        raise typer.Abort()

    mdfiles: List[str] = [str(md) for md in files]



    rc = find_config()
    if rc.status == Severity.FATAL:
        print_error(rc.msg)

    config = rc.msg
    print(read_config(config))


    home = os.environ['HOME']

    template = os.environ.get('MD2PDF_TEMPLATE') or home + "/dotfiles/pandoc/eisvogel.tex"
    print(f'template: {template}')
    email = os.environ.get('MD2PDF_EMAIL') or 'manfred.lotz@posteo.de'
    footer_center = ''

    # check correct pdf-engine
    if not pdf_engine in ['xelatex', 'lualatex', 'tectonic']:
        print('--pdf-engine must be one of "xelatex", "lualatex", "tectonic"')
        sys.exit(1)

    ext = ".pdf"
    if tex_file:
        ext = ".tex"


    if len(mdfiles) == 1:
        toml_file = os.path.splitext(mdfiles[0])[0] + '.toml'

        if os.path.exists(toml_file):
            print(f"TOML file {toml_file} found")
            parsed_toml = toml.load(toml_file)
            default_val = parsed_toml.get('default')
            if default_val is None:
                print(f'No file names found in {toml_file}')
            else:
                mdfiles = default_val.get('files')

    for mdf in mdfiles:
        print(f'Compiling {mdf}')


    # we want to check if we are in the `vimwiki_work` directory tree
    vimwiki_work = False
    main_mdfile = os.path.realpath(mdfiles[0])
    if re.search(r'/vimwiki_work', main_mdfile):
        vimwiki_work = True

    outfile = Path(main_mdfile).stem + ext

    if ibm:
        email = os.environ.get('MD2PDF_EMAIL_IBM') or '<manfred.lotz@de.ibm.com>'
        year = date.today().year
        if ibm_confidential:
            footer_center = f'© {year} IBM Confidential'
        else:
            footer_center = f'{year} IBM Corporation'
        if gsd:
            footer_center = 'GSD Platform Services'

    pandoc = [ 'pandoc' ] + mdfiles + [
        "-o", outfile,
        '-f', 'markdown+smart',
        "--number-sections",
        '-M', 'colorlinks=true',
        '-V', 'linkcolor=ForestGreen',
        '-V', 'classoption=oneside',
        '-V', "listings",
        '-V', "footer-center=" + footer_center,
#        '-V', "footer-center=" + email,
#        '-V', "footer-left=" + footer_left,
        '-M', 'toc-own-page=true',
        '--template', template,
        '--pdf-engine=' + pdf_engine,
        '--highlight-style', 'pygments', ]

    if no_title:
        pandoc.append('-M')
        pandoc.append('titlepage=false')
    # else:
    #     pandoc.append('-M')
    #     pandoc.append('titlepage=')


#    if vimwiki_work:
    if True:
        pandoc.append('-V')
        pandoc.append("logo=/home/manfred/dotfiles/pandoc/ibmpos_blue.jpg")
        pandoc.append('-V')
        pandoc.append("logo-width=41")

    if not no_toc:
        pandoc.append('--toc')

    if debug:
        print(' '.join(pandoc))


    rc = subprocess.run(pandoc).returncode
    if rc:
        print(f"pandoc error: {rc}")



if __name__ == "__main__":
    typer.run(main)
