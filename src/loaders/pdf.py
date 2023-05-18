from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

from loaders.base import Loader


class PdfLloader(Loader):
    def __init__(self, url):
        self.name = "pdf"
        super().__init__(url)

    def run(pdf_path: str) -> str:
        resource_manager = PDFResourceManager()
        return_string = StringIO()
        codec = "utf-8"
        laparams = LAParams()
        device = TextConverter(
            resource_manager, return_string, codec=codec, laparams=laparams
        )
        interpreter = PDFPageInterpreter(resource_manager, device)

        with open(pdf_path, "rb") as file:
            for page in PDFPage.get_pages(file, check_extractable=True):
                interpreter.process_page(page)

        text = return_string.getvalue()
        device.close()
        return_string.close()

        return text
