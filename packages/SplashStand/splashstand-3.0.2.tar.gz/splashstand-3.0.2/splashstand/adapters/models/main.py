import typing as t
from ast import literal_eval
from contextlib import suppress
from contextvars import ContextVar
from datetime import date
from datetime import time
from datetime import timedelta
from decimal import Decimal
from enum import Enum
from inspect import isclass
from warnings import catch_warnings
from warnings import filterwarnings

import arrow
import uuid_utils as uuid
from acb import base_path
from acb.actions.encode import load
from acb.adapters import import_adapter
from acb.adapters import settings_path
from acb.config import Settings
from acb.config import Config
from acb.debug import debug
from acb.depends import depends
from aiopath import AsyncPath
from fastblocks import current_user
from inflection import camelize
from inflection import pluralize
from inflection import tableize
from inflection import titleize
from inflection import underscore
from pydantic import ConfigDict
from pydantic import create_model
from pydantic.types import UUID
from schemaorg_lite import main as schemaorg  # type: ignore
from sqlalchemy import Column
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.types import TypeDecorator
from sqlalchemy_utils import ArrowType
from sqlalchemy_utils import ChoiceType
from sqlalchemy_utils import ColorType
from sqlalchemy_utils import CountryType
from sqlalchemy_utils import CurrencyType
from sqlalchemy_utils import EmailType
from sqlalchemy_utils import LocaleType
from sqlalchemy_utils import PhoneNumberType
from sqlalchemy_utils import URLType
from sqlmodel import Field
from sqlmodel import Relationship
from sqlmodel import select
from sqlmodel import SQLModel
from sqlmodel.main import default_registry

# from sqlalchemy.ext.hybrid import hybrid_property
# from sqlalchemy_utils import TimezoneType

Logger = import_adapter()


def primary_key_factory() -> UUID:
    return UUID(str(uuid.uuid7()))


class AppModel(SQLModel):
    model_config: ConfigDict = ConfigDict(arbitrary_types_allowed=True, extra="allow")
    __table_args__ = {"extend_existing": True}
    __mapper_args__ = {"always_refresh": True}
    id: t.Optional[UUID] = Field(default_factory=primary_key_factory, primary_key=True)

    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:  # type: ignore
        return underscore(cls.__name__)

    # @hybrid_property
    # def date_created(self):
    #     return Field(Arrow.from_timestamp(ulid.parse(self.id).timestamp().int),
    #       alias="created_at")
    #
    # https://github.com/van51/sqlmodel.git#93509eb

    @property
    def date_created(self):
        return Field(
            arrow.Arrow.from_timestamp(  # type: ignore
                self.id.timestamp()  # type: ignore
            ),
            alias="created_at",
        )

    maintainer: t.Optional[str] = Field(
        default_factory=lambda: current_user.get().identity, alias="created_by"
    )
    # date_modified: t.Optional[ArrowType] = Field(
    #     default_factory=arrow.utcnow,
    #     alias="last_edited_at",
    #     sa_column=Column(ArrowType, onupdate=arrow.utcnow),
    # )
    editor: t.Optional[str] = Field(
        default_factory=lambda: current_user.get().identity,
        sa_column_kwargs=dict(onupdate=lambda: current_user.get().identity),
        alias="last_edited_by",
    )

    @depends.inject
    async def save(self) -> None:
        sql = depends.get(import_adapter("sql"))
        async with sql.get_session() as session:
            session.add(self)
            await session.commit()

    @classmethod
    @depends.inject
    async def query(cls) -> t.Any:
        sql = depends.get(import_adapter("sql"))
        async with sql.get_session() as session:
            return (await session.exec(select(cls))).all()


# Relationship(sa_relationship_kwargs={"ondelete":"cascade"},back_populates="news",
# link_model=EventNews}))


data_type_map = dict(
    bool=bool,
    false=False,
    true=True,
    date=date,
    datetime=ArrowType,
    duration=timedelta,
    timedelta=timedelta,
    time=time,
    decimal=Decimal,
    number=Decimal,
    float=float,
    int=int,
    str=str,
    text=str,
    choice=ChoiceType,
    email=EmailType,
    cssselectortype=str,
    pronounceabletext=str,
    url=URLType,
    xpathtype=str,
    currency=CurrencyType,
    phonenumber=PhoneNumberType,
    country=CountryType,
    locale=LocaleType,
    color=ColorType,
)

schema_registry: ContextVar[dict[str, t.Any]] = ContextVar(
    "schema_registry", default={}
)
_field_relationships: ContextVar[t.Any] = ContextVar("_field_relationships", default=[])
_field_definitions: ContextVar[t.Any] = ContextVar("_field_definitions", default={})
_schema_models: ContextVar[t.Any] = ContextVar("_schema_models", default={})
_schema_orgs: ContextVar[t.Any] = ContextVar("_schema_orgs", default={})
_model_overrides: ContextVar[t.Any] = ContextVar("_model_overrides", default={})


