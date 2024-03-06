from threading import Thread
from time import sleep

import pytest

from w.exceptions import NotFoundError
from w.services.technical.context_service import ContextService
from w.tests.fixtures.datasets.builders.context.contexts import FakeContext
from w.tests.mixins.testcase_mixin import TestCaseMixin


class TestContextService(TestCaseMixin):
    @classmethod
    def setup_class(cls):
        super().setup_class()

    # noinspection PyMethodMayBeStatic
    def setup_method(self):
        ContextService.clear()

    """
    register
    """

    def test_register_with_invalid_context_raise_runtime_error(self):
        match = "Invalid context, you should inherit from BaseContext"
        with pytest.raises(RuntimeError, match=match):
            # noinspection PyTypeChecker
            ContextService.register("invalid", "invalid context")

    def test_register_with_success_return_none(self):
        context = FakeContext("Allo quoi ?!")
        assert ContextService.register("fake", context) is None

    """
    get
    """

    def test_get_with_key_notexists_return_none(self):
        assert ContextService.get("fake") is None

    def test_get_with_success_return_context(self):
        context = FakeContext("Allo quoi ?!")
        ContextService.register("fake", context)
        actual = ContextService.get("fake")
        assert actual.to_dict() == context.to_dict()

    def test_get_with_key_notexists_in_current_thread_return_none(self):
        def thread_with_register():
            context = FakeContext("fake other thread context")
            ContextService.register("fake", context)
            sleep(0.05)
            assert ContextService.get("fake") == context

        # process1 is the current test :)
        process2 = Thread(target=thread_with_register)
        process2.start()
        assert ContextService.get("fake") is None

    def test_get_is_thread_safe(self):
        def assert_is_thread_safe(key, context, sleep_time):
            ContextService.register(key, context)
            sleep(sleep_time)
            assert ContextService.get(key) == context

        context = FakeContext("thread1-key1")
        context2 = FakeContext("thread2-key1")
        context3 = FakeContext("thread3-key2")
        context4 = FakeContext("thread4-key1")
        ContextService.register("key2", FakeContext("thread1-key2"))
        process2 = Thread(target=assert_is_thread_safe, args=("key1", context2, 0.02))
        process3 = Thread(target=assert_is_thread_safe, args=("key2", context3, 0.05))
        process4 = Thread(target=assert_is_thread_safe, args=("key1", context4, 0.03))
        process2.start()
        process3.start()
        ContextService.register("key1", context)
        process4.start()
        assert ContextService.get("key1") == context
        sleep(0.15)
        assert len(ContextService._registry.keys()) == 4
        ContextService.register("key3", FakeContext("thread1-key3"))
        assert len(ContextService._registry.keys()) == 1, "no cleaning finished thread"
        self.assert_equals_resultset(
            {
                k: c.to_dict()
                for k, c in ContextService._registry[context.thread_id].items()
            }
        )

    """
    check_exists
    """

    def test_check_exists_with_not_exists_raise_notfound_error(self):
        match = "context 'not-exists' not found"
        with pytest.raises(NotFoundError, match=match):
            ContextService.check_exists("not-exists")

    def test_check_exists_with_success_return_context(self):
        context = FakeContext("Yes it exists!")
        ContextService.register("existingKey", context)
        assert ContextService.check_exists("existingKey") == context
