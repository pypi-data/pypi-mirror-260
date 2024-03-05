from dataclasses import dataclass
from conf import get_param, get_env
import sqlalchemy as sa
from pymodm import connect
from typing import ClassVar
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus


class _BaseEnginePool:
    def __init__(self, schema=None):
        self.ec = EngineCreator.from_ini(schema)

    def get(self, database):
        self.ec.database = database
        return self.ec.create_engine(echo=False, future=True, pool_recycle=3600)

    def uri(self, database):
        self.ec.database = database
        return f"mysql+pymysql://{self.ec.uri}"


class MysqlEnginePool:
    def __getattr__(self, name):
        def method():
            return _BaseEnginePool(name)

        return method


class EngineCreator:
    def __init__(
            self,
            host=None,
            port=None,
            database=None,
            username=None,
            password=None,
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self._database = database

    def __repr__(self):
        return "{classname}(host='{host}', port={port}, database='{database}', username={username}, password='xxxxxxxxxxxx')".format(
            classname=self.__class__.__name__,
            host=self.host,
            port=self.port,
            database=self.database,
            username=self.username,
        )

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, var):
        self._database = var

    @classmethod
    def from_ini(cls, schema):
        db_param = DBParam.read_from_conf("mysql", schema)
        return EngineCreator(
            host=db_param.db_host,
            port=db_param.db_port,
            username=db_param.db_user,
            password=db_param.db_pwd,
        )

    @property
    def uri(self) -> str:
        """
        Return sqlalchemy connect string URI.
        """
        uri_template = (
            "{username}{has_password}{password}@{host}{has_port}{port}/{database}"
        )

        return uri_template.format(
            host=self.host,
            port="" if self.port is None else self.port,
            database=self.database,
            username=self.username,
            password="" if self.password is None else self.password,
            has_password="" if self.password is None else ":",
            has_port="" if self.port is None else ":",
        )

    def create_engine(self, **kw):
        return sa.create_engine(
            f"mysql+pymysql://{self.uri}",
            **kw,
        )


class MongoConn:
    mongo_uri: ClassVar[str] = "mongodb://{usr}:{pwd}@{host}:{port}/{database}?authSource=admin"
    """
    创建mongo链接，建议设置别名好进行区分
    """

    @classmethod
    def get(cls, database, alis=None, **kwargs):
        conf = DBParam.read_from_conf("mongo", database)
        format_uri = cls.mongo_uri.format(usr=quote_plus(conf.db_user), pwd=quote_plus(conf.db_pwd), host=conf.db_host,
                                          port=conf.db_port,
                                          database=conf.db_schema)
        if alis is None:
            return connect(format_uri, **kwargs)
        else:
            return connect(format_uri, alias=alis, **kwargs)


class DatabaseConnector:
    class ConnectionBuilder:
        def __init__(self, db_type):
            self.db_type = db_type

        def __call__(self, schema, alias=None):
            if self.db_type == 'mysql':
                engine_pool = _BaseEnginePool(schema=schema)
                return engine_pool.get(schema)
            elif self.db_type == 'mongo':
                return MongoConn.get(schema, alias=alias)

    @classmethod
    def mysql(cls, database, schema) -> sessionmaker:
        return sessionmaker(_BaseEnginePool(database).get(schema))

    @classmethod
    def mongo(cls, schema, alias=None):
        MongoConn.get(schema, alias)


@dataclass
class DBParam:
    db_type: str
    db_host: str
    db_port: str
    db_user: str
    db_pwd: str
    db_schema: str

    @classmethod
    def read_from_conf(cls, type, schema):
        param = get_param("db.ini", type + "_" + schema + "_" + get_env())
        return cls(type, param.get('host'), param.get('port'), param.get('user'), param.get('password'), schema)
