"""A client for interacting with the API.

This module provides a client class for interacting with the API, including
indexing documents, listing them, deleting them, get S3 URL to a document,
querying them and extracting structured json data from text.

Classes:
    APIClient: Client for interacting with the API.
"""

import os
import json
import io
from typing import List, Optional, Literal, Tuple, Union
from urllib.parse import urljoin
import requests

from .schema import (
    UploadFileResponse,
    GetFileS3Reponse,
    FilterRequest,
    FilterDocStoreReponse,
    DeleteDocResponse,
    QueryRequest,
    QueryResponse,
    DataExtractRequest,
    DataExtractResponse,
    ChatMessage,
    LogIndexationTable,
)


class APIClient:
    """Client for interacting with the API.

    This class provides methods for interacting with the API, including
    indexing documents, listing them, deleting them, get S3 URL to a document,
    querying them and extracting structured json data from text.

    Attributes:
        url: The base URL for the API.
        api-key: The api key for the API.
        upload_docs_endpoint: The endpoint for uploading.
        filter_docs_endpoint: The endpoint for filtering.
        delete_docs_endpoint: The endpoint for deleting.
        get_file_s3_endpoint: The endpoint for getting file URL from s3.
        query_endpoint: The endpoint for querying.
        extract_json_data_endpoint: The endpoint for extracting JSON data from text.
    """

    def __init__(self, url: str, api_key: str):
        """Initializes the API client with the given URL and the API key.

        Args:
            url: The base URL for the API.
            api_key: The api key for the API.

        Usage:
        ```python
        from pythia_client.client import APIClient
        client = APIClient("http://localhost:8000", "api-key")
        ```
        """
        self.url = url
        self.api_key = api_key
        self.upload_docs_endpoint = urljoin(str(self.url), "file-upload")
        self.indexing_jobs_endpoint = urljoin(str(self.url), "indexing-jobs")
        self.filter_docs_endpoint = urljoin(str(self.url), "documents/get_by_filters")
        self.delete_docs_endpoint = urljoin(
            str(self.url), "documents/delete_by_filters"
        )
        self.get_file_s3_endpoint = urljoin(str(self.url), "documents/get")
        self.query_endpoint = urljoin(str(self.url), "query")
        self.extract_json_data_endpoint = urljoin(str(self.url), "structured_output")

    def _query(self, request: QueryRequest) -> QueryResponse | None:
        """Queries the API.

        Args:
            request: The request object containing the query data.

        Returns:
            The response from the API as a Pydantic model. You can use response.model_dump() to get a Dict. Returns None if the status code is not 200.
        """
        with requests.Session() as session:
            payload = json.loads(request.model_dump_json())
            headers = {
                "accept": "application/json",
                "Content-Type": "application/json",
                "X-API-Key": self.api_key,
            }
            with session.post(
                self.query_endpoint, headers=headers, json=payload
            ) as response:
                if response.status_code == 200:
                    return QueryResponse(**response.json())
                else:
                    return None

    def query(
        self,
        query: str,
        chat_history: Optional[List[ChatMessage]] = None,
        filters: Optional[FilterRequest] = None,
        group_id: str = None,
    ) -> QueryResponse:
        """Query the API with a user question to get a LLM-generated answer based
            on context from the document store.

            Args:
                query: The user question to be answered.
                chat_history: The chat history to provide context to the model. Should be a list of ChatMessage objects.
                filters: Haystack 2.0 filter dict. See: https://docs.haystack.deepset.ai/v2.0/docs/metadata-filtering#filters for more information about how to build a filter.
                group_id: The name of the group_id the client making the request, for logging in DynamoDB. Defaults to "api".

            Returns:
                The response from the API as a Pydantic model. You can use reponse.model_dump() to get a Dict. Returns None if the status code is not 200.

            Usage:
            ```python
            filters = {
                        "operator": "AND",
                        "conditions": [
                            {
                                "field": "meta.source",
                                "operator": "==",
                                "value": "Salesforce",
                            },
                        ],
                    }
            query_response = client.query("Hey how are you", filters=filters)
            query_response.model_dump()
            ```
            Can also be used with chat history:
            ```python
            chat_history = [
                {
                    "content": "Hello Chatbot. My name is Corentin !",
                    "role": "user",
                    "name": None,
                    "meta": {},
                }
            ]
            response = client.query(
                query="Given our previous exchange of messages, what is my name ?",
                chat_history=chat_history,
            )
        ```
        """
        filters = FilterRequest(filters=filters).model_dump()
        filters["group_id"] = group_id if group_id else "api"
        request = QueryRequest(
            query=query,
            chat_history=chat_history,
            params=filters,
        )
        response = self._query(request)

        return response

    def index_files(
        self,
        files: List[Union[str, Tuple[str, io.IOBase]]],
        meta: Optional[List[dict]] = None,
        indexation_mode: Literal["unstructured", "pypdf"] = "unstructured",
    ) -> UploadFileResponse:
        """Index one or multiples files (documents) to the document store through the Haystack-API upload-file endpoint.

        Args:
            files: The paths to the files OR tuples of filename and file object to index.
            meta: The list of metadata for the files.
            indexation_mode: The indexation mode between unstructured and pypdf.

        Returns:
            The response from the API. Returns None if the status code is not 202.

        Usage:
        ```python
        index_response = client.index_files(["path/to/file.pdf"], meta=[{"source": "Salesforce"}], indexation_mode="pypdf")
        {"message": "Files Submitted. Indexing task created."}
        index_response = client.index_files([("file.pdf", file)], meta=[{"source": "Salesforce"}], indexation_mode="pypdf")
        {"message": "Files Submitted. Indexing task created."}
        ```
        """
        prepared_files = []
        for file in files:
            if isinstance(file, str):
                file_name = os.path.basename(file)
                with open(file, "rb") as f:
                    file_content = f.read()
            elif (
                isinstance(file, tuple)
                and len(file) == 2
                and isinstance(file[1], io.IOBase)
            ):
                file_name, file_object = file
                file_content = file_object.read()
            else:
                raise ValueError(
                    "Each file must be a file path or a tuple of (filename, fileIObyte)"
                )

            prepared_files.append(("files", (file_name, file_content)))

        with requests.Session() as session:
            payload = {"meta": json.dumps(meta), "indexation_mode": indexation_mode}
            headers = {
                "X-API-Key": self.api_key,
            }
            with session.post(
                self.upload_docs_endpoint,
                files=prepared_files,
                data=payload,
                headers=headers,
            ) as response:
                if response.status_code == 202:
                    api_response = response.json()
                else:
                    api_response = None
        return api_response

    def get_indexing_jobs(self, group_id: str, top: int = 20) -> List[dict]:
        """Get the indexing jobs from the API.

        Args:
            group_id: The name of the group_id the client making the request, for logging in DynamoDB. If none, the default group_id is "api" (set by the API itself).
            top: The number of top most recent indexing jobs to return.

        Returns:
            The response from the API. Returns None if the status code is not 200.

        Usage:
        ```python
        indexing_jobs = client.get_indexing_jobs(group_id="api", top=20)
        indexing_jobs.model_dump()
        ```
        """
        with requests.Session() as session:
            params = {"top": top}
            headers = {
                "X-API-Key": self.api_key,
            }
            with session.get(
                self.indexing_jobs_endpoint + "/" + group_id,
                params=params,
                headers=headers,
            ) as response:
                if response.status_code == 200:
                    api_response = [
                        LogIndexationTable(**resp) for resp in response.json()
                    ]
                else:
                    api_response = None
        return api_response

    def _list_docs(
        self, request: FilterRequest, return_content: bool = False
    ) -> List[FilterDocStoreReponse] | None:
        """List all documents in the document store that match the filter provided.

        Args:
            request: The request object containing the filter data.
            return_content: If True, the content of the documents will be returned.

        Returns:
            The response from the API as a Pydantic model. You can use response.model_dump() to get a Dict. Returns None if the status code is not 200.
        """
        with requests.Session() as session:
            payload = json.loads(request.model_dump_json())
            headers = {
                "accept": "application/json",
                "Content-Type": "application/json",
                "X-API-Key": self.api_key,
            }
            if return_content:
                endpoint = f"{self.filter_docs_endpoint}?return_content=true"
            else:
                endpoint = self.filter_docs_endpoint

            with session.post(endpoint, headers=headers, json=payload) as response:
                if response.status_code == 200:
                    responses = response.json()
                    return [FilterDocStoreReponse(**resp) for resp in responses]
                else:
                    return None

    def list_docs(
        self,
        filters: FilterRequest = None,
        return_content: bool = False,
    ) -> List[FilterDocStoreReponse]:
        """List all documents in the document store that match the filter provided.

        Args:
            filters: Haystack 2.0 filter dict. See: https://docs.haystack.deepset.ai/v2.0/docs/metadata-filtering#filters for more information about how to build a filter.
            return_content: If True, the content of the documents will be returned.

        Returns:
            The response from the API. Returns None if the status code is not 200.

        Usage:
        ```python
        filters = {
                    "operator": "AND",
                    "conditions": [
                        {
                            "field": "meta.source",
                            "operator": "==",
                            "value": "Salesforce",
                        },
                    ],
                }
        list_response = client.list_docs(filters=filters)
        list_response.model_dump()
        ```
        """
        request = FilterRequest(filters=filters)
        response = self._list_docs(request, return_content=return_content)

        return response

    def _remove_docs(self, request: FilterRequest) -> DeleteDocResponse | None:
        """Remove documents from the API document store.

        Args:
            request: The request object containing the filter data.

        Returns:
            The response from the API as a Pydantic model. You can use response.model_dump() to get a Dict.
        """
        with requests.Session() as session:
            payload = json.loads(request.model_dump_json())
            headers = {
                "accept": "application/json",
                "Content-Type": "application/json",
                "X-API-Key": self.api_key,
            }
            with session.post(
                self.delete_docs_endpoint, headers=headers, json=payload
            ) as response:
                if response.status_code == 200:
                    return DeleteDocResponse(**response.json())
                else:
                    return None

    def remove_docs(
        self,
        filters: FilterRequest = None,
    ) -> DeleteDocResponse:
        """Remove documents from the API document store.

        Args:
            filters: Haystack 2.0 filter dict. See: https://docs.haystack.deepset.ai/v2.0/docs/metadata-filtering#filters for more information about how to build a filter.

        Returns:
            The response from the API as a Pydantic model. You can use reponse.model_dump() to get a Dict. Returns None if the status code is not 200.
        Usage:
        ```python
        filters = {
                    "operator": "AND",
                    "conditions": [
                        {
                            "field": "meta.source",
                            "operator": "==",
                            "value": "Salesforce",
                        },
                    ],
                }
        remove_response = client.remove_docs(filters=filters)
        remove_response.model_dump()
        ```
        """
        request = FilterRequest(filters=filters)
        response = self._remove_docs(request)

        return response

    def get_doc_url(self, filename: str, page: Optional[int] = 1) -> GetFileS3Reponse:
        """Get a presigned URL to a file located on S3.

        Args:
            filename: The filename of the file to get.
            page: The page to directly point the URL.

        Returns:
            The response from the API as a Pydantic model. You can use reponse.model_dump() to get a Dict. Returns None if the status code is not 200.

        Usage:
        ```python
        get_doc_response = client.get_doc_url("s3fd_sample.pdf", page=2)
        s3_url = get_doc_response.url
        ```
        """
        with requests.Session() as session:
            params = {"page": page}
            url = f"{self.get_file_s3_endpoint}/{filename}"
            headers = {
                "X-API-Key": self.api_key,
            }
            with session.get(
                url,
                params=params,
                headers=headers,
            ) as response:
                if response.status_code == 200:
                    api_response = GetFileS3Reponse(**response.json())
                else:
                    api_response = None
        return api_response

    def _extract_json_data(
        self, request: DataExtractRequest
    ) -> DataExtractResponse | None:
        """Query the API to extract structured JSON from unstructured text.

        Args:
            request: The request object containing the query data.

        Returns:
            The response from the API as a Pydantic model. You can use response.model_dump() to get a Dict.
        """
        with requests.Session() as session:
            payload = json.loads(request.model_dump_json())
            headers = {
                "accept": "application/json",
                "Content-Type": "application/json",
                "X-API-Key": self.api_key,
            }
            with session.post(
                self.extract_json_data_endpoint, headers=headers, json=payload
            ) as response:
                if response.status_code == 200:
                    return DataExtractResponse(**response.json())
                else:
                    return None

    def extract_json_data(
        self,
        text_content: str,
    ) -> DataExtractResponse:
        """Query the API to extract structured JSON from unstructured text.

        Args:
            text_content: The text to process.

        Returns:
            The response from the API as a Pydantic model. You can use reponse.model_dump() to get a Dict. Returns None if the status code is not 200.

        Usage:
        ```python
        extract_response = client.extract_json_data("Hello I want to modify the delivery date of order FR73681920")
        extract_response.model_dump()
        ```
        """
        request = DataExtractRequest(
            email_content=text_content,
        )
        response = self._extract_json_data(request)

        return response
