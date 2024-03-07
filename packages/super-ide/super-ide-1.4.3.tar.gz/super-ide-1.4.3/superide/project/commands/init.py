# Copyright (c) Mengning Software. 2023. All rights reserved.
#
# Super IDE licensed under GNU Affero General Public License v3 (AGPL-3.0) .
# You can use this software according to the terms and conditions of the AGPL-3.0.
# You may obtain a copy of AGPL-3.0 at:
#
#    https://www.gnu.org/licenses/agpl-3.0.txt
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR
# PURPOSE.
# See the AGPL-3.0 for more details.

# pylint: disable=line-too-long,too-many-arguments,too-many-locals


import json
import os
import shutil

    
import click

from superide import __configfile__
from superide import fs
from superide.registry.cli import install_project_dependencies
# from superide.package.manager.platform import PlatformPackageManager
# from superide.platform.exception import UnknownBoard
# from superide.platform.factory import PlatformFactory
from superide.project.config import ProjectConfig
from superide.project.exception import UndefinedEnvPlatformError
from superide.project.helpers import is_platformio_project
# from superide.project.integration.generator import ProjectGenerator
from superide.project.options import ProjectOptions
from superide.project.vcsclient import VCSClientFactory

def validate_boards(ctx, param, value):  # pylint: disable=unused-argument
    # pm = PlatformPackageManager()
    # for id_ in value:
    #     try:
    #         pm.board_config(id_)
    #     except UnknownBoard as exc:
    #         raise click.BadParameter(
    #             "`%s`. Please search for board ID using `superide boards` "
    #             "command" % id_
    #         ) from exc
    return value


@click.command("init", short_help="Initialize a project or update existing")
@click.option(
    "--project-dir",
    "-d",
    default=os.getcwd,
    type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True),
)
@click.option("-e", "--environment", help="Update existing environment")
@click.option(
    "-O",
    "--project-option",
    "project_options",
    multiple=True,
    help="A `name=value` pair",
)
@click.option("--sample-code", default="")
@click.option("--no-install-dependencies", is_flag=True)
@click.option("--env-prefix", default="")
@click.option("-s", "--silent", is_flag=True)
def project_init_cmd(
    project_dir,
    environment,
    project_options,
    sample_code,
    no_install_dependencies,
    env_prefix,
    silent,
):
    # 用于判断当前目录或project_dir指定的目录下有没有配置文件即__configfile__所代表的ini文件
    is_new_project = not is_platformio_project(project_dir)
    if is_new_project:
        if not silent:
            print_header(project_dir)
        # 初始化项目，增加配置文件以及include、lib、src目录等
        # 但是这个目录结构的通用性存疑？
        init_base_project(project_dir)

    with fs.cd(project_dir):
        if environment:
            # 在配置文件添加[env:ENV_NAME]及key=value
            update_project_env(environment, project_options)

        config = ProjectConfig.get_instance(os.path.join(project_dir, __configfile__))

        # resolve project dependencies
        if not no_install_dependencies and (environment):
            install_project_dependencies(
                options=dict(
                    project_dir=project_dir,
                    environments=[environment] if environment else [],
                    silent=silent,
                )
            )

        if sample_code:
            init_sample_code(config, environment, sample_code)

        if is_new_project:
            init_cvs_ignore()

    if not silent:
        print_footer(is_new_project)


def print_header(project_dir):
    click.echo("The following files/directories have been created in ", nl=False)
    try:
        click.secho(project_dir, fg="cyan")
    except UnicodeEncodeError:
        click.secho(json.dumps(project_dir), fg="cyan")
    click.echo("%s - Put project header files here" % click.style("include", fg="cyan"))
    click.echo(
        "%s - Put project specific (private) libraries here"
        % click.style("lib", fg="cyan")
    )
    click.echo("%s - Put project source files here" % click.style("src", fg="cyan"))
    click.echo(
        "%s - Project Configuration File" % click.style(__configfile__, fg="cyan")
    )


def print_footer(is_new_project):
    action = "initialized" if is_new_project else "updated"
    return click.secho(
        f"Project has been successfully {action}!",
        fg="green",
    )


def init_base_project(project_dir):
    with fs.cd(project_dir):
        config = ProjectConfig()
        config.save()
        dir_to_readme = [
            (config.get("superide", "src_dir"), None),
            (config.get("superide", "include_dir"), init_include_readme),
            (config.get("superide", "lib_dir"), init_lib_readme),
            (config.get("superide", "test_dir"), init_test_readme),
        ]
        for path, cb in dir_to_readme:
            if os.path.isdir(path):
                continue
            os.makedirs(path)
            if cb:
                cb(path)


