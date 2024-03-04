import datetime
from abc import ABC, abstractmethod
from typing import NamedTuple, Sequence

from sqlalchemy import (Boolean, Column, DateTime, Integer, RowMapping, String,
                        func, select)
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import declarative_base


class JobExtents(NamedTuple):
  values: dict


class Progress(NamedTuple):
  value: int
  max_value: int


class ETAEstimatorBase(ABC):

  def __self__(self):
    pass

  @abstractmethod
  async def Begin(self, *, job_id: str, job_extents: JobExtents):
    raise NotImplementedError()

  @abstractmethod
  async def Record(self, *, job_id: str, node_id: str | None,
                   node_progress: Progress | None):
    raise NotImplementedError()

  @abstractmethod
  async def ETA(self, *, job_id: str, node_id: str | None,
                node_progress: Progress | None) -> float | None:
    raise NotImplementedError()

  @abstractmethod
  async def RecordFinished(self, *, job_id: str):
    raise NotImplementedError()


class DummyETAEstimator(ETAEstimatorBase):

  def __init__(self):
    pass

  async def Begin(self, *, job_id: str, job_extents: JobExtents):
    pass

  async def Record(self, *, job_id: str, node_id: str | None,
                   node_progress: Progress | None):
    pass

  async def ETA(self, *, job_id: str, node_id: str | None,
                node_progress: Progress | None) -> float | None:
    return None

  async def RecordFinished(self, *, job_id: str):
    pass


class SqliteETAEstimator(ETAEstimatorBase):
  Base = declarative_base()

  class Job(Base):
    __tablename__ = 'jobs'
    job_id = Column(String, primary_key=True)
    job_extents = Column(String)
    recorded_at = Column(DateTime, nullable=False)
    finished_at = Column(DateTime, nullable=True)

  class Datapoint(Base):
    __tablename__ = 'datapoints'
    datapoint_id = Column(Integer, primary_key=True, autoincrement=True)
    job_extents = Column(String)
    job_id = Column(String)
    node_id = Column(String, nullable=True)
    node_progress = Column(Integer, nullable=True)
    recorded_at = Column(DateTime, nullable=False)
    delta = Column(Integer, nullable=False)
    finished = Column(Boolean, nullable=False)

  def __init__(self, *, db_url: str):
    """

    Args:
        db_url (str): e.g "sqlite+aiosqlite:///./test.db"
    """
    self._db_url = db_url
    self._async_engine: AsyncEngine = create_async_engine(db_url, echo=True)
    self._async_session = async_sessionmaker(bind=self._async_engine,
                                             class_=AsyncSession,
                                             expire_on_commit=False)

  async def Init(self):
    # Create tables
    async with self._async_engine.begin() as conn:
      await conn.run_sync(self.Base.metadata.create_all)

  async def Begin(self, *, job_id: str, job_extents: JobExtents):
    async with self._async_session() as session:
      async with session.begin():
        job = self.Job(job_id=job_id, job_extents=str(job_extents))
        session.add(job)

  async def Record(self,
                   *,
                   job_id: str,
                   node_id: str | None,
                   node_progress: Progress | None,
                   finished: bool = False):
    async with self._async_session() as session:
      async with session.begin():
        # Find job,
        job: SqliteETAEstimator.Job = await session.get(self.Job, job_id)
        if job is None:
          raise Exception(f'Job {job_id} not found')
        datapoint = self.Datapoint(job_id=job_id,
                                   job_extents=job.job_extents,
                                   node_id=node_id,
                                   node_progress=node_progress,
                                   recorded_at=func.now(),
                                   delta=func.now() - job.recorded_at)
        session.add(datapoint)

  async def ETA(self, *, job_id: str, node_id: str | None,
                node_progress: Progress | None) -> float | None:
    async with self._async_session() as session:
      async with session.begin():
        # Find job,
        job: SqliteETAEstimator.Job = await session.get(self.Job, job_id)
        if job is None:
          raise Exception(f'Job {job_id} not found')
        query = select(SqliteETAEstimator.Datapoint).where(
            SqliteETAEstimator.Datapoint.job_id == job_id).order_by(
                SqliteETAEstimator.Datapoint.datapoint_id.desc())

        result = await session.execute(query)
        datapoints_path: Sequence[RowMapping] = result.mappings().all()
        if len(datapoints_path) == 0:
          return None
        time_since_last_datapoint: float = (
            datetime.datetime.now() -
            datapoints_path[-1]['recorded_at']).total_seconds()
        time_since_start: float = (
            datetime.datetime.now() -
            datapoints_path[0]['recorded_at']).total_seconds()
        known_node: str | None = None
        time_since_known_node: float = 0.0

        for datapoint in reversed(datapoints_path):
          if known_node is None and datapoint['node_id'] is not None:
            known_node = datapoint['node_id']
            time_since_known_node = (datetime.datetime.now() -
                                     datapoint['recorded_at']).total_seconds()

        # for i,datapoint in datapoints_path:
        #   delta: int = cast(int, datapoint.delta)

        query = select(SqliteETAEstimator.Datapoint).where(
            SqliteETAEstimator.Datapoint.job_extents ==
            job.job_extents).order_by(
                SqliteETAEstimator.Datapoint.job_id.desc(),
                SqliteETAEstimator.Datapoint.datapoint_id.desc())
        result = await session.execute(query)
        all_datapoints_paths: Sequence[
            SqliteETAEstimator.Datapoint] = result.scalars().all()
