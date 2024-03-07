from unittest.mock import MagicMock

from django.test import RequestFactory

import pytest
from watson import search

from giant_search.views import SearchView


@pytest.mark.django_db
class TestSearchView:
    def test_get_queryset(self, monkeypatch):
        monkeypatch.setattr(search, "filter", lambda a, b: [MagicMock(path="test")])
        monkeypatch.setattr(search, "search", lambda a, models, exclude: [MagicMock(path="test")])
        view = SearchView()
        view.query = "test"
        view.request = RequestFactory().get("/")
        queryset_list = view.get_queryset()
        assert len(queryset_list) == 1
