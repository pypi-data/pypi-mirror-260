"""Compiler module
"""

import json
import os
import shutil
import copy
from pathlib import Path
from typing import Optional, Tuple
import click
from jinja2 import Environment, FileSystemLoader
from codectl import utils
from codectl import jinja


def _load_associated_schema(tmpl_path: Path) -> Tuple[dict, Path]:
    """Load the associated JSON schema for a given template file.

    Args:
        tmpl_path (Path): The path to the template file.

    Returns:
        dict: A dictionary representing the loaded JSON schema.
    """
    schema_path = tmpl_path.with_suffix(".schema")
    schema = json.loads(schema_path.read_text()) if schema_path.is_file() else {}
    return schema, schema_path


def _get_output_dir(tmpl_path: Path, tmpl_root_dir: Path, output: Path) -> Path:
    """Determine the output directory for the rendered template based on the template path,
    template directory.

    Args:
        tmpl_path (Path): The path to the template file.
        tmpl_dir (Path): The root directory of the template files.

    Returns:
        Path: The path to the output directory.
    """
    rel_path = tmpl_path.parent.relative_to(tmpl_root_dir)
    return output / rel_path


def _copy_file(source: Path, dest: Path):
    """Copy a file from the source path to the destination path.

    Args:
        source (Path): The path to the source file.
        dest (Path): The path to the destination file.
    """
    if source == dest:
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(source, dest)


def process_file(
    env: Environment,
    loader: FileSystemLoader,
    tmpl_path: Path,
    schemas: dict,
    output: Path,
):
    """Process a single file template, render it with the provided schemas,
    and save the output to the designated directory.

    Args:
        env (Environment): The Jinja2 environment.
        loader (FileSystemLoader): The Jinja2 loader.
        tmpl_path (Path): The path to the template file.
        schemas (dict): A dictionary containing data to be used in the template rendering.
    """
    schema, schema_path = _load_associated_schema(tmpl_path)
    schemas.update(schema)

    searchpath = loader.searchpath[0]
    searchpath = Path(searchpath)
    tmpl_fullname = tmpl_path.relative_to(searchpath)
    tmpl = env.get_template(str(tmpl_fullname))
    content = tmpl.render(**schemas)

    output_dir = _get_output_dir(tmpl_path, searchpath, output)

    tmpl_ = jinja.create_string_template(tmpl_path.stem)
    filename = tmpl_.render(schemas)
    filepath = output_dir / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)

    update = schemas.get("_update", False)
    if filepath.is_file() and not update:
        click.secho(
            f"The {filepath.relative_to(output_dir)} file already exists and will be ignored.",
            fg="green",
        )
        return
    filepath.write_text(content)
    _copy_file(tmpl_path, output_dir / tmpl_path.name)
    if schema_path.is_file():
        _copy_file(schema_path, output_dir / schema_path.name)


def process_files_with_iterator(
    env: Environment,
    loader: FileSystemLoader,
    tmpl_path: Path,
    schemas: dict,
    output: Path,
):
    """Process files with an iterator, rendering each element with the template and
    saving the outputs to the designated directory.

    Args:
        env (Environment): The Jinja2 environment.
        loader (FileSystemLoader): The Jinja2 loader.
        tmpl_path (Path): The path to the template file.
        schemas (dict): A dictionary containing data to be used in the template rendering.
    """
    schema, schema_path = _load_associated_schema(tmpl_path)
    schemas.update(schema)

    searchpath = loader.searchpath[0]
    searchpath = Path(searchpath)
    tmpl_fullname = tmpl_path.relative_to(searchpath)
    tmpl = env.get_template(str(tmpl_fullname))

    output_dir = _get_output_dir(tmpl_path, searchpath, output)

    iter_key = schemas["_iter"]
    elements = utils.retrieve_nested_value(schemas, iter_key) or []

    iter_filter_ = schemas.get("_iter_filter")
    if iter_filter_:
        elements = env.filters[iter_filter_](elements)

    update = schemas.get("_update", False)
    for elem in elements:
        schema = {"_": elem, **schemas}
        content = tmpl.render(schema)
        tmpl_ = jinja.create_string_template(tmpl_path.stem)
        filename = tmpl_.render(schema)
        filepath = output_dir / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)

        if filepath.is_file() and not update:
            click.secho(
                f"The {filepath.relative_to(output_dir)} file already exists and will be ignored.",
                fg="green",
            )
            continue
        filepath.write_text(content)

    _copy_file(tmpl_path, output_dir / tmpl_path.name)
    if schema_path.is_file():
        _copy_file(schema_path, output_dir / schema_path.name)


def process_directory(tmpl_root_dir: Path, output: Path, schemas: dict = {}):
    """Process a directory of templates, including single file templates,
    multi-file templates with iterators, and static files.

    Args:
        tmpl_dir (Path): The path to the directory containing the template files.
        schemas (dict): A dictionary containing global data to be used across all templates.
    """
    env, loader = jinja.create_filesys_env(tmpl_root_dir)

    schema_name = "_data.schema"
    schemas_path = tmpl_root_dir / schema_name
    if schemas_path.is_file():
        schema = json.loads(schemas_path.read_text())
        schemas.update(schema)
        schemas_path.write_text(json.dumps(schemas, indent=2, ensure_ascii=False))
        _copy_file(schemas_path, output / schema_name)

    env.globals.update(schemas)

    module = tmpl_root_dir / "_filter.py"
    if module.is_file():
        for name, function in utils.load_priv_funcs_from_mod(module):
            env.filters[name[1:]] = function
        _copy_file(module, output / module.name)

    module = tmpl_root_dir / "_handle.py"
    if module.is_file():
        for name, function in utils.load_priv_funcs_from_mod(module):
            env.globals[name[2:]] = function
        _copy_file(module, output / module.name)

    for root, _, files in os.walk(tmpl_root_dir):
        root = Path(root)

        for file in files:
            file = root / file
            if file.suffix == ".tpl":
                process_file(env, loader, file, copy.deepcopy(schemas), output)
            elif file.suffix == ".mtpl":
                process_files_with_iterator(
                    env, loader, file, copy.deepcopy(schemas), output
                )
            elif (
                file.name
                not in (
                    "_filter.py",
                    "_handler.py",
                )
                and file.suffix != ".schema"
            ):
                filename = jinja.create_string_template(file.name).render(
                    **copy.deepcopy(schemas)
                )
                dest = _get_output_dir(file, tmpl_root_dir, output) / filename
                _copy_file(file, dest)