def init_include_readme(include_dir):
    with open(os.path.join(include_dir, "README"), mode="w", encoding="utf8") as fp:
        fp.write(
            """
This directory is intended for project header files.

A header file is a file containing C declarations and macro definitions
to be shared between several project source files. You request the use of a
header file in your project source file (C, C++, etc) located in `src` folder
by including it, with the C preprocessing directive `#include'.

```src/main.c

#include "header.h"

int main (void)
{
 ...
}
```

Including a header file produces the same results as copying the header file
into each source file that needs it. Such copying would be time-consuming
and error-prone. With a header file, the related declarations appear
in only one place. If they need to be changed, they can be changed in one
place, and programs that include the header file will automatically use the
new version when next recompiled. The header file eliminates the labor of
finding and changing all the copies as well as the risk that a failure to
find one copy will result in inconsistencies within a program.

In C, the usual convention is to give header files names that end with `.h'.
It is most portable to use only letters, digits, dashes, and underscores in
header file names, and at most one dot.

Read more about using header files in official GCC documentation:

* Include Syntax
* Include Operation
* Once-Only Headers
* Computed Includes

https://gcc.gnu.org/onlinedocs/cpp/Header-Files.html
""",
        )


def init_lib_readme(lib_dir):
    with open(os.path.join(lib_dir, "README"), mode="w", encoding="utf8") as fp:
        fp.write(
            """
This directory is intended for project specific (private) libraries.
superide will compile them to static libraries and link into executable file.

The source code of each library should be placed in a an own separate directory
("lib/your_library_name/[here are source files]").

For example, see a structure of the following two libraries `Foo` and `Bar`:

|--lib
|  |
|  |--Bar
|  |  |--docs
|  |  |--examples
|  |  |--src
|  |     |- Bar.c
|  |     |- Bar.h
|  |  |- library.json (optional, custom build options, etc) https://docs.superide.org/page/librarymanager/config.html
|  |
|  |--Foo
|  |  |- Foo.c
|  |  |- Foo.h
|  |
|  |- README --> THIS FILE
|
|- platformio.ini
|--src
   |- main.c

and a contents of `src/main.c`:
```
#include <Foo.h>
#include <Bar.h>

int main (void)
{
  ...
}

```

superide Library Dependency Finder will find automatically dependent
libraries scanning project source files.

More information about superide Library Dependency Finder
- https://docs.superide.org/page/librarymanager/ldf.html
""",
        )


def init_test_readme(test_dir):
    with open(os.path.join(test_dir, "README"), mode="w", encoding="utf8") as fp:
        fp.write(
            """
This directory is intended for superide Test Runner and project tests.

Unit Testing is a software testing method by which individual units of
source code, sets of one or more MCU program modules together with associated
control data, usage procedures, and operating procedures, are tested to
determine whether they are fit for use. Unit testing finds problems early
in the development cycle.

More information about superide Unit Testing:
- https://docs.superide.org/en/latest/advanced/unit-testing/index.html
""",
        )


def init_cvs_ignore():
    conf_path = ".gitignore"
    if os.path.isfile(conf_path):
        return
    with open(conf_path, mode="w", encoding="utf8") as fp:
        fp.write(".pio\n")

def update_project_env(environment, extra_project_options=None):
    if not extra_project_options:
        return
    env_section = "env:%s" % environment
    # 保持与platformio兼容
    option_to_sections = {"platformio": [], env_section: []}
    for item in extra_project_options:
        assert "=" in item
        name, value = item.split("=", 1)
        name = name.strip()
        destination = env_section
        for option in ProjectOptions.values():
            if option.scope in option_to_sections and option.name == name:
                destination = option.scope
                break
        option_to_sections[destination].append((name, value.strip()))

    config = ProjectConfig(
        __configfile__, parse_extra=False, expand_interpolations=False
    )
    for section, options in option_to_sections.items():
        if not options:
            continue
        if not config.has_section(section):
            config.add_section(section)
        for name, value in options:
            config.set(section, name, value)

    config.save()


def init_sample_code(config, environment, sample_code):
    # try:
    #     p = PlatformFactory.from_env(environment)
    #     return p.generate_sample_code(config, environment)
    # except (NotImplementedError, UndefinedEnvPlatformError):
    #     pass
    if sample_code!="":
        src_dir = config.get("superide", "src_dir")
        if os.listdir(src_dir):
            shutil.rmtree(src_dir)
            os.makedirs(src_dir)
        vcs = VCSClientFactory.new(src_dir, sample_code)
        assert vcs.export()
        return True
    framework = config.get(f"env:{environment}", "framework", None)
    if framework != ["arduino"]:
        return None
    main_content = """
#include <Arduino.h>

// put function declarations here:
int myFunction(int, int);

void setup() {
  // put your setup code here, to run once:
  int result = myFunction(2, 3);
}

void loop() {
  // put your main code here, to run repeatedly:
}

// put function definitions here:
int myFunction(int x, int y) {
  return x + y;
}
"""
    is_cpp_project = p.name not in ["intel_mcs51", "ststm8"]
    src_dir = config.get("superide", "src_dir")
    main_path = os.path.join(src_dir, "main.%s" % ("cpp" if is_cpp_project else "c"))
    if os.path.isfile(main_path):
        return None
    if not os.path.isdir(src_dir):
        os.makedirs(src_dir)
    with open(main_path, mode="w", encoding="utf8") as fp:
        fp.write(main_content.strip())
    return True
