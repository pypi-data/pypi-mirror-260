from typing import List

from verba_interface.document import Document as VerbaDocument


class DocumentProcessor:
    def process_documents(self, documents: List[VerbaDocument]) -> List[VerbaDocument]:
        raise NotImplementedError
