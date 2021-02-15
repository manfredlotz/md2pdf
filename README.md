# md2pdf

## Overview

A small Python 3 script to create a PDF document from one or more markdown files.

- using [pandoc](https://pandoc.org/)
- and the pandoc LaTeX template [Eisvogel](https://github.com/Wandmalfarbe/pandoc-latex-template) to
    convert the markdown file(s) to LaTeX
- which I modified for my needs

The main adjustment to the _Eisvogel_ template is the addition of some variables

- `company`: to specify a company name
- `department`: to specify a department name

Another adjustment is to create documents using the IBM Plex fonts. For the time being, this is
simply hardcoded in the modified _Eisvogel_ template.


Basically, I wrote this in my leisure time to create somehow good looking PDF documents in my
company which (perhaps no surprice) is IBM.

## Licence

Dual licensed under the Apache License, Version 2.0 and MIT License.

## Installing

- The `md2pdf` script could be copied to a directory which is in the PATH.
- The Python 3 packages `typer` and `toml` are required. 

## Usage

See [md2pdf.md](md2pdf.md)

## Sample documents

- `test1.md`

Run
```
export MD2PDF_COMPANY="IBM Corporation"
export MD2PDF_DEPARTMENT="My Department"
export MD2PDF_AUTHOR_EMAIL='manfred.lotz@de.ibm.com'
export MD2PDF_LOGO="ibmpos_blue.jpg"
export MD2PDF_TEMPLATE=eisvogel.tex

./md2pdf.py test1.md 
```

- `test2.md`: 

Just run 


```
md2pdf test2.md --template eisvogel.tex --company 'Best Company Ever' --department 'Future Development'
```
