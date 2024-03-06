from zipfile import ZipFile

from w.services.technical.filesystem_service import FilesystemService
from w.services.technical.zip_service import ZipService
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestZipService(TestCaseMixin):
    @classmethod
    def setup_class(cls):
        super().setup_class()
        pdf_file = "pdf/exemple_pdf.pdf"
        txt_file = "filesystem/dir1/file1.txt"
        cls.files_to_zip = {
            pdf_file: FilesystemService.read_binary_file(
                cls.get_datasets_dir(pdf_file)
            ),
            txt_file: FilesystemService.read_file(cls.get_datasets_dir(txt_file)),
        }

    def setup_method(self):
        ZipService.clear()
        self.clean_sandbox()

    """
    zip2memory
    """

    def test_zip2memory_with_success_return_zip_bytes(self):
        actual = ZipService.zip2memory(self.files_to_zip)
        zip_file = self.get_sandbox_dir("success.zip")
        FilesystemService.write_binary_file(zip_file, actual)
        extract_dir = self.get_sandbox_dir("extracted_in")
        FilesystemService.check_file_can_be_created(extract_dir)
        with ZipFile(zip_file, "r") as zip:
            zip.extractall(extract_dir)
        for file in self.files_to_zip.keys():
            self.assert_file_exists(self.get_sandbox_dir(f"extracted_in/{file}"))
