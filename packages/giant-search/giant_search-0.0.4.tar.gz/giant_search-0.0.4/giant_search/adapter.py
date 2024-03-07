import json
from typing import final

from django.core.serializers.json import DjangoJSONEncoder
from django.utils.html import strip_tags
from watson.search import SearchAdapter

from giant_search.utils import is_page_title, is_cms_plugin


@final
class GiantSearchAdapter(SearchAdapter):
    """
    This adapter allows us to define how we populate the title, description, URL and other fields on the Watson
    SearchResult instances.

    Each method assumes that the model set on this Adapter class implements the SearchableMixin.
    """

    def get_title(self, obj):
        """
        Returns the title of this search result.
        This is given high priority in search result ranking.

        You can access the title of the search entry as `entry.title` in your search results.
        """

        # As a starting point, use the model's string representation.
        title = str(obj)

        # If the model is a Django CMS Page Title model use the title field.
        if is_page_title(obj):
            title = obj.title

        # If the model is a Django CMS Plugin model, we can try to get the Page title.
        if is_cms_plugin(obj):
            try:
                title = obj.page.get_page_title()
            except AttributeError:
                pass

        try:
            title = obj.get_search_result_title()
        except AttributeError:
            pass

        return strip_tags(title[:1000])

    def get_description(self, obj):
        """
        Returns the description of this search result.
        This is given medium priority in search result ranking.

        You can access the description of the search entry as `entry.description`
        in your search results. Since this should contains a short description of the search entry,
        it's excellent for providing a summary in your search results.
        """

        if is_page_title(obj):
            # If the object is a Page Title, return right away since it can't implement get_search_result_description.
            return strip_tags(obj.meta_description) or ""

        try:
            return strip_tags(obj.get_search_result_description())
        except AttributeError:
            return ""

    def get_url(self, obj):
        """
        Get the URL of this search result.
        """

        url = ""

        # First, try to get the value from the object's get_absolute_url method.
        try:
            url = obj.get_absolute_url()
        except AttributeError:
            pass

        # If the model is a Django CMS Page Title model or a Plugin, try to get the URL from the Page.
        if is_page_title(obj) or is_cms_plugin(obj):
            try:
                url = obj.page.get_absolute_url()
            except AttributeError:
                pass

        # Finally, we check to see if the model has implemented get_search_result_url, and if so, use that.
        try:
            url = obj.get_search_result_url()
        except AttributeError:
            pass

        return url

    def serialize_meta(self, obj):
        """
        Implement the serialize_meta method in order to get some useful information about our search result and put it
        into the search result object for use on the front end.

        If you want to add some data here, please ensure that you update the SearchableMixin to provide a default
        value for it.
        """

        category = ""

        if is_page_title(obj):
            # If this Model is a Django CMS Title instance, we tell a lie and say that it is a Page because that makes
            # more sense for end users.
            category = "Page"

        try:
            category = obj.get_search_result_category()
        except AttributeError:
            pass

        meta_obj = {"category": category}
        return json.dumps(meta_obj, cls=DjangoJSONEncoder)
