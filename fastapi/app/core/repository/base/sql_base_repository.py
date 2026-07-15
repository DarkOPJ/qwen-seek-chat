from typing import Dict, List, Type, TypeVar, Union

import sqlalchemy as sa
import sqlalchemy as sql
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase

from app.constants import SortResultEnum
from app.core.database import db_sync_session
from app.core.exceptions import AppException

from .crud_repository_interface import CRUDRepositoryInterface

ModelObject = TypeVar("ModelObject", bound=DeclarativeBase)


class SQLBaseRepository(CRUDRepositoryInterface):
    model: Type[DeclarativeBase]
    object_name: str

    def __init__(
        self,
    ):
        self.table = inspect(self.model)
        self.db_session = db_sync_session

    def index(self, paginate_data=False, page_params: Params = None):
        with self.db_session() as session:
            stmt = sql.select(self.model)
            return self._result(
                conn=session,
                query=stmt,
                paginated=paginate_data,
                page_params=page_params,
            )

    def create(self, obj_in):
        with self.db_session() as session:
            obj_data = dict(obj_in)
            db_obj = self.model(**obj_data)
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return db_obj

    def update_by_id(self, obj_id, obj_in):
        db_obj = self.find_by_id(obj_id)
        with self.db_session() as session:
            for field, value in obj_in.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return db_obj

    def delete_by_id(self, obj_id):
        db_obj = self.find_by_id(obj_id)
        with self.db_session() as session:
            session.delete(db_obj)
            session.commit()
        return True

    def find_by_id(self, obj_id):
        with self.db_session() as session:
            result = session.get(self.model, obj_id)
            if not result:
                raise AppException.NotFoundException(
                    error_message=f"{self.object_name}({obj_id}) not found"
                )
            return result

    def find(self, filter_param: dict):
        with self.db_session() as session:
            stmt = sql.select(self.model).filter_by(**filter_param)
            result = session.execute(stmt)
            obj = result.unique().scalar_one_or_none()
            if not obj:
                raise AppException.NotFoundException(
                    error_message=f"{self.object_name}({filter_param}) not found"
                )
            return obj

    def update(self, filter_params, obj_in):
        db_obj = self.find(filter_params)
        with self.db_session() as session:
            for field, value in obj_in.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return db_obj

    def delete(self, filter_params: dict):
        db_obj = self.find(filter_params)
        with self.db_session() as session:
            session.delete(db_obj)
            session.commit()
            return True

    def _is_column_available(self, column_name: str):
        if column_name in self.table.columns.keys():
            return column_name
        raise AppException.BadRequestException(
            error_message=f"column {column_name} does not exist"
        )

    def _result(self, conn, query, paginated=False, page_params=None, many=True):
        if paginated and page_params:
            return paginate(conn=conn, query=query, params=page_params)
        results = conn.execute(query).scalars()
        if not many:
            db_obj = results.first()
            if not db_obj:
                raise AppException.NotFoundException(
                    error_message=f"{self.object_name} not found"
                )
            return db_obj
        return results.all()

    def _is_string_column(self, column):
        return isinstance(column.type, (sa.String, sa.Text))

    def _is_enum_column(self, column):
        return isinstance(column.type, sa.Enum)

    def _is_jsonb_column(self, column):
        return isinstance(column.type, JSONB)

    def _is_date_column(self, column):
        return isinstance(column.type, (sa.DateTime, sa.Date))

    def _query_columns(self, attrs: Union[List[str], None]):
        columns = set()
        attrs = attrs or []
        for attr in attrs:
            self._is_column_available(attr)
            columns.add(getattr(self.model, attr))
        return columns

    def _colum_contain(self, contains: Union[Dict[str, List[str]], None]):
        in_clause = set()
        contains = contains or {}
        for col, value in contains.items():
            in_clause.add(getattr(self.model, col).in_(value))
        return in_clause

    def _colum_includes(self, includes: dict):
        _includes = set()
        includes = includes or {}
        for col, value in includes.items():
            if self._is_string_column(self.table.columns[col]):
                _includes.add(getattr(self.model, col).ilike(f"%{value}%"))
        return _includes

    def _get_sort_order(self, sort_param: dict):
        if sort_param.get("column") and sort_param.get("order") == SortResultEnum.asc:
            return sa.asc(
                getattr(
                    self.model, self._is_column_available(sort_param["column"].strip())
                )
            )
        elif (
            sort_param.get("column") and sort_param.get("order") == SortResultEnum.desc
        ):
            return sa.desc(
                getattr(
                    self.model, self._is_column_available(sort_param["column"].strip())
                )
            )
        return None

    def _build_keyword_query(self, keyword: str) -> set:
        search_query = set()
        for column in self.table.columns:
            try:
                if self._is_string_column(column) and keyword:
                    search_query.add(
                        getattr(self.model, column.name).ilike(f"%{keyword}%")
                    )
                elif self._is_enum_column(column) and keyword:
                    search_query.add(
                        getattr(self.model, column.name)
                        .cast(sa.String)
                        .ilike(f"%{keyword}%")
                    )
                elif self._is_jsonb_column(column) and keyword:
                    search_query.add(
                        getattr(self.model, column.name)
                        .cast(sa.String)
                        .ilike(f"%{keyword}%")
                    )
            except AttributeError:
                continue
        return search_query

    def _build_date_query(self, date_filter: dict) -> set:
        query = set()
        if date_filter.get("column"):
            column = self._is_column_available(date_filter.get("column").strip())
            if self._is_date_column(self.table.columns[column]):
                if date_filter.get("min_date") and date_filter.get("max_date"):
                    query.add(
                        getattr(self.model, column).between(
                            date_filter["min_date"], date_filter["max_date"]
                        )
                    )
                elif date_filter.get("min_date"):
                    query.add(getattr(self.model, column) >= date_filter["min_date"])
                elif date_filter.get("max_date"):
                    query.add(getattr(self.model, column) <= date_filter["max_date"])
                elif date_filter.get("date"):
                    query.add(
                        sa.cast(getattr(self.model, column), sa.Date)
                        == date_filter["date"]
                    )
            else:
                raise AppException.BadRequestException(
                    error_message=f"column {column} not of type date"
                )
        return query

    def find_all(
        self,
        filter_param: dict,
        paginate_data: bool = False,
        page_params: Params = None,
    ):
        with self.db_session() as session:
            stmt = sql.select(self.model).filter_by(**filter_param)
            return self._result(
                conn=session,
                query=stmt,
                paginated=paginate_data,
                page_params=page_params,
            )

    def advance_query(
        self,
        keyword: str = None,
        date_filter: dict = None,
        sort_param: dict = None,
        filter_params: dict = None,
        includes: Dict[str, str] = None,
        contains: Dict[str, List[str]] = None,
        columns: List[str] = None,
        paginate_data: bool = False,
        page_params: Params = None,
        many: bool = True,
    ):
        with self.db_session() as session:
            filters = [*self._colum_contain(contains), *self._colum_includes(includes)]
            filters += list(self._build_keyword_query(keyword=keyword))
            filters += list(self._build_date_query(date_filter or {}))
            if filter_params:
                filters.append(
                    sa.and_(
                        True,
                        *[
                            getattr(self.model, k) == v
                            for k, v in filter_params.items()
                        ],
                    )
                )

            stmt = (
                sql.select(*self._query_columns(columns))
                if columns
                else sql.select(self.model)
            )
            if filters:
                stmt = stmt.filter(*filters)
            if sort_order := self._get_sort_order(sort_param or {}):
                stmt = stmt.order_by(sort_order)

            return self._result(
                conn=session,
                query=stmt,
                paginated=paginate_data,
                page_params=page_params,
                many=many,
            )
