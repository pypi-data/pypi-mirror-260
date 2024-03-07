
# Table of Contents

1.  [How does it work?](#orgca6e186)
2.  [Installing](#org0063954)
    1.  [Docker](#org86f814e)
    2.  [From Package](#orgbd751af)
    3.  [From Source](#org61126e1)
3.  [Usage](#org9b49e92)
    1.  [Folder Structure](#org2f5dcc4)
    2.  [Tangle](#orgd036c9e)
    3.  [Detangle](#org55ce117)
    4.  [Execute](#orgd25be73)
    5.  [Monitor](#org4689778)
4.  [Tangling Workflows](#org3e076b5)
5.  [Contributions](#org6084e8b)

`orgweb` is intended for developers that want to create literate programming
project using Org-mode, but that **does not** want to investing time to learn how
to use Emacs and Org-mode. If you are a developer that already uses Emacs and
Org-mode, this tool is most likely not for you, but maybe for the people on your
team that doesn't know, nor want to know, about Emacs.

`orgweb` is a very simple CLI tool that does the following:

1.  `tangle` one or multiple Org files
2.  `detangle` one or multiple source files
3.  `execute` one or multiple Org files
4.  `monitor` file changes on the file system to automatically `tangle` and
    `detangle` files that changes.

[What is Literate Programming? Why?](https://fgiasson.com/blog/index.php/2023/08/28/what-is-literate-programming-why/)

If you wonder what a Literate Programming project looks like, just poke around
this repository to have a glimps of the potential.


<a id="orgca6e186"></a>

# How does it work?

`orgweb` is designed in a way that developers can use all the power of Org-mode,
in any IDE they like, without having to rely on Emacs directly.

To do that, it leverages Docker to build an image where Emacs is properly
installed and configured to implement the commands that are exposed via the
command line tool.

If the `orgweb` docker image is not currently existing in the environment, then
it will request Docker to build the image using the Dockerfile. The build
process will install and configure all the components required to implement all
`orgweb` commands.

`orgweb` check if it exists every time it is invoked from the command line. This
process will happen any time that the image is not available in the environment.

![img](imgs/orgweb.svg)

If the image is existing in the environment, then the following will happen.

`orgweb` will ask Docker to create a container based on the image. Once the
container is running, it will execute a command on the container's terminal to
run Emacs. Emacs is used directly from the command line by evaluating ELisp code
it gets as input.

Every time a `orgweb` command line is executed, a new container is created:

![img](imgs/orgweb_2.svg)


<a id="org0063954"></a>

# Installing


<a id="org86f814e"></a>

## Docker

If Docker is already installed in your development environment, you can skip
this step. Otherwise, you should install Docker.

[To install Docker Desktop, you simply have read and follow those instructions.](https://docs.docker.com/desktop/)


<a id="orgbd751af"></a>

## From Package

`orgweb` is available on PyPi, you can easily install it locally by running the
following command in your terminal:

    pip install orgweb


<a id="org61126e1"></a>

## From Source

If you want to improve and contribute to the project, you will first have to
generate the sources files from the Org mode files in the repository. To do so,
you will need `orgweb` itself (installed in the previous step), or you could do
the same if you have a local Emacs instance configured with `org-mode`. But
let's assumes you don't.

First clone the repository in your environment:

    git clone https://github.com/fgiasson/orgweb.git

Once the repository is cloned, let's tangle all the files:

    cd orgweb
    orgweb tangle .

These commands will tangle all the sources and configuration files required by
the project.

Once they have been tangle, you will be able to use make to create the
development environment and the package to run locally.

    make create-venv          # create the pyenv virtual environment
    make install-build        # install Python's build
    source .venv/bin/activate # source that environment
    make build                # build the orgweb CLI application
    make install-local-build  # install the package we just created

After that, you will be able to run `make rebuid-local` every time you want to
test some changes you made to the application.


<a id="org9b49e92"></a>

# Usage


<a id="org2f5dcc4"></a>

## Folder Structure

Each of the operation work with the same folder structure assumption. There are three main components:

1.  folder
2.  files

The `folder` is a where the `files` are located, within the `project folder`.

The `files` is a list of one or multiple files we want to tangle.


<a id="orgd036c9e"></a>

## Tangle

`orgweb tangle` takes a `folder` as input. The `folder` is where the Org files
we want to tangle are located. The operation is recursive, it will check in all
subfolders of `folder`

Optionally, one or multiple files can be listed. Those files are located in
`folder`, and those are the ones that will be tangled from that folder.

If no file is mentioned, then all the Org files from `folder` will be tangled.

    
    cd /my/project/folder/
    orgweb tangle . --file=foo.org --file=bar.org

In that example, `orgweb` will tangle the two files `/my/project/folder/foo.org`
and `/my/project/folder/bar.org`


<a id="org55ce117"></a>

## Detangle

`orgweb detangle` takes a `folder` as input. The `folder` is where the source
files we want to detangle are located. The operation is recursive, it will check in all
subfolders of `folder`

Optionally, one or multiple files can be listed. Those files are located in
`folder`, and those are the ones that will be detangled from that folder.

If no file is mentioned, then all the Org files from `folder` will be detangled.

The `detangle` command does make sure that an input source file is a file that
was previously tangled. Otherwise, it will be ignored. It does so by checking
the tangling markup in comments of the source file.

    
    cd /my/project/folder/
    orgweb detangle . --file=foo.py --file=bar.py

In that example, `orgweb` will detangle the two files
`/my/project/folder/foo.py` and `/my/project/folder/bar.py`


<a id="orgd25be73"></a>

## Execute

`orgweb execute` takes a `folder` as input. The `folder` is where the Org files
we want to execute are located. The operation is recursive, it will check in all
subfolders of `folder`

Optionally, one or multiple files can be listed. Those files are located in
`folder`, and those are the ones that will be executed from that folder.

If no file is mentioned, then all the Org files from `folder` will be executed.

The `execute` command is used to execute every code block or the Org files. This
is normally used to execute PlantUML code blocks such that it produces graphs
that are referrenced within Org files.

    
    cd /my/project/folder/
    orgweb execute . --file=foo.org

In that example, `orgweb` will execute the `/my/project/folder/foo.py`


<a id="org4689778"></a>

## Monitor

`orgweb monitor` will take a folder as input and will monitor every file changes
in that directory, recursively. If a Org file changes, it will be tangled, if a
source file changes it will be detangled.

Monitoring is used to make sure that the Org files and their source files are
always in sync, without having the developers to carefully tangle and detangle
every time they modify a file.

    
    cd /my/project/folder/
    orgweb monitor .


<a id="org3e076b5"></a>

# Tangling Workflows

Let's take some time to cover the different tangling workflows that you may
imagine.

The first scenario is when you have a single Org file that tangles code blocks
in one, or multiple, source files, such as:

![img](imgs/graph.svg)

This is the workflow that is currently implemented in Org-mode. You can tangle a
`foo.org` file in as many source files you want. Then, if you just detangle
`Foo.py`, then only the code blocks with that code will be updated in `Foo.org`.

Then you could extrapolite this case and think about the following scenario:

![img](imgs/graph_2.svg)

This scenario is when you have two different Org files that tangle in the same
source file. Then, when you detangle `FooBar.py`, you would imagine that each
blocks would detangle in their respective Org file.

However, this is not currently the case with Org mode. **This scenario is
currently not supported and will break your literate programming workkflow**.

Another thing to take care of is that the [noweb syntax is not currently
supported for the detangle command](https://orgmode.org/manual/Noweb-Reference-Syntax.html). This is a long standing issue with
Org-mode that is discussed for several years now.

You can use `noweb` only if you won't `detangle` your source files. 


<a id="org6084e8b"></a>

# Contributions

We welcome contributions to OrgWeb! If you’d like to contribute, please follow
these steps:

1.  Fork the repository on GitHub.
2.  Create a new branch with a descriptive name: `git checkout -b
         feature/your-feature-name`
3.  Push your changes to your fork: `git push origin feature/your-feature-name`
4.  Make your changes and commit them: =git commit -m "Add feature: your
    feature name"​=
5.  Submit a pull request to the main branch of the original repository.
6.  Make sure that you only commit the Org-mode files, and not the source files
    themselves. Add them to the `make clean` method if needed.

