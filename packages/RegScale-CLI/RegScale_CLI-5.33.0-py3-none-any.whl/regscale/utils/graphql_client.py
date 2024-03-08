"""
A module for making paginated GraphQL queries.
"""

import json
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from typing import List, Dict, Optional, Any
from gql.transport.requests import log as requests_logger
import logging
from regscale.core.app.utils.app_utils import create_progress_object

logger = logging.getLogger(__name__)


class PaginatedGraphQLClient:
    """
    A class for making paginated GraphQL queries.
    """

    def __init__(
        self,
        endpoint: str,
        query: str,
        headers: Optional[Dict[str, str]] = None,
        logging_level: str = logging.CRITICAL,
    ) -> None:
        """
        Initializes the client with the GraphQL endpoint, query, and default number of results per page.

        Args:
            endpoint: The URL of the GraphQL endpoint.
            query: The GraphQL query string.
            headers: Optional headers to include in the request.
            logging_level: The logging level for the client (default: 'CRITICAL').
        """
        self.log_level = logging_level
        self.endpoint = endpoint
        self.query = gql(query)
        self.headers = headers or {}  # Ensure headers are a dictionary
        self.transport = RequestsHTTPTransport(url=endpoint, headers=self.headers)
        self.client = Client(transport=self.transport)
        self.job_progress = create_progress_object()
        requests_logger.setLevel(level=self.log_level)

    def fetch_all(
        self,
        topic_key: str,
        variables: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetches all results from the paginated query.

        Args:
            topic_key: The key to the topic in the response.
            variables: Optional query variables.

        Returns:
             Dict[str, Any].
        """
        self.job_progress.add_task("[#f68d1f]Fetching data...", total=None)
        results = []
        next_cursor = None
        has_next_page = True
        page_info_default = {"hasNextPage": False, "endCursor": None}
        with self.job_progress:
            while has_next_page:
                data = self.fetch_page(variables=variables, after=next_cursor)
                if data:
                    results.extend(data.get(topic_key, {}).get("nodes", []))
                    page_info = data.get(topic_key, {}).get(
                        "pageInfo", page_info_default
                    )
                    logger.info(f"pageInfo: {page_info}")
                    has_next_page = page_info.get("hasNextPage", False)
                    next_cursor = page_info.get("endCursor", None)
                    if not has_next_page:
                        break
                else:
                    break
            return results

    def fetch_page(
        self, variables: Optional[Dict[str, Any]] = None, after: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Fetches a single page of results.

        Args:
            variables: Optional query variables.
            after: The cursor for pagination (optional, defaults to None for the first page).

        Returns:
            A dictionary containing the fetched page of results and pagination information.
        """
        variables = variables or {}
        variables["after"] = after

        result = self.client.execute(self.query, variable_values=variables)
        return result
