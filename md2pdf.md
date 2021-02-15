---
title: md2pd
titlepage: true
subtitle: Creating PDF from markdown
toc: true
author: Manfred Lotz
date: 2021-02-14
...


# Configuring md2pdf

`md2pdf` can be configured by setting

- environment variables
- commandline arguments, and
- variables in the metadata header in the markdown document

Some of the variables in the metadata header in markdown document can be 
overwritten by command line arguments or environment variables. Commandline
arguments overwrite environment variables.

Here a table of possible configuration values

| Name              | env var               | cmdline var    | metadata     |
| --                | --                    | --             | --           |
| template location | `MD2PDF_TEMPLATE`     | `template`     |              |
| logo location     | `MD2PDF_LOGO`         | `logo`         |              |
| logo width        | `MD2PDF_LOGO_WIDTH`   | `logo-width`   |              |
| author's email    | `MD2PDF_AUTHOR_EMAIL` | `email`        | `email:`     |
| company           | `MD2PDF_COMPANY`      | `company`      |              |
| department        | `MD2PDF_DEPARTMENT`   | `department`   |              |
| pdf engine        | `MD2PDF_PDF_ENGINE`   | `pdf-engine`   |              |
| title             |                       |                | `title:`
| title page        |                       | `no-titlepage` | `titlepage:` |
| subtitle          |                       |                | `subtitle:`
| toc               |                       | `no-toc`       | `toc:`       |
| author            |                       |                | `author:`
| date              |                       |                | `date:`


# Compiling more than a single markdown file


There are basically two ways to compile more than a single markdown file in one run.

1. Specify them when calling `md2pdf`

Example:

```
md2pdf mydoc.md mydoc_chap1.md mydoc_chap2.md
```

Here a `mydoc.pdf` gets created.

2. Specify the files to compile in a TOML file

Example:

```toml
[default]

files = ["mydoc.md", "mydoc_chap.md", "mydoc_chap2.md"]
```

Now run just: `md2pdf mydoc.toml`


