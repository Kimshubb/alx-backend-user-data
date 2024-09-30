#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session
    
    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Create a user object and sava it to db
        Args: Email (str)
            hashed_password(str) : password hashed using bcrypt
        Return: Newly created user object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        try:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


    def find_user_by(self, **kwargs) -> User:
        """
        Returns a user from db who has similar attributes as passed args
        """
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).one()
        except NoResultFound as e:
            raise NoResultFound(f"No user found for {kwargs}") from e
        except InvalidRequestError as e:
            raise InvalidRquestError(f"Invalid query arguments: {kwargs}") from e
        return user
