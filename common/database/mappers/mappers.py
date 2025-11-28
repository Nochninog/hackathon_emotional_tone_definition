from ...domain.models import Text, Upload, Validation
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
        upload=upload_orm_to_model(orm.upload) if orm.upload is not None else None,
        validation=validation_orm_to_model(orm.validation) if orm.validation is not None else None,
    )


def upload_orm_to_model(
    orm: UploadORM,
) -> Upload:
    return Upload(
        upload_id=orm.upload_id,
        uploaded_at=orm.uploaded_at,
        status=orm.status,
        filename=orm.filename,
        has_validation=orm.has_validation,
        texts=[
            text_orm_to_model(text_orm)
            for text_orm in orm.texts
        ] if orm.texts is not None else None,
    )


def validation_orm_to_model(
    orm: ValidationORM,
) -> Validation:
    return Validation(
        validation_id=orm.validation_id,
        text_id=orm.text_id,
        label=orm.label,
        text=text_orm_to_model(orm.text) if orm.text is not None else None,
    )