from __future__ import annotations
from typing import Any, Mapping, TYPE_CHECKING, Union

from pingsafe_cli.psgraph.common.graph.graph_builder import CustomAttributes
from pingsafe_cli.psgraph.kubernetes.image_referencer.base_provider import BaseKubernetesProvider
from pingsafe_cli.psgraph.common.images.graph.image_referencer_provider import _ExtractImagesCallableAlias

if TYPE_CHECKING:
    from networkx import DiGraph


class BaseHelmProvider(BaseKubernetesProvider):
    def __init__(self, graph_connector: DiGraph,
                 supported_resource_types: dict[str, _ExtractImagesCallableAlias] | Mapping[str, _ExtractImagesCallableAlias],
                 original_root_dir: str, temp_root_dir: str) -> None:
        super().__init__(
            graph_connector=graph_connector,
            supported_resource_types=supported_resource_types,
        )
        self.original_root_dir = original_root_dir
        self.temp_root_dir = temp_root_dir

    def _get_resource_path(self, resource: dict[str, Any]) -> str:
        k8s_path = resource.get(CustomAttributes.FILE_PATH, "")
        return str(k8s_path.replace(self.temp_root_dir, self.original_root_dir, 1))
