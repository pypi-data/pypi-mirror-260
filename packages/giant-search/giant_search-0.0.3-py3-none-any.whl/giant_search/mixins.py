from django.db.models import QuerySet


class SearchableMixin:
    @classmethod
    def get_search_queryset(cls) -> QuerySet:
        """
        Override this method to provide your own Queryset to be indexed.
        For example, for some models, you might use cls.objects.published() or apply filters etc.

        This is a class method as we won't have an instance of the model when registering it with search.
        """

        return cls.objects.all()

    @staticmethod
    def get_search_fields() -> tuple:
        """
        Override this method to provide a tuple containing the fields to search.
        If the method returns an empty tuple, all text fields will be indexed as per Watson's defaults.
        """

        return tuple()

    @property
    def is_searchable(self):
        """
        This always needs to return True in order for the model that implements this Mixin to be searchable.
        """

        return True

    def get_search_result_title(self) -> str:
        """
        By default, get_search_result_title() will return the string representation of the model as defined in __str__.
        Override this method to provide a different search result title.
        """

        return str(self)

    def get_search_result_description(self) -> str:
        """
        By default, get_search_result_description() returns an empty string. If you want to define a description, for
        example if your model has a description field, you could override get_search_result_description() to provide it.
        """

        return ""

    def get_search_result_url(self):
        """
        Define how to get the URL that the search result should point to.

        By default, we attempt to call get_absolute_url on the object. If your model doesn't implement this method, or
        needs something more complex, you must override this property method.
        """

        try:
            return self.get_absolute_url()
        except AttributeError:
            # Fallback to returning an empty string since the URL field on the SearchResult model is not nullable.
            # Note that we will filter out any search results that don't have a valid URL because they're pointless.
            return ""

    def get_search_result_category(self) -> str:
        """
        By default, the search result category is the human readable name of the Model, but of course, you can override
        this by overriding this property method on your model.
        """

        return self._meta.object_name
