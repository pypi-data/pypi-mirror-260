import os
from typing import List
from injectable import injectable, Autowired, autowired
from PyPDF2 import PdfFileReader
import io
import pdf2image
import tempfile
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from tekleo_common_utils.utils_file import UtilsFile


@injectable
class UtilsPdf:
    @autowired
    def __init__(self, utils_file: Autowired(UtilsFile)):
        self.utils_file = utils_file

    def get_number_of_pages_from_path(self, pdf_file_path: str) -> int:
        reader = PdfFileReader(pdf_file_path)
        return reader.getNumPages()

    def get_number_of_pages_from_bytes(self, pdf_bytes) -> int:
        reader = PdfFileReader(io.BytesIO(pdf_bytes))
        return reader.getNumPages()

    def render_from_bytes_to_image_paths_all_pages(self, pdf_bytes, dpi: int = 300, output_image_format: str = "png", thread_count: int = 1) -> List[str]:
        temp_folder = tempfile.gettempdir()
        page_image_paths = pdf2image.convert_from_bytes(pdf_bytes, dpi=dpi, output_folder=temp_folder, fmt=output_image_format, paths_only=True, thread_count=thread_count)
        return page_image_paths

    def render_from_bytes_to_image_paths_single_page(self, pdf_bytes, page_number: int, dpi: int = 300, output_image_format: str = "png") -> str:
        temp_folder = tempfile.gettempdir()
        page_image_paths = pdf2image.convert_from_bytes(pdf_bytes, dpi=dpi, output_folder=temp_folder, fmt=output_image_format, paths_only=True, thread_count=1, first_page=page_number, last_page=page_number)
        return page_image_paths[0]

    def render_from_bytes_to_image_paths(self, pdf_bytes, first_page_number: int, last_page_number: int, dpi: int = 300, output_image_format: str = "png", thread_count: int = 1) -> List[str]:
        temp_folder = tempfile.gettempdir()
        page_image_paths = pdf2image.convert_from_bytes(pdf_bytes, dpi=dpi, output_folder=temp_folder, fmt=output_image_format, paths_only=True, thread_count=thread_count, first_page=first_page_number, last_page=last_page_number)
        return page_image_paths

    def convert_to_images(self, pdf_file_path: str, output_folder: str, dpi: int = 300, output_image_format: str = "png", thread_count: int = 1) -> List[str]:
        # Build file name
        pdf_file_name = pdf_file_path.split("/")[-1].replace(".pdf", "")

        # Read the file
        pdf_bytes = self.utils_file.open_file_to_bytes(pdf_file_path)

        # Render the file
        page_image_paths = self.render_from_bytes_to_image_paths_all_pages(pdf_bytes, dpi=dpi, output_image_format=output_image_format, thread_count=thread_count)

        # Move pages from temp to permanent location
        new_page_image_paths = []
        for page_image_path in page_image_paths:
            # Build new path
            new_page_image_path = page_image_path.split("/")[-1]
            new_page_image_path = new_page_image_path.split("-")[-1]
            new_page_image_path = output_folder + "/" + pdf_file_name + "-" + new_page_image_path

            # Move the image
            os.rename(page_image_path, new_page_image_path)
            new_page_image_paths.append(new_page_image_path)

        # Return results
        return new_page_image_paths

    def convert_to_texts(self, pdf_file_path: str) -> List[List[str]]:
        number_of_pages = self.get_number_of_pages_from_path(pdf_file_path)
        pages = []
        for page_number in range(1, number_of_pages + 1):
            paragraphs = self.convert_to_texts_single_page(pdf_file_path, page_number)
            pages.append(paragraphs)
        return pages

    def convert_to_texts_single_page(self, pdf_file_path: str, page_number: int) -> List[str]:
        page_index = page_number + 1
        infile = open(pdf_file_path, 'rb')
        output = io.StringIO()
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, laparams=LAParams())
        interpreter = PDFPageInterpreter(manager, converter)
        for page in PDFPage.get_pages(infile, [page_index]):
            interpreter.process_page(page)
        text = output.getvalue()
        infile.close()
        converter.close()
        paragraph_texts = text.split("\n\n")
        paragraph_texts = [t.replace("\n", " ").replace("  ", " ").strip() for t in paragraph_texts]
        return paragraph_texts
