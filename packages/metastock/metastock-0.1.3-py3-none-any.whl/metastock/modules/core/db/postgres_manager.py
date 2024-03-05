from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

from metastock.modules.core.logging.logger import Logger, AppLogger
from metastock.modules.core.util.environment import env


class PostgresManager:
    def __init__(self, logger: AppLogger = None):
        self.Session = None
        self._engine = None
        self.logger = logger or Logger()

    def initialize(self):
        if self._engine is not None:
            return

        self.logger.info("Initializing Postgres...")

        host = env().get("POSTGRES_HOST")
        user = env().get("POSTGRES_USER")
        password = env().get("POSTGRES_PASSWORD")
        port = env().get("POSTGRES_PORT")
        db_name = env().get("POSTGRES_DB_NAME")

        self.logger.debug(
            "Postgres connection info: host=%s, user=%s, password=%s, port=%s, db_name=%s"
            % (host, user, password, port, db_name)
        )

        self._engine = create_engine(
            f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db_name}"
        )
        self.Session = sessionmaker(bind=self._engine)

        # Try to connect db
        try:
            session = self.Session()
            session.execute(text("SELECT 1"))
            session.close()

            self.logger.ok("Postgres connection successful")
        except Exception as e:
            self.logger.error("Postgres connection error: %s", e)

    def get_engine(self):
        self.initialize()

        return self._engine

    def get_session(self) -> Session:
        return self.Session()

    def get_session_factory(self) -> sessionmaker:
        return self.Session

    def create_tables(self):
        # Đây là nơi bạn có thể định nghĩa các bảng trong cơ sở dữ liệu của bạn và sử dụng `self.engine` để tạo chúng.
        # Ví dụ:
        # Base.metadata.create_all(self.engine)
        pass

    def drop_tables(self):
        # Đây là nơi bạn có thể xóa các bảng khỏi cơ sở dữ liệu của bạn sử dụng `self.engine`.
        # Ví dụ:
        # Base.metadata.drop_all(self.engine)
        pass


postgres_manager = PostgresManager()
