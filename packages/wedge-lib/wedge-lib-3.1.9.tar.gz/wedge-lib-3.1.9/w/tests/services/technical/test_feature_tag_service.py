import pytest
from django.test import override_settings

from w.services.technical.feature_tag_service import FeatureTagService
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestFeatureTagService(TestCaseMixin):
    @classmethod
    def setup_class(cls):
        super().setup_class()

    def setup_method(self):
        FeatureTagService.clear()

    """
    is_enabled
    """

    def test_is_enabled_with_missing_var_env_return_false(self):
        assert FeatureTagService.is_enabled("my-feature") is False

    def test_is_enabled_with_unknown_feature_raise_runtime_exception(self):
        match = "feature 'my-unknown-feature' not found in settings FEATURE_TAGS"
        with pytest.raises(RuntimeError, match=match):
            with override_settings(FEATURE_TAGS={"my-feature": False}):
                FeatureTagService.is_enabled("my-unknown-feature")

    def test_is_enabled_with_disabled_return_false(self):
        with override_settings(FEATURE_TAGS={"my-feature": "0"}):
            assert FeatureTagService.is_enabled("my-feature") is False

    def test_is_enabled_with_enabled_return_true(self):
        with override_settings(FEATURE_TAGS={"my-feature": "1"}):
            assert FeatureTagService.is_enabled("my-feature") is True

    """
    is_disabled
    """

    def test_is_disabled_with_missing_var_env_return_true(self):
        assert FeatureTagService.is_disabled("my-feature") is True

    def test_is_disabled_with_unknown_feature_raise_runtime_exception(self):
        match = "feature 'my-unknown-feature' not found in settings FEATURE_TAGS"
        with pytest.raises(RuntimeError, match=match):
            with override_settings(FEATURE_TAGS={"my-feature": False}):
                FeatureTagService.is_disabled("my-unknown-feature")

    def test_is_disabled_with_disabled_return_true(self):
        with override_settings(FEATURE_TAGS={"my-feature": "0"}):
            assert FeatureTagService.is_disabled("my-feature") is True

    def test_is_disabled_with_enabled_return_false(self):
        with override_settings(FEATURE_TAGS={"my-feature": "1"}):
            assert FeatureTagService.is_disabled("my-feature") is False