class SchemaModel:
    config: Config = depends()
    logger: Logger = depends()  # type: ignore

    def __init__(self, name: str, **data: str) -> None:
        self.name = camelize(name)
        self.alias = str
        self.table_name = underscore(name)
        self.model_overrides = _model_overrides.get().get(self.table_name) or {}
        self.schema_definitions = {}
        self.schema = {}
        self.schema_model = {}
        self.sqlmodel_fields = {}
        super().__init__(**data)

    @staticmethod
    def get_relation_table_name(primary: str, secondary: str) -> str:
        print(underscore(f"{primary}__{secondary}"))
        return f"{underscore(primary)}__{underscore(secondary)}"

    @depends.inject
    async def create_link_model(self, relation1: str, relation2: str):
        related = {}
        for relation in (relation1, relation2):
            relation = underscore(relation)
            related[f"{relation}_id"] = (
                t.Optional[UUID],
                Field(default=None, foreign_key=f"{relation}.id"),
            )
        model_name = self.get_relation_table_name(relation1, relation2)
        model = create_model(
            model_name, __base__=SQLModel, __cls_kwargs__={"table": True}, **related
        )
        setattr(depends.get(Models), model_name, model)
        return model_name

    async def create_fields(self) -> None:
        if self.name not in _field_definitions.get():
            _field_definitions.get()[self.name] = {}
        self.schema_model = schema_registry.get().get(self.table_name)
        _schema_models.get()[self.name] = self.schema_model
        self.schema = _schema_orgs.get().get(self.name)
        if not self.schema:
            self.schema = schemaorg.Schema(self.name)
            _schema_orgs.get()[self.name] = self.schema
        self.schema_definitions = self.schema._properties
        field_overrides = self.model_overrides.get("fields", {})
        non_field_overrides = {
            k: v for (k, v) in self.model_overrides.items() if k != "fields"
        }
        self.schema_model = self.schema_model | non_field_overrides  # type: ignore
        self.sqlmodel_fields = self.schema_model.get("fields", {})
        self.alias = self.schema_model.get("alias", self.table_name)
        extends = [
            x
            for x in (
                "thing",
                self.schema_model.get("parent"),
                self.schema_model.get("extends"),
            )
            if x
        ]
        if extends:
            parents = []
            for extend in extends:
                while 1:
                    extends_model = schema_registry.get()[underscore(extend)]
                    parents.append(extends_model)
                    if "extends" in extends_model:
                        extend = underscore(extends_model["extends"])
                        continue
                    break
            for parent in reversed(parents):
                self.sqlmodel_fields = parent["fields"] | self.sqlmodel_fields
        for prop, attrs_ in field_overrides.items():
            self.sqlmodel_fields[prop] = self.sqlmodel_fields[prop] | attrs_
        for prop, attrs_ in self.sqlmodel_fields.items():
            _help = False
            with suppress(TypeError):
                _help = self.schema_definitions.get(
                    camelize(prop, False)  # type: ignore
                )["comment"]
            type_ = attrs_.get("type")
            if not type_:
                continue
            alias = attrs_.get("alias")
            required = attrs_.get("required", False)
            unique = attrs_.get("unique")
            field_type = data_type_map.get(type_.lower())
            choices = attrs_.get("choices")
            sa_column = None
            if isinstance(field_type, ChoiceType | Enum):
                if isinstance(choices, str):
                    choices = literal_eval(choices)
                enum = Enum(camelize(f"{prop}_choices"), choices)
                sa_column = Column(ChoiceType(enum))
            elif isclass(field_type) and issubclass(field_type, TypeDecorator):
                sa_column = Column(field_type)
            relation = underscore(type_) if not field_type else None
            relation_type = attrs_.get("relation", "one-to-many")
            one_2_many = (
                True if relation_type == "one-to-many" and not field_type else None
            )
            many_2_many = (
                True if relation_type == "many-to-many" and not field_type else None
            )
            prop_name = f"{prop}_id" if not field_type else prop
            content_length = None
            match type_.lower():
                case "text":
                    content_length = 10710
                case _:
                    ...
            if not many_2_many:
                default_factory = attrs_.get("default_factory")
                field_kwargs = dict(
                    default=attrs_.get("default") if not default_factory else None,
                    default_factory=(
                        exec(default_factory) if default_factory else None
                    ),
                    max_length=(
                        attrs_.get("max_length") or content_length  # type: ignore
                    ),
                    foreign_key=(
                        f"{relation}.id" if one_2_many else None  # type: ignore
                    ),
                    description=_help,  # type: ignore
                    alias=alias,
                    unique=unique if sa_column is None else None,
                    sa_column=sa_column,
                )
                field = Field(  # type: ignore
                    **{k: v for (k, v) in field_kwargs.items() if v is not None}
                )
                field_type = UUID if one_2_many else field_type  # type: ignore
                field_type = (
                    t.Optional[field_type]  # type: ignore
                    if not required  # or prop_name.endswith("_id")
                    else field_type
                )
                _field_definitions.get()[self.name][prop_name] = (field_type, field)
            if not relation:
                continue
            if type_ not in _field_definitions.get():
                await SchemaModel(type_).create_fields()
            link_model = None
            if many_2_many:
                link_model_name = self.get_relation_table_name(self.name, type_)
                with suppress(InvalidRequestError):
                    with catch_warnings():
                        filterwarnings("ignore", category=Warning)
                        await self.create_link_model(self.name, type_)
                link_model = getattr(depends.get(Models), link_model_name)
                debug(link_model)
            primary = dict(
                name="primary",
                model_name=self.name,
                prop_name=pluralize(prop) if many_2_many else prop,
                field_type=t.List[type_] if many_2_many else t.Optional[type_],
                relation_kwargs=dict(
                    back_populates=tableize(self.name),
                    sa_relationship_kwargs=(
                        {"primaryjoin": f"{self.name}.{prop_name}=={type_}.id"}
                        if one_2_many
                        else None
                    ),
                    link_model=link_model,
                ),
            )
            secondary = dict(
                name="secondary",
                model_name=type_,
                prop_name=tableize(self.name),
                field_type=t.List[self.name],  # type: ignore
                relation_kwargs=dict(
                    back_populates=pluralize(prop) if many_2_many else prop,
                    sa_relationship_kwargs=(
                        {"primaryjoin": f"{type_}.id=={self.name}.{prop_name}"}
                        if one_2_many
                        else None
                    ),
                    link_model=link_model,
                ),
            )
            for related in (primary, secondary):
                relationship_kwargs = {
                    k: v
                    for (k, v) in related["relation_kwargs"].items()  # type: ignore
                    if v is not None
                }
                _field_definitions.get().get(related["model_name"])[
                    related["prop_name"]
                ] = (
                    related["field_type"],
                    Relationship(**relationship_kwargs),
                )
            if type_ not in _field_relationships.get():
                _field_relationships.get().append(type_)

    async def create_sqlmodel(self) -> None:
        await self.create_fields()
        model = create_model(
            self.name,
            __base__=AppModel,
            __cls_kwargs__={"table": True},
            **_field_definitions.get()[self.name],
        )
        model._alias = self.alias
        model._schema = self.schema
        model._help = vars(self.schema)["comment"]
        model.__doc__ = vars(self.schema)["comment"]
        setattr(depends.get(Models), self.name, model)


