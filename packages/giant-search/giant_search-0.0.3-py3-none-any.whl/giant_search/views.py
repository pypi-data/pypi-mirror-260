from watson.views import SearchView as WatsonSearchView

from giant_search.utils import SearchResultDeduplicator


class SearchView(WatsonSearchView):
    template_name = "search/results.html"

    def get_queryset(self):
        queryset = super().get_queryset().exclude(url="")
        return SearchResultDeduplicator(queryset).deduplicate()
