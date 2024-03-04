# pylint-comply
Pylint plugin to help automate code reviews and complying with quality standards.

## Installation
Install the module with e.g. `poetry add --group dev pylint-comply`.

## Usage
In your Pylint configuration (e.g. in `pyproject.toml`) add the following:
```
[tool.pylint.MAIN]
load-plugins = "pylint_comply"
```

### Import restrictions
Once the plugin is enabled, in your Pylint configuration (e.g. in `pyproject.toml`) add the following:
```
[tool.pylint.MAIN]
import-restriction = [
    "module_visited->module_import_restriction",
    "module2_visited -> restriction\\..*"
]
```
The restrictions configured as part of `import-restriction` setting, and as represented above take the following shape - `module_visited -> import_restriction`
- `module_visited`: The module which is presently being looked at. This could be a RegEx in order to capture several modules.
- `->`: The separator denoting the module being investigated (on the left), and the restricted imports (on the right). You can optionally add spaces around it for clarity.
- `import_restriction`: The module which is restricted from being imported within the module being investigated. This could be a RegEx in order to capture several modules.