class ModelsSettings(Settings): ...


class Models:
    logger: Logger = depends()  # type: ignore

    async def init(self) -> None:
        SQLModel.metadata.clear()
        self.logger.info("Creating models...")
        model_overrides = await load.yaml(AsyncPath(settings_path / "models.yml"))
        for model, overrides in {m: o for m, o in model_overrides.items() if o}:
            _model_overrides.get().update({model: overrides})
        for s in [
            s
            async for s in (base_path / "schemas").glob("**/*.yml")
            if await s.is_file()
        ]:
            schema_name = s.stem
            parent_name = s.parent.stem
            if s.stem == "_base":
                schema_name = parent_name
                parent_name = s.parent.parent.stem
            elif s.stem.startswith("_"):
                continue
            properties = await load.yaml(s) or {}
            if parent_name not in ("schema", base_path.stem, "thing", "intangible"):
                properties.update({"parent": parent_name})
            schema_registry.get()[schema_name] = properties
        model_list = {
            s: a for (s, a) in schema_registry.get().items() if a and a.get("model")
        }
        for schema in model_list:
            await SchemaModel(schema).create_sqlmodel()
            self.logger.info(f"{titleize(schema)} model created")
        for schema in _field_relationships.get():
            model = getattr(depends.get(Models), schema)
            for k, v in vars(model.__table__).items():
                debug(k)
                debug(v)
            for k, v in default_registry.__dict__.items():
                debug(k)
                # debug(v)
            default_registry._dispose_cls(cls=model)
            await SchemaModel(schema).create_sqlmodel()
            self.logger.debug(f"{titleize(schema)} model updated")
        self.logger.info("Models created")

    async def create_user(
        self,
        gmail: EmailType,
        is_superuser: bool = False,
        role: str = "user",
        **kwargs: str,
    ) -> None:
        user = getattr(self, "Person")(
            gmail=gmail, is_superuser=is_superuser, role=role, **kwargs
        )
        await user.save()


depends.set(Models)
