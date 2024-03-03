"""Experiments."""

from collections.abc import Iterable, Iterator
from typing import Any, TypeAlias

import polars as pl
from more_itertools import flatten

from corvic import embed, orm
from corvic.model.spaces import Space, SpaceSource
from corvic.model.wrapped_orm import WrappedOrmObject
from corvic.result import BadArgumentError

ExperimentID: TypeAlias = orm.ExperimentID


class Experiment(WrappedOrmObject[ExperimentID, orm.Experiment]):
    """Experiments are the results produced by applying embedding methods to Spaces.

    Example:
    >>> experiment = Experiment.node2vec(space, dim=10, walk_length=10, window=10)
    """

    def _sub_orm_objects(self, orm_object: orm.Experiment) -> Iterable[orm.Base]:
        return []

    @classmethod
    def node2vec(
        cls, space: Space, *, dim: int, walk_length: int, window: int
    ) -> embed.Node2Vec[str]:
        """Run Node2Vec on the graph described by the space.

        Args:
            space: The space to run Node2Vec on
            dim: The dimensionality of the embedding
            walk_length: Length of the random walk to be computed
            window: Size of the window. This is half of the context,
                as the context is all nodes before `window` and
                after `window`.

        Returns:
            An Experiment
        """
        if not space.relationships:
            raise BadArgumentError("Node2Vec requires some relationships")

        directed = space.relationships[0].directional
        if any(rel.directional != directed for rel in space.relationships):
            raise NotImplementedError(
                "node2vec with mixed directionality not yet implemented"
            )

        def normalize(id_val: Any, space_source: SpaceSource):
            return f"{space_source.source.name}-{id_val}"

        edges: list[tuple[str, str]] = list(
            flatten(
                (
                    (
                        normalize(frm, rel.from_space_source),
                        normalize(to, rel.to_space_source),
                    )
                    for frm, to in rel.edge_list()
                )
                for rel in space.relationships
            )
        )
        n2v_space = embed.Space(edges, directed=directed)
        return embed.Node2Vec(
            space=n2v_space, dim=dim, walk_length=walk_length, window=window
        )

    def to_polars(self) -> Iterator[pl.DataFrame]:
        raise NotImplementedError()
