#!/usr/bin/env python3
"""Unit tests for utils module."""

import unittest
from parameterized import parameterized
from typing import Any, Mapping, Sequence, Dict
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json


class TestAccessNestedMap(unittest.TestCase):
    """Test case for the access_nested_map function."""

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(
        self, nested_map: Mapping[str, Any], path: Sequence[str], expected: Any
    ) -> None:
        """Test that access_nested_map returns the expected result."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand(
        [
            ({}, ("a",)),
            ({"a": 1}, ("a", "b")),
        ]
    )
    def test_access_nested_map_exception(
        self, nested_map: Mapping[str, Any], path: Sequence[str]
    ) -> None:
        """Test that access_nested_map raises KeyError with correct message."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), repr(path[-1]))


class TestGetJson(unittest.TestCase):
    """Test case for the get_json function."""

    @parameterized.expand(
        [
            ("http://example.com", {"payload": True}),
            ("http://holberton.io", {"payload": False}),
        ]
    )
    def test_get_json(self, test_url: str, test_payload: Dict[str, Any]) -> None:
        """Test that get_json returns expected payload from mocked response."""
        with patch("utils.requests.get") as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)

            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test case for the memoize decorator function."""

    def test_memoize(self) -> None:
        """Test that memoize caches the result of a method."""

        class TestClass:
            """Class with a method and memoized property."""

            def a_method(self) -> int:
                """Return a constant integer."""
                return 42

            @memoize
            def a_property(self) -> int:
                """Call a_method and cache its result."""
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mocked:
            obj = TestClass()
            result1 = obj.a_property
            result2 = obj.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mocked.assert_called_once()
