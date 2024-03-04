from django.db.models import Field, QuerySet
from django.db.models.expressions import Func
from django.db.models.aggregates import Aggregate


class Annotation:

    def __init__(
            self,
            verbose_name: str,
            field: type[Field],
            function: type[Func] | type[Aggregate],
            help_text: str = '',
            **kwargs
    ):
        self.verbose_name = verbose_name or self
        self.field = field
        self.function = function
        self.help_text = help_text
        self.__dict__.update(kwargs)


class AnnotationModelMixin:

    @classmethod
    def get_annotations(cls) -> list[dict]:
        return list({'name': a, 'annotation': getattr(cls, a)} for a in filter(
            lambda a:
            not a.startswith('__')
            and isinstance(getattr(cls, a), Annotation),
            cls.__dict__
        ))


class AnnotationManagerMixin:

    @staticmethod
    def add_annotations(queryset: QuerySet):
        model = queryset.model
        if not hasattr(model, 'get_annotations'):
            return queryset
        return queryset.annotate(**{
            annotation['name']: annotation['annotation'].function
            for annotation in model.get_annotations()
        })

