from __future__ import annotations

import abc
import importlib
import pathlib

import jinja2
import pandas as pd

import lea


class Client(abc.ABC):
    """

    This is the base class for all clients. It defines the interface that all clients must
    implement. It is not meant to be used directly. Instead, use one of the subclasses.

    """

    @abc.abstractproperty
    def sqlglot_dialect(self):
        ...

    def prepare(self):
        ...

    @abc.abstractmethod
    def teardown(self):
        ...

    @abc.abstractmethod
    def _view_key_to_table_reference(self, view_key: tuple[str], with_username: bool) -> str:
        ...

    @abc.abstractmethod
    def _table_reference_to_view_key(self, table_reference: str) -> tuple[str]:
        ...

    def materialize_view(self, view: lea.views.View):
        if isinstance(view, lea.views.SQLView):
            incremental_fields = [field for field in view.fields if field.is_incremental]
            if len(incremental_fields) > 1:
                raise ValueError(
                    f"Multiple incremental fields are not supported (found in {str(self)})"
                )
            elif len(incremental_fields) == 1:
                self.materialize_sql_view_incremental(
                    view, incremental_field_name=incremental_fields[0].name
                )
            else:
                self.materialize_sql_view(view)
        elif isinstance(view, lea.views.PythonView):
            self.materialize_python_view(view)
        elif isinstance(view, lea.views.JSONView):
            self.materialize_json_view(view)
        else:
            raise ValueError(f"Unhandled view type: {view.__class__.__name__}")

    @abc.abstractmethod
    def materialize_sql_view(self, view: lea.views.SQLView):
        ...

    @abc.abstractmethod
    def materialize_sql_view_incremental(
        self, view: lea.views.SQLView, incremental_field_name: str
    ):
        ...

    @abc.abstractmethod
    def materialize_python_view(self, view: lea.views.PythonView):
        ...

    def read_python_view(self, view: lea.views.PythonView) -> pd.Dataframe:
        module_name = view.path.stem
        spec = importlib.util.spec_from_file_location(module_name, view.path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Step 2: Retrieve the variable from the module's namespace
        dataframe = getattr(module, view.key[-1], None)
        if dataframe is None:
            raise ValueError(f"Could not find variable {view.key[1]} in {view.path}")
        return dataframe

    @abc.abstractmethod
    def delete_table_reference(self, table_reference: str):
        ...

    @abc.abstractmethod
    def list_tables(self) -> pd.DataFrame:
        ...

    @abc.abstractmethod
    def list_columns(self) -> pd.DataFrame:
        ...

    def list_existing_view_keys(self) -> set[tuple[str, ...]]:
        tables = self.list_tables()
        return {self._table_reference_to_view_key(table) for table in tables.table_reference}

    def make_column_test_unique(self, view: lea.views.View, column: str) -> str:
        return self.load_assertion_test_template("#UNIQUE").render(
            table=view.table_reference, column=column
        )

    def make_column_test_unique_by(self, view: lea.views.View, column: str, by: str) -> str:
        return self.load_assertion_test_template("#UNIQUE_BY").render(
            table=view.table_reference,
            column=column,
            by=by,
        )

    def make_column_test_no_nulls(self, view: lea.views.View, column: str) -> str:
        return self.load_assertion_test_template("#NO_NULLS").render(
            table=view.table_reference, column=column
        )

    def make_column_test_set(self, view: lea.views.View, column: str, elements: set[str]) -> str:
        schema, *leftover = view.key
        return self.load_assertion_test_template("#SET").render(
            table=view.table_reference,
            column=column,
            elements=elements,
        )

    def load_assertion_test_template(self, tag: str) -> jinja2.Template:
        return jinja2.Template(
            (
                pathlib.Path(__file__).parent / "assertions" / f"{tag.lstrip('#')}.sql.jinja"
            ).read_text()
        )
