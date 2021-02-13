---
title: md2pdf
titlepage: true
subtitle: Creating PDF from markdown
toc: true
author: Manfred Lotz
date: 2021-02-14
...


# Overview



Variable and metadata settings


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

Command line overwrites both 

- environment variable settings, and
- metadata settings in the document
