from __future__ import annotations

from typing import TYPE_CHECKING

from ...domain.models import Text, Upload, Validation

if TYPE_CHECKING:
    from collections.abc import Iterable

    from ..models import TextORM, UploadORM, ValidationORM


def text_orm_to_model(
    orm: TextORM,
) -> Text:
    return Text(
        text_id=orm.text_id,
        upload_id=orm.upload_id,
        status=orm.status,
        content=orm.content,
        predicted_label=orm.predicted_label,
    )

def text_orms_to_models(
    orms: Iterable[TextORM],
) -> tuple[Text, ...]:
    return tuple(text_orm_to_model(orm) for orm in orms)

def upload_orm_to_model(
    orm: UploadORM,
) -> Upload:
    return Upload(
        upload_id=orm.upload_id,
        uploaded_at=orm.uploaded_at,
        status=orm.status,
        filename=orm.filename,
        has_validation=orm.has_validation,
    )

def upload_orms_to_models(
    orms: Iterable[UploadORM],
) -> tuple[Upload, ...]:
    return tuple(upload_orm_to_model(orm) for orm in orms)

def validation_orm_to_model(
    orm: ValidationORM,
) -> Validation:
    return Validation(
        validation_id=orm.validation_id,
        text_id=orm.text_id,
        label=orm.label,
    )

def validation_orms_to_models(
    orms: Iterable[ValidationORM],
) -> tuple[Validation, ...]:
    return tuple(validation_orm_to_model(orm) for orm in orms)
