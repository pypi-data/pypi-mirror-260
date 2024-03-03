"""Data model definitions; backed by an RDBMS."""
from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy import orm as sa_orm

from corvic.orm.base import Base
from corvic.orm.keys import MappedPrimaryKey, primary_key_column

from .ids import ExperimentID, ResourceID, SourceID, SpaceID, SpaceSourceID


class Resource(Base):
    """A Resource represents import data."""

    __tablename__ = "resource"

    name: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text)
    mime_type: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text)
    url: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text)
    md5: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.CHAR(32), nullable=True)
    size: sa_orm.Mapped[int] = sa_orm.mapped_column(nullable=True)
    original_path: sa_orm.Mapped[str] = sa_orm.mapped_column(nullable=True)
    description: sa_orm.Mapped[str] = sa_orm.mapped_column(nullable=True)
    id: MappedPrimaryKey = primary_key_column()

    source_associations: sa_orm.Mapped[
        list[SourceResourceAssociation]
    ] = sa_orm.relationship(
        back_populates="resource",
        cascade="save-update, merge, delete, delete-orphan",
        default_factory=list,
    )


class Source(Base):
    """A Source describes how resources should be treated."""

    __tablename__ = "source"
    __table_args__ = (sa.UniqueConstraint("name"),)

    name: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text)
    # protobuf describing the operations required to construct a table
    table_op_graph: sa_orm.Mapped[bytes] = sa_orm.mapped_column(sa.LargeBinary)
    id: MappedPrimaryKey = primary_key_column()

    resource_associations: sa_orm.Mapped[
        list[SourceResourceAssociation]
    ] = sa_orm.relationship(
        back_populates="source",
        cascade="save-update, merge, delete, delete-orphan",
        default_factory=list,
    )

    @property
    def source_key(self):
        return self.name


class SourceResourceAssociation(Base):
    __tablename__ = "source_resource_association"

    source_id: MappedPrimaryKey = primary_key_column(Source.foreign_key().make())
    resource_id: MappedPrimaryKey = primary_key_column(Resource.foreign_key().make())
    source: sa_orm.Mapped[Source] = sa_orm.relationship(
        back_populates="resource_associations", init=False
    )
    resource: sa_orm.Mapped[Resource] = sa_orm.relationship(
        back_populates="source_associations", init=False
    )


class Space(Base):
    """A Space defines how Sources should be modeled to create a feature space."""

    __tablename__ = "space"

    id: MappedPrimaryKey = primary_key_column()
    name: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text, default=None)
    description: sa_orm.Mapped[str] = sa_orm.mapped_column(sa.Text, default="")

    @property
    def space_key(self):
        return self.name

    space_sources: sa_orm.Mapped[list[SpaceSource]] = sa_orm.relationship(
        viewonly=True,
        init=True,
        default_factory=list,
        secondary="space_source",
        secondaryjoin=lambda: (Space.id == SpaceSource.space_id)
        & (SpaceSource.source_id == Source.id),
    )


class SpaceSource(Base):
    """Sources inside of a space."""

    __tablename__ = "space_source"
    table_op_graph: sa_orm.Mapped[bytes] = sa_orm.mapped_column(sa.LargeBinary)
    id: MappedPrimaryKey = primary_key_column()
    drop_disconnected: sa_orm.Mapped[bool] = sa_orm.mapped_column(default=False)
    space_id: sa_orm.Mapped[int | None] = sa_orm.mapped_column(
        Space.foreign_key().make(ondelete="CASCADE"), nullable=False, default=None
    )
    source_id: sa_orm.Mapped[int | None] = sa_orm.mapped_column(
        Source.foreign_key().make(ondelete="CASCADE"), nullable=False, default=None
    )
    source: sa_orm.Mapped[Source] = sa_orm.relationship(init=True, default=None)
    space: sa_orm.Mapped[Space] = sa_orm.relationship(init=True, default=None)


class IntraSpaceRelationship(Base):
    __tablename__ = "intra_space_relationship"
    from_source_id: sa_orm.Mapped[int] = sa_orm.mapped_column(
        Source.foreign_key().make(ondelete="CASCADE"), nullable=False, primary_key=True
    )
    to_source_id: sa_orm.Mapped[int] = sa_orm.mapped_column(
        Source.foreign_key().make(ondelete="CASCADE"), nullable=False, primary_key=True
    )
    directional: sa_orm.Mapped[bool] = sa_orm.mapped_column(nullable=False)
    space_id: sa_orm.Mapped[int | None] = sa_orm.mapped_column(
        Space.foreign_key().make(ondelete="CASCADE"),
        nullable=False,
        default=None,
        primary_key=True,
    )

    space: sa_orm.Mapped[Space] = sa_orm.relationship(default=None)


class Experiment(Base):
    """An Experiment is the result produced by applying embedding methods to Spaces."""

    __tablename__ = "experiment"

    table_op_graph: sa_orm.Mapped[bytes] = sa_orm.mapped_column(sa.LargeBinary)
    id: MappedPrimaryKey = primary_key_column()


__all__ = [
    "Experiment",
    "ExperimentID",
    "ResourceID",
    "Source",
    "SourceID",
    "Space",
    "SpaceID",
    "SpaceSource",
    "SpaceSourceID",
]
