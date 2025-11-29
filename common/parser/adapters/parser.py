from io import BytesIO

import pandas as pd

from ...adapters.parser import IUploadParser, TextItem, TextItemWithValidation


class PandasCsvUploadParser(IUploadParser):
    def parse_upload_file(self, file_bytes: bytes) -> tuple[TextItem, ...]:
        df = pd.read_csv(BytesIO(file_bytes))
        return tuple(
            TextItem(
                text=row["text"],
                src=row["src"],
            ) for row in df.to_dict(orient="records")
        )

    def parse_upload_file_with_validation(
        self,
        file_bytes: bytes,
    ) -> tuple[TextItemWithValidation, ...]:
        df = pd.read_csv(BytesIO(file_bytes))
        return tuple(
            TextItemWithValidation(
                text=row["text"],
                src=row["src"],
                label=row["label"]
            ) for row in df.to_dict(orient="records")
        )

