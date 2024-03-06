import pytest
from django.conf import settings
from django.test import override_settings
from io import BytesIO

from w.services.technical.boto3_service import Boto3Service
from w.tests.mixins.boto3test_mixin import Boto3TestMixin
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestBoto3Service(TestCaseMixin, Boto3TestMixin):

    """
    init
    """

    def test_init_service_with_invalid_credentials_return_runtime_error(self):
        for key in [
            "AWS_ACCESS_KEY_ID",
            "AWS_SECRET_ACCESS_KEY",
            "AWS_STORAGE_BUCKET_NAME",
        ]:
            new_setting = {key: None}
            with override_settings(**new_setting):
                with pytest.raises(
                    RuntimeError, match=f"Please set {key} in your settings"
                ):
                    Boto3Service.init()

    def test_init_service_with_good_credentials_return_none(self):
        assert Boto3Service._s3_client is not None
        assert Boto3Service._s3_resource is not None

    """
    create_bucket_if_not_exist
    """

    def test_create_bucket_if_not_exist_with_not_initialize_service_raise_runtime_error(
        self,
    ):
        Boto3Service.clear()
        with pytest.raises(RuntimeError, match="Boto3Service not initialized"):
            Boto3Service.create_bucket_if_not_exist()

    def test_create_bucket_if_not_exist_with_bucket_return_none(self):
        Boto3Service.clear()
        with override_settings(AWS_STORAGE_BUCKET_NAME="bucket-name"):
            Boto3Service.init()
            Boto3Service.create_bucket_if_not_exist()
            buckets = [b.name for b in Boto3Service._s3_resource.buckets.all()]
            assert settings.AWS_STORAGE_BUCKET_NAME in buckets

    """
    is_bucket_exists
    """

    def test_is_bucket_exists_with_not_initialize_service_raise_runtime_error(self):
        Boto3Service.clear()
        with pytest.raises(RuntimeError, match="Boto3Service not initialized"):
            Boto3Service.is_bucket_exists()

    def test_is_bucket_exists_with_not_exists_return_false(self):
        with override_settings(AWS_STORAGE_BUCKET_NAME="not_exists"):
            assert Boto3Service.is_bucket_exists() is False

    def test_is_bucket_exists_with_success_return_true(self):
        with override_settings(AWS_STORAGE_BUCKET_NAME="bucket-name"):
            Boto3Service.create_bucket_if_not_exist()
            assert Boto3Service.is_bucket_exists() is True

    """
    delete_bucket
    """

    def test_delete_bucket_with_not_initialize_service_raise_runtime_error(self):
        Boto3Service.clear()
        with pytest.raises(RuntimeError, match="Boto3Service not initialized"):
            Boto3Service.delete_bucket()

    def test_delete_bucket_with_success_return_none(self):
        with override_settings(AWS_STORAGE_BUCKET_NAME="bucket-name"):
            Boto3Service.create_bucket_if_not_exist()
            Boto3Service.reset_bucket()
            Boto3Service.delete_bucket()
            assert Boto3Service.is_bucket_exists() is False

    """
    reset_bucket
    """

    def test_reset_bucket_with_not_initialize_service_raise_runtime_error(self):
        Boto3Service.clear()
        with pytest.raises(RuntimeError, match="Boto3Service not initialized"):
            Boto3Service.reset_bucket()

    def test_reset_bucket_with_not_exists_bucket_return_none(self):
        with override_settings(AWS_STORAGE_BUCKET_NAME="not-exists"):
            assert Boto3Service.reset_bucket() is None

    def test_reset_bucket_with_success_return_none(self):
        file_path = self.get_datasets_dir("s3_file/recapitulatif_mensuel.pdf")
        destination_path = "path/in/remote/recapitulatif_mensuel.pdf"
        with override_settings(AWS_STORAGE_BUCKET_NAME="bucket-name"):
            with open(file_path, "rb") as file:
                pdf_data = file.read()
                Boto3Service.create_bucket_if_not_exist()
                Boto3Service.upload(
                    file=BytesIO(pdf_data),
                    destination_path=destination_path,
                )
                assert Boto3Service.is_bucket_empty() is False
                Boto3Service.reset_bucket()
                assert Boto3Service.is_bucket_empty() is True

    """
    is_bucket_empty
    """

    def test_is_bucket_empty_with_not_initialize_service_raise_runtime_error(self):
        Boto3Service.clear()
        with pytest.raises(RuntimeError, match="Boto3Service not initialized"):
            Boto3Service.is_bucket_empty()

    def test_is_bucket_empty_with_empty_bucket_return_true(self):
        with override_settings(AWS_STORAGE_BUCKET_NAME="bucket-name"):
            Boto3Service.create_bucket_if_not_exist()
            Boto3Service.reset_bucket()
            assert Boto3Service.is_bucket_empty() is True

    def test_is_bucket_empty_with_filled_bucket_return_false(self):
        file_path = self.get_datasets_dir("s3_file/recapitulatif_mensuel.pdf")
        destination_path = "path/in/remote/recapitulatif_mensuel.pdf"
        with override_settings(AWS_STORAGE_BUCKET_NAME="bucket-name"):
            with open(file_path, "rb") as file:
                pdf_data = file.read()
                Boto3Service.create_bucket_if_not_exist()
                Boto3Service.upload(
                    BytesIO(pdf_data), destination_path=destination_path
                )
                assert Boto3Service.is_bucket_empty() is False

    """
    upload
    """

    def test_upload_with_not_initialize_service_raise_runtime_error(self):
        file_path = self.get_datasets_dir("s3_file/recapitulatif_mensuel.pdf")
        destination_path = "path/in/remote/recapitulatif_mensuel.pdf"
        Boto3Service.clear()
        with override_settings(AWS_STORAGE_BUCKET_NAME="bucket-name"):
            with pytest.raises(RuntimeError, match="Boto3Service not initialized"):
                with open(file_path, "rb") as file:
                    pdf_data = file.read()
                    Boto3Service.upload(
                        BytesIO(pdf_data), destination_path=destination_path
                    )

    def test_upload_with_success_return_none(self):
        file_path = self.get_datasets_dir("s3_file/recapitulatif_mensuel.pdf")
        destination_path = self.get_sandbox_dir(
            "path/in/remote/recapitulatif_mensuel.pdf"
        )
        with override_settings(AWS_STORAGE_BUCKET_NAME="bucket-name"):
            Boto3Service.create_bucket_if_not_exist()
            assert Boto3Service.is_file_exists(destination_path) is False
            with open(file_path, "rb") as file:
                pdf_data = file.read()
                Boto3Service.upload(
                    BytesIO(pdf_data), destination_path=destination_path
                )
            assert Boto3Service.is_file_exists(destination_path) is True

    """
    is_file_exists
    """

    def test_is_file_exists_with_not_initialize_service_raise_runtime_error(self):
        Boto3Service.clear()
        destination_path = self.get_sandbox_dir(
            "path/in/remote/recapitulatif_mensuel.pdf"
        )
        with pytest.raises(RuntimeError, match="Boto3Service not initialized"):
            Boto3Service.is_file_exists(destination_path)

    def test_is_file_exists_with_success_return_true(self):
        file_path = self.get_datasets_dir("s3_file/recapitulatif_mensuel.pdf")
        destination_path = self.get_sandbox_dir(
            "path/in/remote/recapitulatif_mensuel.pdf"
        )
        with override_settings(AWS_STORAGE_BUCKET_NAME="bucket-name"):
            Boto3Service.create_bucket_if_not_exist()
            assert Boto3Service.is_file_exists(destination_path) is False
            with open(file_path, "rb") as file:
                pdf_data = file.read()
                Boto3Service.upload(
                    BytesIO(pdf_data), destination_path=destination_path
                )
            assert Boto3Service.is_file_exists(destination_path) is True

    def test_is_file_exists_with_no_file_return_false(self):
        with override_settings(AWS_STORAGE_BUCKET_NAME="bucket-name"):
            Boto3Service.create_bucket_if_not_exist()
            assert Boto3Service.is_file_exists("no_file.pdf") is False

    """
    generate_signed_url
    """

    def test_generate_signed_url_with_not_initialize_service_raise_runtime_error(self):
        Boto3Service.clear()
        file_path = self.get_datasets_dir("s3_file/recapitulatif_mensuel.pdf")
        with pytest.raises(RuntimeError, match="Boto3Service not initialized"):
            Boto3Service.generate_signed_url(file_path)

    def test_generate_signed_url_with_success_return_url(self):
        file_path = self.get_datasets_dir("s3_file/recapitulatif_mensuel.pdf")
        destination_path = self.get_sandbox_dir(
            "path/in/remote/recapitulatif_mensuel.pdf"
        )
        with override_settings(AWS_STORAGE_BUCKET_NAME="bucket-name"):
            Boto3Service.create_bucket_if_not_exist()
            with open(file_path, "rb") as file:
                pdf_data = file.read()
                Boto3Service.upload(
                    BytesIO(pdf_data), destination_path=destination_path
                )
                signed_url = Boto3Service.generate_signed_url(file_path=file_path)
                assert signed_url is not None
