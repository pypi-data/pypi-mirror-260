from typing import List

from verba_interface.document import Document as VerbaDocument


class DocumentImporter:
    def import_documents(self, documents: List[VerbaDocument]) -> None:
        raise NotImplementedError
