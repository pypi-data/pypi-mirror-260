import logging

import sqlalchemy.exc
import sqlalchemy.orm

from palaestrai.core.runtime_config import RuntimeConfig

LOG = logging.getLogger(__name__)


def Session() -> sqlalchemy.orm.Session:
    """Creates a new, connected database session to run queries on.

    This is a convenience function that creates and returns a new, opened
    database session. It uses the access data provided by
    ::`RuntimeConfig.store_uri`. It exists in order to facilitate working
    with the store, such as this::

        from palaestrai.store import Session, database_model as dbm

        session = Session()
        q = session.query(dbm.Experiment)

    Returns:
    --------

    sqlalchemy.orm.Session
        The initialized, opened database session.
    """
    _db_engine = sqlalchemy.create_engine(RuntimeConfig().store_uri)
    _db_session_maker = sqlalchemy.orm.sessionmaker()
    _db_session_maker.configure(bind=_db_engine)
    try:
        return _db_session_maker()
    except (
        sqlalchemy.exc.OperationalError,
        sqlalchemy.exc.ArgumentError,
    ) as e:
        LOG.exception("Is your database available?")
        raise e
