"""Pylint module: Automate code reviews and complying with quality standards."""

import re
from astroid.nodes import NodeNG, Module, Import, ImportFrom
from pylint.checkers import BaseChecker
from pylint.lint import PyLinter


class ImportRestriction(BaseChecker):
    """
    A pylint plugin to help automate code reviews and complying with quality standards.

    Attributes:
        name: The name of this plugin.
        priority: The priority of this plugin.
        msgs: The Pylint error messages triggered by this plugin.
        options: The Pylint configuration options for this plugin.
        _current_module: The current host module being checked.
        _restrictions: The parsed module restrictions supplied through plugin
            configuration.
    """

    name = "comply"
    priority = -1
    msgs = {
        "E7101": (
            'Module "%s" is not allowed to be imported from "%s"',
            "import-restriction",
            "Only allowed modules can be imported.",
        )
    }
    options = (
        (
            "import-restriction",
            {
                "type": "string",
                "help": "A comma separated list specifying restrictions per module. "
                "Both module and restriction specification can be a regex.",
                "metavar": "<regex module -> regex restriction; regex module -> ...>",
                "default": "",
            },
        ),
    )
    _current_module: str = ""
    _restrictions: list[tuple[re.Pattern, re.Pattern]] = []

    def open(self) -> None:
        """
        Called when this plugin is being called to perform checking
        (after initialization).
        """
        # Parse and prepare the plugin configuration
        for pair in self.linter.config.import_restriction.split(",") or []:
            restrictions = pair.split("->")
            if len(restrictions) == 2:
                self._restrictions.append(
                    (
                        re.compile(restrictions[0].strip()),
                        re.compile(restrictions[1].strip()),
                    )
                )

    def visit_module(self, node: Module) -> None:
        """
        Called the first time when the host module check begins.

        Args:
            node: The current node being checked.
        """
        self._current_module = node.name

    def visit_import(self, node: Import) -> None:
        """
        Called if an `import ...` is detected in the host module being checked.

        Args:
            node: The current node being checked.
        """
        for name, _ in node.names:
            self._check_module(node, name)

    def visit_importfrom(self, node: ImportFrom) -> None:
        """
        Called if an `from ... import ...` is detected in the host module being checked.

        Args:
            node: The current node being checked.
        """
        if node.level is None:
            mod_name = node.modname
        else:
            mod_name = "." * node.level + node.modname

        for name, _ in node.names:
            self._check_module(node, f"{mod_name}.{name}")

    def _check_module(self, node: NodeNG, import_module: str) -> None:
        """
        Check if the imported module is restricted within the host module being checked.

        Args:
            node: The current node being checked.
            import_module: The module being imported.
        """
        import_module = self._normalize_module(import_module)
        for host, restriction in self._restrictions:
            # Check if the current module has restrictions
            if not re.match(host, self._current_module):
                continue

            # The current module has restrictions
            # now check if any of its import should not be performed
            if re.match(restriction, import_module):
                self.add_message(
                    "import-restriction",
                    node=node,
                    args=(import_module, self._current_module),
                )

    def _normalize_module(self, import_module: str) -> str:
        """
        Normalize the module by constructing its full qualified name. This is
        especially useful for relative imports.

        Args:
            import_module: The module being imported.

        Returns:
            A fully qualified name for the module being imported.
        """
        levels = self._current_module.split(".")
        relative_levels = len(import_module) - len(import_module.lstrip("."))
        if relative_levels > 0:
            return (
                ".".join(levels[: len(levels) - relative_levels])
                + "."
                + import_module.lstrip(".")
            )

        return import_module


def register(linter: PyLinter) -> None:
    """
    This function is required to register the plugin during initialization.

    Args:
        linter: The linter to register the plugin to
    """
    linter.register_checker(ImportRestriction(linter))
