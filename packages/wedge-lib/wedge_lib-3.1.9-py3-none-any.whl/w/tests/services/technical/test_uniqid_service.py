from w.services.technical.uniqid_service import UniqIdService
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestUniqIdService(TestCaseMixin):
    @classmethod
    def setup_class(cls):
        super().setup_class()

    def setup_method(self, func):
        UniqIdService.clear()

    """
    get
    """

    def test_get_with_success_return_uniq_id(self):
        uniq_id = UniqIdService.get()
        uniq_id2 = UniqIdService.get()
        assert uniq_id != uniq_id2
        assert len(uniq_id) == 36
        assert len(uniq_id2) == 36
        part = uniq_id.split("-")
        assert len(part) == 5

    """
    set_fake_generator
    """

    def test_set_fake_generator_with_success_return_none(self):
        UniqIdService.set_fake_generator()

        for i in range(1, 3):
            uniq_id = UniqIdService.get()
            assert uniq_id == f"00000000000000000000000{i}"
