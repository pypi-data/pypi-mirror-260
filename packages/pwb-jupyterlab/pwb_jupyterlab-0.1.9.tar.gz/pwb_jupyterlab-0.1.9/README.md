# pwb_jupyterlab

<!--- 

===============
Developer Note: 
===============

This is the public-facing README that is displayed on the extension's PyPI page.

Keep this content relevant to end-users. Developer-related content should go in ../README.md

--->

The `pwb_jupyterlab` JupyterLab plugin provides features for integrating JupyterLab 4.x with Posit Workbench. 

Note: Using JupyterLab 3.x? You'll want to install the legacy `workbench_jupyterlab` extension instead. This `pwb_jupyterlab` extension is for Posit Workbench with JupyterLab 4.x only.

## Features

* Provides a button on the main toolbar that will bring the user to the Posit Workbench homepage
* Provides the command "Return to Posit Workbench Home" that can be accessed through the Command Palette to bring the user to the Posit Workbench homepage.
* Provides a "Proxied Servers" sidebar view that allows users to access their remote servers from Posit Workbench environments.
* Provide popup alert when the JupyterLab session has lost connection to Workbench, usually indicating expired login credentials.

## Requirements

* JupyterLab == 4.x

## Install

To install the extension, execute:

```bash
pip install pwb_jupyterlab
```

## Uninstall

To remove the extension, execute:

```bash
pip uninstall pwb_jupyterlab
```
