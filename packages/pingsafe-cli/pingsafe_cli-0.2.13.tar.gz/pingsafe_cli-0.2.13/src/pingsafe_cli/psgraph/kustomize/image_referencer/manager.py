from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pingsafe_cli.psgraph.common.images.graph.image_referencer_manager import GraphImageReferencerManager
from pingsafe_cli.psgraph.kustomize.image_referencer.provider.kustomize import KustomizeProvider

if TYPE_CHECKING:
    from pingsafe_cli.psgraph.common.images.image_referencer import Image
    from networkx import DiGraph


class KustomizeImageReferencerManager(GraphImageReferencerManager):

    def __init__(self, graph_connector: DiGraph, report_mutator_data: dict[str, dict[str, Any]]):
        super().__init__(graph_connector)
        self.report_mutator_data = report_mutator_data

    def extract_images_from_resources(self) -> list[Image]:
        kustomize_provider = KustomizeProvider(graph_connector=self.graph_connector, report_mutator_data=self.report_mutator_data)
        images = kustomize_provider.extract_images_from_resources()

        return images
