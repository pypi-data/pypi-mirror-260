import logging

from .patches import InsertDataPatch, ModifyDataPatch, RemoveDataPatch
from .targets import Target

logger = logging.getLogger(__name__)


class Patcherex:
    def __init__(
        self, binary_path, target_cls=None, target_opts=None, components_opts=None
    ):
        if target_opts is None:
            target_opts = {}
        if components_opts is None:
            components_opts = {}
        self.binary_path = binary_path
        if target_cls is None:
            self.target = Target.detect_target(self, binary_path)
        else:
            self.target = target_cls(self, binary_path)

        self.symbols = {}
        self.sypy_info = {"patcherex_added_functions": []}
        self.patches = []

        # Initialize components
        components = [
            "assembler",
            "disassembler",
            "compiler",
            "binary_analyzer",
            "allocation_manager",
            "binfmt_tool",
            "utils",
            "archinfo",
        ]
        for component in components:
            setattr(
                self,
                component,
                self.target.get_component(
                    component,
                    target_opts.get(component),
                    components_opts.get(component),
                ),
            )

    def apply_patches(self):
        # TODO: sort patches properly
        self.patches.sort(
            key=lambda x: not isinstance(
                x, (ModifyDataPatch, InsertDataPatch, RemoveDataPatch)
            )
        )
        logger.debug(f"Applying patches: {self.patches}")
        for patch in self.patches:
            patch.apply(self)
        self.binfmt_tool.finalize()

    def save_binary(self, filename=None):
        logger.warning(
            "p.save_binary() is deprecated, use p.binfmt_tool.save_binary() instead."
        )
        self.binfmt_tool.save_binary(filename)
