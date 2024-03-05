from .module_imports import *


@headers({"Ocp-Apim-Subscription-Key": key})
class _Oracle_Knowledge_Management(Consumer):
    """Inteface to Oracle knowledge management resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    @returns.json
    @http_get("oracle/content/articles/{answer_id}")
    def get_article(
        self,
        answer_id: str
    ):
        """This call will return the Oracle knowledge base article for the specified answer id."""

    @returns.json
    @http_get("oracle/search/question/")
    def get_search_results(
        self,
        question: Query(type=str),
        facet: Query(type=str) = None,
        include_multi_facets: Query(type=bool) = None,
    ):
        """This call will return search results from Oracle knowledge management"""
