"""Module containing the Data Store Collection related classes."""
from __future__ import annotations

import json
import re
from functools import total_ordering
from typing import TYPE_CHECKING
from xml.etree import ElementTree

import requests

if TYPE_CHECKING:  # pragma: no cover
    import sys
    from typing import Any, Optional

    if sys.version_info < (3, 9):
        from typing import Generator, Mapping, MutableMapping, Pattern
    else:
        from collections.abc import Mapping, MutableMapping, Generator
        from re import Pattern
    from eumdac.datastore import DataStore
    from eumdac.product import Product

from eumdac.errors import EumdacError, eumdac_raise_for_status
from eumdac.request import get
import eumdac.common


class SearchResults:
    """Iterable results for a search of a given Data Store collection.

    Usage:
    >>> results = collection.search(parameters)
    >>> number_found = results.total_results
    >>> for product in results:
    >>>     print(product)

    Attributes
    ----------
    collection: Collection

    Parameters
    ----------
    total_results: int
        Number of total results in the search.
    query: dict
        Query parameters for the search.

    Methods
    -------
    update_query(**query): SearchResults
        Perform a new search updating the current params with `query` and return its results. Does not modify this instance.
    first: Product
        Return the first product of the search.
    """

    collection: Collection
    _query: MutableMapping[str, Optional[str]]
    _total_results: Optional[int] = None
    _items_per_page: int = 100

    def __init__(self, collection: Collection, query: Mapping[str, Any]) -> None:
        """Init the SearchResults for searching 'collection' based on 'query'.

        Does not perform the search yet.
        """

        self.collection = collection
        self.query = query  # type: ignore[assignment]

    def __contains__(self, product: Product) -> bool:
        """Return true if 'product' is among the search results.

        Iterates over the whole result set in the worst case.
        """

        # if this is used more often, maybe better implement a bisection
        # on page loading to find the product
        for item in self.__iter__():
            if product == item:
                return True
        return False

    def __iter__(self) -> Generator[Product, None, None]:
        """Iterate the found products, querying the next page if needed."""
        params = self._get_request_params()
        page_json = self._load_page(params)
        self._total_results = int(page_json["totalResults"])
        yield from self._yield_products(page_json)
        for start_index in range(self._items_per_page, self._total_results, self._items_per_page):
            params["si"] = start_index
            page_json = self._load_page(params)
            yield from self._yield_products(page_json)

    def __len__(self) -> int:
        """Return total results."""
        return self.total_results

    def __repr__(self) -> str:
        """Represent the search as `collection` and `query` performed."""
        return f"{self.__class__}({self.collection}, {self.query})"

    @property
    def total_results(self) -> int:
        """Number of total results in the search."""
        if self._total_results is None:
            params = self._get_request_params()
            params["c"] = 0
            page_json = self._load_page(params)
            self._total_results = int(page_json["totalResults"])
        return self._total_results

    @property
    def query(self) -> MutableMapping[str, Optional[str]]:
        """Query performed to get the search results."""
        return {**self._query}

    @query.setter
    def query(self, query: Mapping[str, Any]) -> None:
        """Set the query terms."""
        valid_keys = set(self.collection.search_options)
        new_keys = set(query)
        diff = new_keys.difference(valid_keys)
        if diff:
            raise CollectionError(f"invalid search options {diff}, valid options are {valid_keys}")
        self._query = {
            key: None if query.get(key) is None else str(query.get(key)) for key in valid_keys
        }
        if hasattr(query.get("dtstart"), "isoformat"):
            self._query["dtstart"] = query["dtstart"].isoformat()
        if hasattr(query.get("dtend"), "isoformat"):
            self._query["dtend"] = query["dtend"].isoformat()

    def first(self) -> Optional[Product]:
        """Return the first product of the search."""
        params = self._get_request_params()
        params["c"] = 1
        page_json = self._load_page(params)
        self._total_results = page_json["totalResults"]
        if self._total_results == 0:
            return None
        return next(self._yield_products(page_json))

    def update_query(self, **query: Any) -> SearchResults:
        """Perform a new search updating the current params with `query` and return its results. Does not modify this instance."""
        new_query = {**self._query, **query}
        return SearchResults(self.collection, new_query)

    def _load_page(
        self, params: Mapping[str, Any], session: Optional[requests.Session] = None
    ) -> MutableMapping[str, Any]:
        """Fetch the next page of the search."""
        auth = self.collection.datastore.token.auth
        url = self.collection.datastore.urls.get("datastore", "search")
        session = None
        if session is None:
            response = get(
                url,
                params=params,
                auth=auth,
                headers=eumdac.common.headers,
            )
        else:
            response = session.get(url, params=params, auth=auth, headers=eumdac.common.headers)
        eumdac_raise_for_status(
            f"Search query load page failed for {self.collection} with {self._query}",
            response,
            CollectionError,
        )
        return response.json()

    def _yield_products(self, page_json: Mapping[str, Any]) -> Generator[Product, None, None]:
        """Return all products."""
        collection_id = str(self.collection)
        for feature in page_json["features"]:
            product_id = feature["id"]
            product = self.collection.datastore.get_product(collection_id, product_id)
            yield product

    def _get_request_params(self) -> MutableMapping[str, Any]:
        """Build the search request parameters from 'query'."""
        return {
            "format": "json",
            "pi": str(self.collection),
            "si": 0,
            "c": self._items_per_page,
            **{key: value for key, value in self._query.items() if value is not None},
        }


