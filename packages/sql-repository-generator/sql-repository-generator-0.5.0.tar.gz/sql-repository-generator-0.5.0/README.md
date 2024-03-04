![logo](LOGO.jpg)
# SQLRepositoryGenerator

![pipeline](https://gitlab.com/Tagashy/sqlgen/badges/master/pipeline.svg)
![coverage](https://gitlab.com/Tagashy/sqlgen/badges/master/coverage.svg)
![release](https://gitlab.com/Tagashy/sqlgen/-/badges/release.svg)

## Description

SQLRepositoryGenerator is a wrapper above [SQLAlchemy](https://www.sqlalchemy.org/) to allow the generation of Repository class from
SQLAlchemy models.

This way one can concentrate the repository code to non standard SQL query and have the common one auto generated.

## Installation

`pip install sql-repository-generator`

## Usage

to use SQLRepositoryGenerator, it is needed to make a child class of one of the Repository base class

### AsyncRepository
AsyncRepository is a base class that just hide the internal of query making for a given model
#### Example

```python
from typing import Annotated
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

from sqlgen import AsyncRepository

UUID_PK = Annotated[UUID, mapped_column(primary_key=True)]
PROJECT_FK = Annotated[UUID, mapped_column(ForeignKey("project.id"))]


class Base(DeclarativeBase):
    id: Mapped[UUID_PK] = mapped_column(default=uuid4)


class Host(Base):
    __tablename__ = "host"
    name: Mapped[str]
    project_id: Mapped[PROJECT_FK]
    project: Mapped["Project"] = relationship(back_populates="hosts")


class HostRepository(AsyncRepository):
    cls = Host  # Model to query


async def main(session: AsyncSession):
    repository = HostRepository(session)
    host = await repository.create(name="toto")
    hosts = await repository.get_all()

```


### AsyncObjectBoundRepository
AsyncObjectBoundRepository allows to have a repository filtered for a specific object_id:
#### Example

```python
from typing import Annotated
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

from sqlgen import AsyncObjectBoundRepository

UUID_PK = Annotated[UUID, mapped_column(primary_key=True)]
HOST_FK = Annotated[UUID, mapped_column(ForeignKey("host.id"))]
PROJECT_FK = Annotated[UUID, mapped_column(ForeignKey("project.id"))]


class Base(DeclarativeBase):
    id: Mapped[UUID_PK] = mapped_column(default=uuid4)


class Webserver(Base):
    __tablename__ = "webserver"

    host_id: Mapped[HOST_FK]
    host: Mapped["Host"] = relationship(back_populates="webservers")


class Host(Base):
    __tablename__ = "host"
    name: Mapped[str]
    project_id: Mapped[PROJECT_FK]
    project: Mapped["Project"] = relationship(back_populates="hosts")
    webservers: Mapped[list["Webserver"]] = relationship(back_populates="host", cascade="all, delete-orphan")


class Project(Base):
    __tablename__ = "project"
    hosts: Mapped[list["Host"]] = relationship(back_populates="project", cascade="all, delete-orphan")


class WebserverRepository(AsyncObjectBoundRepository):
    cls = Webserver  # Model to query
    bound_model = Project


async def main(session: AsyncSession):
    project_id = uuid4()
    repository = WebserverRepository(session, project_id)
    host = await repository.create(name="toto")  # Not Filtered
    hosts = await repository.get_all()  # filtered by Webserver.host.project.id == project_id

```

## Support

Any help is welcome. you can either:

- [create an issue](https://gitlab.com/Tagashy/sqlgen/issues/new)
- look for TODO in the code and provide a MR with changes
- provide a MR for support of new class

## Roadmap

- Make a public python package

## Authors and acknowledgment

Currently, solely developed by Tagashy but any help is welcomed and will be credited here.

## License

See the [LICENSE](LICENSE) file for licensing information as it pertains to
files in this repository.
