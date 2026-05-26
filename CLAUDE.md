# DZX Filter POE2 Project Guidelines

This file provides quick reference commands and guidelines for AI agents working on this project.

## Build Commands

- **Build Main Filters**: `python script/start_build.py`
- **Build CSS Components**: `python script/build_css.py`
- **Build HTML Preview**: `python script/build_html.py`
- **Merge Filter Groups**: `python script/merge_file.py`

## Release Process

- **Create a Local Release**: `python -X utf8 script/create_release.py`
  *(Note: This builds filters, compiles the Windows EXE launcher, tags git, and publishes to GitHub releases.)*

## Test Commands

- **Run Pytest Suite**: `python -m pytest tests/`
- **Test Build Process**: `python script/test_build.py`

## Code Style Guidelines

- **Python**: Use PEP 8, type hints, descriptive naming conventions, and write clean docstrings.
- **HTML/CSS**: Use semantic HTML, layout via Flexbox/Grid, and responsive custom CSS properties.
- **Filters**: Follow consistent naming conventions, group rules logically by item type, and add comments for complex filters.
