from watson.search import register


def register_for_search(model, **field_overrides):
    """
    Registers a given model with Watson using the Giant Search Adapter.
    """

    from giant_search.adapter import GiantSearchAdapter
    register(model, adapter_cls=GiantSearchAdapter, **field_overrides)


def is_page_title(obj):
    """
    Determine if the given object is a Django CMS Page Title model instance.
    """

    from cms.models import Title
    return isinstance(obj, Title)


def is_cms_plugin(obj):
    """
    Determine if the given object is a Django CMS Plugin model instance.
    """

    from cms.models import CMSPlugin
    return isinstance(obj, CMSPlugin)


class SearchResultDeduplicator:
    def __init__(self, queryset):
        self.queryset = queryset
        self.seen_urls = []

    def deduplicate(self):
        """
        Ensures that the QuerySet does not contain multiple results for the same URL.
        """

        queryset = self.queryset

        for result in queryset:
            url = result.url
            if not self._is_valid_url(url):
                self.queryset = self.queryset.exclude(pk=result.pk)
            # Add the URL for this result to the seen URLs list so we don't add it again.
            self.seen_urls.append(url.strip("/"))

        return self.queryset

    def _is_valid_url(self, url):
        """
        Ensures that the URL given is valid and has not already been processed.
        """

        if not url or url.strip("/") in self.seen_urls:
            return False

        return True
