from __future__ import annotations

from typing import Any

from pingsafe_cli.psgraph.common.graph.graph_builder.consts import GraphSource
from pingsafe_cli.psgraph.common.graph.graph_builder.graph_components.blocks import Block


class BicepBlock(Block):
    def __init__(
        self,
        name: str,
        config: dict[str, Any],
        path: str,
        block_type: str,
        attributes: dict[str, Any],
        id: str = "",
    ) -> None:
        super().__init__(name, config, path, block_type, attributes, id, GraphSource.BICEP)
