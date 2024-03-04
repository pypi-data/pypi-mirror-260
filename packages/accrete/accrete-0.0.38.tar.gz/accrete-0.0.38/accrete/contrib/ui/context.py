import logging
from dataclasses import dataclass, field
from typing import TypedDict
from django.utils.translation import gettext_lazy as _t
from django.db import models
from django.db.models import Model, QuerySet
from django.core.paginator import Paginator
from django.core import paginator
from django.forms import Form, ModelForm
from accrete.utils.models import get_related_model
from accrete.annotation import Annotation
from .elements import (
    ClientAction, BreadCrumb, TableField, TableFieldType, TableFieldAlignment
)
from .filter import Filter


_logger = logging.getLogger(__name__)

DEFAULT_PAGINATE_BY = 40


class DetailPagination(TypedDict):
    previous_object_url: str
    next_object_url: str
    current_object_idx: int
    total_objects: int


@dataclass(kw_only=True)
class Context:

    title: str = ''
    breadcrumbs: list[BreadCrumb] = field(default_factory=list)
    actions: list[ClientAction] = field(default_factory=list)
    kwargs: dict = field(default_factory=dict)

    def __post_init__(self):
        for key, value in self.kwargs.items():
            setattr(self, key, value)

    def dict(self):
        return {
            attr: getattr(self, attr, '') for attr
            in filter(lambda x: not x.startswith('_'), self.__dict__)
        }


@dataclass
class TableContext(Context):

    object_label: str
    fields: list[TableField]
    list_page: paginator.Page
    pagination_param_str: str
    endless_scroll: bool
    filter: Filter
    object_param_str: str = field(default='', kw_only=True)


@dataclass
class ListContext(Context):

    object_label: str
    object_param_str: str
    list_page: paginator.Page
    pagination_param_str: str
    filter: Filter
    endless_scroll: bool = True
    column_height: int = 4
    column_width: int = 12

    def __post_init__(self):
        super().__post_init__()
        if self.column_width not in range(1, 13):
            _logger.warning(
                'ListContext parameter column_width should be in range 1 - 12'
            )


class DetailContext(TypedDict, total=False):

    title: str
    object: Model
    breadcrumbs: list[BreadCrumb]
    detail_page: DetailPagination
    pagination_param_str: str
    actions: list[ClientAction]


class FormContext(TypedDict, total=False):

    title: str
    breadcrumbs: list[BreadCrumb]
    form: Form | ModelForm
    form_id: str
    actions: list[ClientAction]


def cast_param(params: dict, param: str, cast_to: callable, default):
    if param not in params:
        return default
    try:
        return cast_to(params.get(param, default))
    except Exception as e:
        _logger.exception(e)
        return default


def prepare_url_params(get_params: dict) -> dict:
    return {key: f'&{key}={value}' for key, value in get_params.items()}


def url_param_str(params: dict, extract: list[str] = None) -> str:
    """
    Return a URL Querystring from the given parameters
    If extract is supplied, extract the value from the dictionary and prepare
    them, so that each value is formatted e.g. {'page': '&page=1'}
    """
    if extract:
        params = prepare_url_params(extract_url_params(params, extract))
    param_str = (
        "".join(str(value) for value in params.values())
        .replace('&&', '&')
        .replace('?&', '?')
        .strip('?&')
    )
    return f'?{param_str}'


def extract_url_params(params: dict, keys: list[str]) -> dict:
    return {key: params[key] for key in keys if key in params}


def exclude_params(params: dict, keys: list[str]) -> dict:
    return {key: val for key, val in params.items() if key not in keys}


def list_page(queryset: QuerySet, paginate_by: int, page_number: int) -> paginator.Page:
    pages = Paginator(queryset, per_page=paginate_by)
    return pages.page(page_number <= pages.num_pages and page_number or pages.num_pages)


def detail_page(queryset: QuerySet, obj: Model) -> dict:
    if not hasattr(obj, 'get_absolute_url'):
        _logger.warning(
            'Detail pagination disabled for models without the '
            'get_absolute_url attribute. Set paginate_by to 0 to '
            'deactivate pagination.'
        )
        return {}
    idx = (*queryset,).index(obj)
    previous_object_url = (
        queryset[idx - 1] if idx - 1 >= 0 else queryset.last()
    ).get_absolute_url()
    next_object_url = (
        queryset[idx + 1] if idx + 1 <= queryset.count() - 1 else queryset.first()
    ).get_absolute_url()
    return {
        'previous_object_url': previous_object_url,
        'next_object_url': next_object_url,
        'current_object_idx': idx + 1,
        'total_objects': queryset.count()
    }


def form_actions(discard_url: str, form_id: str = 'form') -> list[ClientAction]:
    return [
        ClientAction(
            name=_t('Save'),
            submit=True,
            class_list=['is-success'],
            form_id=form_id,
        ),
        ClientAction(
            name=_t('Discard'),
            url=discard_url
        )
    ]


def get_table_fields(
        fields: list[str],
        model: type[Model],
        field_definition: dict[str | TableField] = None
) -> list[TableField]:

    def get_alignment(field_attr):
        number_field_types = (
            models.DecimalField, models.IntegerField, models.FloatField
        )
        if (
                isinstance(field_attr, number_field_types)
                or (
                isinstance(field_attr, Annotation)
                and field_attr.field in number_field_types
        )):
            return TableFieldAlignment.RIGHT
        return TableFieldAlignment.LEFT


    def get_field_definition(f_name: str) -> TableField:
        if definition := field_definition.get(f_name):
            return definition
        parts = f_name.split('__')
        if len(parts) == 1:
            rel_model = model
            names = [rel_model._meta.verbose_name]
        else:
            rel_model, names = get_related_model(model, f_name)
        try:
            return rel_model.table_field_definition[parts[-1]]
        except (AttributeError, KeyError):
            attr = getattr(rel_model, parts[-1])
            if isinstance(attr, Annotation):
                pass
            elif hasattr(attr, 'field'):
                attr = attr.field
        names.append(attr.verbose_name)
        return TableField(
            label=' / '.join([str(name) for name in names[1:]]),
            name=f_name,
            header_info=str(attr.help_text),
            truncate_after=50,
            alignment=get_alignment(attr)
        )

    if field_definition is None:
        field_definition = {}

    table_fields = []
    for field_name in fields:
        try:
            table_fields.append(get_field_definition(field_name))
        except AttributeError as e:
            print(e)
            pass
    return table_fields
