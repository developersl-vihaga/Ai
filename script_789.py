from pathlib import Path
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import MetaData, Table
from sqlalchemy.exc import (
    IllegalStateChangeError,
    NoInspectionAvailable,
    NoSuchTableError,
)
from cme.logger import cme_logger
class database:
    def __init__(self, db_engine):
        self.CredentialsTable = None
        self.HostsTable = None
        self.db_engine = db_engine
        self.db_path = self.db_engine.url.database
        self.protocol = Path(self.db_path).stem.upper()
        self.metadata = MetaData()
        self.reflect_tables()
        session_factory = sessionmaker(bind=self.db_engine, expire_on_commit=True)
        Session = scoped_session(session_factory)
        self.conn = Session()
    @staticmethod
    def db_schema(db_conn):
        db_conn.execute(
            """CREATE TABLE "credentials" (
            "id" integer PRIMARY KEY,
            "username" text,
            "password" text
            )"""
        )
        db_conn.execute(
            """CREATE TABLE "hosts" (
            "id" integer PRIMARY KEY,
            "ip" text,
            "hostname" text,
            "port" integer
            )"""
        )
    def reflect_tables(self):
        with self.db_engine.connect() as conn:
            try:
                self.CredentialsTable = Table("credentials", self.metadata, autoload_with=self.db_engine)
                self.HostsTable = Table("hosts", self.metadata, autoload_with=self.db_engine)
            except (NoInspectionAvailable, NoSuchTableError):
                print(
                    f"""
                    [-] Error reflecting tables for the {self.protocol} protocol - this means there is a DB schema mismatch
                    [-] This is probably because a newer version of CME is being ran on an old DB schema
                    [-] Optionally save the old DB data (`cp {self.db_path} ~/cme_{self.protocol.lower()}.bak`)
                    [-] Then remove the CME {self.protocol} DB (`rm -f {self.db_path}`) and run CME to initialize the new DB"""
                )
                exit()
    def shutdown_db(self):
        try:
            self.conn.close()
        except IllegalStateChangeError as e:
            cme_logger.debug(f"Error while closing session db object: {e}")
    def clear_database(self):
        for table in self.metadata.sorted_tables:
            self.conn.execute(table.delete())