@total_ordering
class Collection:
    """Collection from Data Store.

    Provides access to the collection metadata and allows performing searches of its products.

    Attributes
    ----------
    datastore: DataStore

    Properties
    ----------
    abstract: str
        Detailed description of the collection products.
    title: str
    medatadata: dict
    product_type: str
    search_options: dict
        Dictionary of available search options for the collection.

    Methods
    -------
    search(**query): SearchResults
        Perform a product search inside the collection
    """

    _id: str
    datastore: DataStore
    _geometry: Optional[Mapping[str, Any]] = None
    _properties: Optional[Mapping[str, Any]] = None
    _search_options: Optional[Mapping[str, Any]] = None
    # Title and abstract come with squences of whitespace in the text.
    # We use this regex to substitue them with a normal space.
    _whitespaces: Pattern[str] = re.compile(r"\s+")

    def __init__(self, collection_id: str, datastore: DataStore) -> None:
        """Init the collection.

        Arguments
        ---------
        collection_id: str
            Id of the collection in Data Store.
        datastore: DataStore
            Reference to Data Store.
        """

        self._id = collection_id
        self.datastore = datastore

    def __str__(self) -> str:
        return self._id

    def __repr__(self) -> str:
        return f"{self.__class__}({self._id})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self._id == other._id

    def __lt__(self, other: Collection) -> bool:
        return self._id < other._id

    def _ensure_properties(self) -> None:
        """Fetch properties from Data Store, unless they were already requested."""
        if self._properties is not None:
            return
        url = self.datastore.urls.get(
            "datastore", "browse collection", vars={"collection_id": self._id}
        )
        auth = self.datastore.token.auth
        response = get(
            url,
            params={"format": "json"},
            auth=auth,
            headers=eumdac.common.headers,
        )
        eumdac_raise_for_status(
            f"Could not get properties of {self._id}", response, CollectionError
        )
        geometry = response.json()["collection"]["geometry"]
        properties = response.json()["collection"]["properties"]
        properties.pop("links")
        self._geometry = geometry
        self._properties = properties
        title = properties["title"]
        abstract = properties["abstract"]
        self._properties["title"] = self._whitespaces.sub(" ", title)  # type: ignore[index]
        self._properties["abstract"] = self._whitespaces.sub(" ", abstract)  # type: ignore[index]

    @property
    def abstract(self) -> str:
        """Detailed description of the collection products."""
        self._ensure_properties()
        return str(self._properties["abstract"])  # type: ignore[index]

    @property
    def title(self) -> str:
        """Collection title."""
        self._ensure_properties()
        return str(self._properties["title"])  # type: ignore[index]

    @property
    def metadata(self) -> Mapping[str, Any]:
        """Collection metadata."""
        self._ensure_properties()
        return {
            "geometry": self._geometry.copy(),  # type: ignore[union-attr]
            "properties": self._properties.copy(),  # type: ignore[union-attr]
        }

    @property
    def product_type(self) -> Optional[str]:
        """Product type."""
        self._ensure_properties()
        auth = self.datastore.token.auth
        url = self.datastore.urls.get("tailor", "products")
        response = get(
            url,
            auth=auth,
            headers=eumdac.common.headers,
        )
        eumdac_raise_for_status(f"Could not get search product type", response, CollectionError)
        api_response = json.loads(response.text)

        collection_ids = [i["pn_id"] for i in api_response["data"]]
        product_types = [i["id"] for i in api_response["data"]]
        product_types_dict = dict(zip(product_types, collection_ids))

        for key, value in product_types_dict.items():
            if type(value) == list:
                if self._id in value:
                    return key
            else:
                if self._id == value:
                    return key
        return None

    def search(self, **query: Any) -> SearchResults:
        """Product search inside the collection.

        Note: search parameters differ depending on the collection
        they can be listed with the property search_options
        """
        return SearchResults(self, query)

    @property
    def search_options(self) -> Mapping[str, Any]:
        """Dictionary of available search options for the collection."""
        if self._search_options is None:
            # load remote options
            # this lines may change when the new version of DT offers
            # a way to load collection specific options
            url_static = self.datastore.urls.get("datastore", "search options")
            url = url_static + "?pi=" + self._id
            auth = self.datastore.token.auth
            response = get(
                url,
                auth=auth,
                headers=eumdac.common.headers,
            )
            eumdac_raise_for_status(
                f"Could not get search options for {self._id}", response, CollectionError
            )
            root = ElementTree.fromstring(response.text)
            (element,) = [
                ele
                for ele in root
                if ele.tag.endswith("Url") and ele.get("type") == "application/json"
            ]
            self._search_options = {
                str(e.get("name")): {
                    "title": e.get("title"),
                    "options": [o.get("value") for o in e],
                }
                for e in element
                # remove options controlled by SearchResults
                if e.get("name") not in ["format", "pi", "si", "c", "id", "pw"]
                and e.get("name") is not None
            }
        return self._search_options


class CollectionError(EumdacError):
    """Errors related to collections"""
