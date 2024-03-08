import datetime
import json
import os
import uuid
from typing import Any, AsyncGenerator, Dict, Iterable, List, Optional, Sequence, Union

import httpx
from langmem._internal.utils import ID_T
from langmem._internal.utils import as_uuid as _as_uuid
from pydantic import BaseModel
from pydantic.v1 import BaseModel as BaseModelV1

DEFAULT_TIMEOUT = httpx.Timeout(timeout=30.0, connect=10.0)


def _ensure_url(url: Optional[str]) -> str:
    url_ = url or os.environ.get("LANGMEM_API_URL")
    if url_ is None:
        raise ValueError(
            "api_url is required. Please set LANGMEM_API_URL "
            "or manually provided it to the client."
        )
    return url_


def _default_serializer(obj: Any) -> str:
    if isinstance(obj, uuid.UUID):
        return str(obj)
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    if isinstance(obj, BaseModel):
        return json.loads(obj.model_dump_json())
    if isinstance(obj, BaseModelV1):
        return json.loads(obj.json())
    return json.loads(json.dumps(obj, default=_default_serializer))


def raise_for_status_with_text(response: httpx.Response) -> None:
    """Raise an error with the response text."""
    try:
        response.raise_for_status()
    except httpx.HTTPError as e:
        raise httpx.HTTPError(f"{str(e)}: {response.text}") from e


class AsyncClient:
    __slots__ = ["api_key", "client"]

    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("LANGMEM_API_KEY")
        base_url = _ensure_url(api_url)
        self.client = httpx.AsyncClient(
            base_url=base_url,
            headers=self._headers,
            timeout=DEFAULT_TIMEOUT,
        )

    @property
    def _headers(self):
        if self.api_key is None:
            return {}
        return {
            "x-api-key": self.api_key,
        }

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        await self.client.aclose()

    async def create_user(
        self,
        *,
        user_id: ID_T,
        name: str,
        tags: Optional[Sequence[str]] = None,
        metadata: Dict[str, str] = {},
    ) -> Dict[str, Any]:
        """Create a user.

        Args:
            user_id (ID_T): The user's ID.
            name (str): The user's name.
            tags (Optional[Sequence[str]], optional): The user's tags. Defaults to None.
            metadata (Dict[str, str], optional): The user's metadata. Defaults to {}.

        Returns:
            Dict[str, Any]: The user's data.
        """

        data = {
            "id": user_id,
            "name": name,
            "tags": tags,
            "metadata": metadata,
        }
        response = await self.client.post("/users", json=data)

        return response.json()

    async def get_user(self, user_id: ID_T) -> Dict[str, Any]:
        """Get a user.

        Args:
            user_id (ID_T): The user's ID.

        Returns:
            Dict[str, Any]: The user's data.
        """

        response = await self.client.get(f"/users/{_as_uuid(user_id)}")
        raise_for_status_with_text(response)
        return response.json()

    async def update_user(
        self,
        user_id: ID_T,
        *,
        name: Optional[str] = None,
        tags: Optional[Sequence[str]] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Update a user.

        Args:
            user_id (ID_T): The user's ID.
            name (Optional[str], optional): The user's name. Defaults to None.
            tags (Optional[Sequence[str]], optional): The user's tags. Defaults to None.
            metadata (Optional[Dict[str, str]], optional): The user's metadata. Defaults to None.

        Returns:
            Dict[str, Any]: The user's data.
        """

        data = {}
        if name is not None:
            data["name"] = name
        if tags is not None:
            data["tags"] = tags
        if metadata is not None:
            data["metadata"] = metadata
        response = await self.client.patch(f"/users/{_as_uuid(user_id)}", json=data)
        raise_for_status_with_text(response)
        return response.json()

    async def list_users(
        self,
        *,
        name: Optional[Sequence[str]] = None,
        id: Optional[Sequence[ID_T]] = None,
    ) -> List[Dict[str, Any]]:
        """List users.

        Args:
            name (Optional[Sequence[str]], optional): The user's name. Defaults to None.
            id (Optional[Sequence[ID_T]], optional): The user's ID. Defaults to None.

        Returns:
            List[Dict[str, Any]]: The users' data.
        """

        params = {
            "name": name,
            "id": id,
        }

        response = await self.client.post(
            "/users/query",
            json=params,
            headers={"Content-Type": "application/json"},
        )
        raise_for_status_with_text(response)
        return response.json()["users"]

    async def list_user_memory(self, user_id: ID_T) -> List[Dict[str, Any]]:
        """List a user's memory.

        Args:
            user_id (ID_T): The user's ID.

        Returns:
            List[Dict[str, Any]]: The user's memory.
        """

        response = await self.client.get(f"/users/{_as_uuid(user_id)}/memory")
        raise_for_status_with_text(response)
        return response.json()

    async def trigger_all_for_user(self, user_id: ID_T) -> None:
        """Trigger all memory functions for a user.

        Args:
            user_id (ID_T): The user's ID.
        """

        response = await self.client.post(f"/users/{_as_uuid(user_id)}/trigger-all")
        raise_for_status_with_text(response)
        return response.json()

    async def delete_user_memory(
        self,
        *,
        user_id: ID_T,
        memory_function_id: Optional[ID_T] = None,
    ) -> None:
        """Delete a user's memory.

        Args:
            user_id (ID_T): The user's ID.
            memory_function_id (Optional[ID_T], optional): The memory function's ID. Defaults to None.
        """

        response = await self.client.delete(
            f"/users/{_as_uuid(user_id)}/memory/{_as_uuid(memory_function_id)}/state"
        )
        raise_for_status_with_text(response)
        return response.json()

    async def update_user_memory(
        self,
        user_id: ID_T,
        *,
        memory_function_id: ID_T,
        state: dict,
    ) -> None:
        """Update a user's memory.

        Args:
            user_id (ID_T): The user's ID.
            memory_function_id (ID_T): The memory function's ID.
            state (dict): The memory state.
        """
        response = await self.client.put(
            f"/users/{_as_uuid(user_id)}/memory/{_as_uuid(memory_function_id)}/state",
            data=json.dumps(
                {"state": state},
                default=_default_serializer,
            ),
        )
        raise_for_status_with_text(response)
        return response.json()

    async def get_user_memory(
        self,
        user_id: ID_T,
        *,
        memory_function_id: ID_T,
    ) -> dict:
        """Get a user's memory state.

        Args:
            user_id (ID_T): The user's ID.
            memory_function_id (ID_T): The memory function's ID.

        Returns:
            dict: The memory state.
        """
        response = await self.client.get(
            f"/users/{_as_uuid(user_id)}/memory/{_as_uuid(memory_function_id)}/state"
        )
        raise_for_status_with_text(response)
        return response.json()

    async def query_user_memory(
        self,
        user_id: ID_T,
        text: str,
        k: int = 200,
        memory_function_ids: Optional[Sequence[ID_T]] = None,
        weights: Optional[dict] = None,
    ) -> List:
        """Query a user's memory.

        Args:
            user_id (ID_T): The user's ID.
            text (str): The query text.
            k (int, optional): The number of results to return. Defaults to 200.

        Returns:
            List: The query results.
        """
        response = await self.client.post(
            f"/users/{_as_uuid(user_id)}/memory/query",
            data=json.dumps(
                {
                    "text": text,
                    "k": k,
                    "memory_function_ids": memory_function_ids,
                    "weights": weights,
                },
                default=_default_serializer,
            ),
        )
        raise_for_status_with_text(response)
        return response.json()

    async def create_memory_function(
        self,
        parameters: Union[BaseModel, dict],
        *,
        target_type: str = "user_state",
        name: Optional[str] = None,
        description: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        function_id: Optional[ID_T] = None,
    ) -> Dict[str, Any]:
        """Create a memory function.

        Args:
            parameters (Union[BaseModel, dict]): The memory function's parameters.
            target_type (str, optional): The memory function's target type. Defaults to "user_state".
            name (Optional[str], optional): The memory function's name. Defaults to None.
            description (Optional[str], optional): The memory function's description. Defaults to None.
            custom_instructions (Optional[str], optional): The memory function's custom instructions. Defaults to None.
            function_id (Optional[ID_T], optional): The memory function's ID. Defaults to None.

        Returns:
            Dict[str, Any]: The memory function's data.
        """
        if isinstance(parameters, dict):
            params: dict = parameters

        else:
            params = parameters.model_json_schema()

        function_schema = {
            "name": name or params.pop("title", ""),
            "description": description or params.pop("description", ""),
            "parameters": params,
        }

        data = {
            "type": target_type,
            "custom_instructions": custom_instructions,
            "id": str(function_id) if function_id else str(uuid.uuid4()),
            "schema": function_schema,
        }
        response = await self.client.post("/memory-functions", json=data)
        raise_for_status_with_text(response)
        return response.json()

    async def get_memory_function(self, memory_function_id: ID_T) -> Dict[str, Any]:
        """Get a memory function.

        Args:
            memory_function_id (ID_T): The memory function's ID.

        Returns:
            Dict[str, Any]: The memory function's data.
        """

        response = await self.client.get(
            f"/memory-functions/{_as_uuid(memory_function_id)}"
        )
        raise_for_status_with_text(response)
        return response.json()

    async def list_memory_functions(
        self, *, target_type: Optional[Sequence[str]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """List memory functions.

        Args:
            target_type (Sequence[str], optional): The memory function's target type. Defaults to None.

        Returns:
            AsyncGenerator[Dict[str, Any], None]: The memory functions' data.
        """

        body = {}
        if target_type is not None:
            body["target_type"] = (
                [target_type] if isinstance(target_type, str) else target_type
            )
        cursor = None
        while True:
            if cursor is not None:
                body["cursor"] = cursor
            response = await self.client.post("/memory-functions/query", json=body)
            raise_for_status_with_text(response)
            data = response.json()
            for function in data.get("memory_functions", []):
                yield function
            cursor = data.get("next_cursor")
            if cursor is None:
                break

    async def update_memory_function(
        self,
        memory_function_id: ID_T,
        *,
        name: Optional[str] = None,
        schema: Optional[Union[BaseModel, dict]] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update a memory function.

        Args:
            memory_function_id (ID_T): The memory function's ID.
            name (Optional[str], optional): The memory function's name. Defaults to None.
            schema (Optional[Union[BaseModel, dict]], optional): The memory function's schema. Defaults to None.
            description (Optional[str], optional): The memory function's description. Defaults to None.

        Returns:
            Dict[str, Any]: The memory function's data.
        """

        data = {}
        if name is not None:
            data["name"] = name
        if schema is not None:
            data["function"] = (
                schema
                if isinstance(schema, dict)
                else json.loads(schema.model_dump_json())
            )
        if description is not None:
            data["description"] = description
        response = await self.client.patch(
            f"/memory-functions/{_as_uuid(memory_function_id)}", json=data
        )
        raise_for_status_with_text(response)
        return response.json()

    async def create_thread(
        self,
        *,
        thread_id: Optional[ID_T] = None,
        messages: Optional[Sequence[Dict[str, Any]]] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Create a thread.

        Args:
            user_id (ID_T): The thread's ID.
            name (str): The thread's name.
            tags (Optional[Sequence[str]], optional): The thread's tags. Defaults to None.
            metadata (Dict[str, str], optional): The thread's metadata. Defaults to {}.

        Returns:
            Dict[str, Any]: The thread's data.
        """

        data = {
            "id": thread_id,
            "messages": messages,
            "metadata": metadata,
        }
        response = await self.client.post("/threads", json=data)
        raise_for_status_with_text(response)
        return response.json()

    async def add_messages(
        self, thread_id: ID_T, *, messages: Sequence[Dict[str, Any]]
    ) -> None:
        """Add messages to a thread.

        Args:
            thread_id (ID_T): The thread's ID.
            messages (Sequence[Dict[str, Any]]): The messages to add.
        """

        data = {"messages": messages}
        response = await self.client.post(
            f"/threads/{_as_uuid(thread_id)}/add_messages",
            data=json.dumps(data, default=_default_serializer),
        )
        raise_for_status_with_text(response)
        return response.json()

    async def get_thread(self, thread_id: ID_T) -> Dict[str, Any]:
        """Get a thread.

        Args:
            thread_id (ID_T): The thread's ID.

        Returns:
            Dict[str, Any]: The thread's data.
        """

        response = await self.client.get(f"/threads/{_as_uuid(thread_id)}")
        raise_for_status_with_text(response)
        return response.json()

    async def list_threads(self) -> Iterable[Dict[str, Any]]:
        """List threads.

        Returns:
            Iterable[Dict[str, Any]]: The threads' data.
        """

        response = await self.client.get("/threads")
        raise_for_status_with_text(response)
        return response.json()

    async def list_thread_memory(self, thread_id: ID_T) -> List[Dict[str, Any]]:
        """List a thread's memory.

        Args:
            thread_id (ID_T): The thread's ID.

        Returns:
            List[Dict[str, Any]]: The thread's memory.
        """

        response = await self.client.get(f"/threads/{_as_uuid(thread_id)}/memory")
        raise_for_status_with_text(response)
        return response.json()

    async def trigger_all_for_thread(self, thread_id: ID_T) -> None:
        """Trigger all memory functions for a thread.

        Args:
            thread_id (ID_T): The thread's ID.
        """

        response = await self.client.post(f"/threads/{_as_uuid(thread_id)}/trigger-all")
        raise_for_status_with_text(response)
        return response.json()

    async def add_thread_state(
        self, thread_id: ID_T, state: Dict[str, Any], *, key: Optional[str] = None
    ) -> None:
        """Add a thread state.

        Args:
            thread_id (ID_T): The thread's ID.
            state (Dict[str, Any]): The thread state.
        """

        response = await self.client.post(
            f"/threads/{_as_uuid(thread_id)}/thread_state",
            json={"state": state, "key": key},
        )
        raise_for_status_with_text(response)
        return response.json()

    async def get_thread_state(
        self, thread_id: ID_T, *, key: Optional[str] = None
    ) -> dict:
        """Get a thread state.

        Args:
            thread_id (ID_T): The thread's ID.

        Returns:
            GetThreadStateResponse: The thread state.
        """
        response = await self.client.post(
            f"/threads/{_as_uuid(thread_id)}/thread_state/query", json={"key": key}
        )
        raise_for_status_with_text(response)
        return response.json()

    async def list_messages(
        self,
        thread_id: ID_T,
        *,
        page_size: Optional[int] = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """List a thread's messages.

        Args:
            thread_id (ID_T): The thread's ID.
            page_size (Optional[int], optional): The page size. Defaults to None.

        Returns:
            AsyncGenerator[Dict[str, Any], None]: The messages' data.
        """

        params = {}
        if page_size is not None:
            params["page_size"] = page_size
        # Handle pagination for large threads
        cursor = None
        while True:
            if cursor is not None:
                params["cursor"] = cursor
            response = await self.client.get(
                f"/threads/{_as_uuid(thread_id)}/messages", params=params
            )
            raise_for_status_with_text(response)
            data = response.json()
            for message in data.get("messages", []):
                yield message
            cursor = data.get("next_cursor")
            if cursor is None:
                break


class Client:
    __slots__ = ["api_key", "client"]

    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("LANGMEM_API_KEY")
        base_url = _ensure_url(api_url)
        self.client = httpx.Client(
            base_url=base_url,
            headers=Client._get_headers(self.api_key),
            timeout=DEFAULT_TIMEOUT,
        )

    @staticmethod
    def _get_headers(api_key: str):
        if api_key is None:
            return {}
        return {
            "x-api-key": api_key,
        }

    @property
    def _headers(self):
        return self._get_headers(self.api_key)

    def __enter__(self):
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.client.close()

    def create_user(
        self,
        *,
        user_id: ID_T,
        name: str,
        tags: Optional[Sequence[str]] = None,
        metadata: Dict[str, str] = {},
    ) -> Dict[str, Any]:
        """Create a user.

        Args:
            user_id (ID_T): The user's ID.
            name (str): The user's name.
            tags (Optional[Sequence[str]], optional): The user's tags. Defaults to None.
            metadata (Dict[str, str], optional): The user's metadata. Defaults to {}.

        Returns:
            Dict[str, Any]: The user's data.
        """

        data = {
            "id": user_id,
            "name": name,
            "tags": tags,
            "metadata": metadata,
        }
        response = self.client.post("/users", json=data)
        raise_for_status_with_text(response)
        return response.json()

    def get_user(self, user_id: ID_T) -> Dict[str, Any]:
        """Get a user.

        Args:
            user_id (ID_T): The user's ID.

        Returns:
            Dict[str, Any]: The user's data.
        """
        response = self.client.get(f"/users/{_as_uuid(user_id)}")
        raise_for_status_with_text(response)
        return response.json()

    def update_user(
        self,
        user_id: ID_T,
        *,
        name: Optional[str] = None,
        tags: Optional[Sequence[str]] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Update a user.

        Args:
            user_id (ID_T): The user's ID.
            name (Optional[str], optional): The user's name. Defaults to None.
            tags (Optional[Sequence[str]], optional): The user's tags. Defaults to None.
            metadata (Optional[Dict[str, str]], optional): The user's metadata. Defaults to None.

        Returns:
            Dict[str, Any]: The user's data.
        """
        data = {}
        if name is not None:
            data["name"] = name
        if tags is not None:
            data["tags"] = tags
        if metadata is not None:
            data["metadata"] = metadata
        response = self.client.patch(f"/users/{_as_uuid(user_id)}", json=data)
        raise_for_status_with_text(response)
        return response.json()

    def list_users(
        self,
        *,
        name: Optional[Sequence[str]] = None,
        id: Optional[Sequence[ID_T]] = None,
    ) -> Iterable[Dict[str, Any]]:
        """List users.

        Args:
            name (Optional[Sequence[str]], optional): The user's name. Defaults to None.
            id (Optional[Sequence[ID_T]], optional): The user's ID. Defaults to None.

        Returns:
            List[Dict[str, Any]]: The users' data.
        """
        body = {
            "name": name,
            "id": id,
        }
        response = self.client.post(
            "/users/query",
            data=json.dumps(body, default=_default_serializer),
            headers={"Content-Type": "application/json"},
        )
        raise_for_status_with_text(response)
        return response.json()["users"]

    def trigger_all_for_user(self, user_id: ID_T) -> None:
        """Trigger all memory functions for a user.

        Args:
            user_id (ID_T): The user's ID.
        """
        response = self.client.post(f"/users/{_as_uuid(user_id)}/trigger-all")
        raise_for_status_with_text(response)
        return response.json()

    def delete_user_memory(
        self,
        *,
        user_id: ID_T,
        memory_function_id: Optional[ID_T] = None,
    ) -> None:
        """Delete a user's memory.

        Args:
            user_id (ID_T): The user's ID.
            memory_function_id (Optional[ID_T], optional): The memory function's ID. Defaults to None.
        """
        response = self.client.delete(
            f"/users/{_as_uuid(user_id)}/memory/{_as_uuid(memory_function_id)}/state"
        )
        raise_for_status_with_text(response)
        return response.json()

    def update_user_memory(
        self,
        user_id: ID_T,
        *,
        memory_function_id: ID_T,
        state: dict,
    ) -> None:
        """Update a user's memory.

        Args:
            user_id (ID_T): The user's ID.
            memory_function_id (ID_T): The memory function's ID.
            state (dict): The memory state.
        """
        response = self.client.put(
            f"/users/{_as_uuid(user_id)}/memory/{_as_uuid(memory_function_id)}/state",
            data=json.dumps(
                {"state": state},
                default=_default_serializer,
            ),
        )
        raise_for_status_with_text(response)
        return response.json()

    def get_user_memory(
        self,
        user_id: ID_T,
        *,
        memory_function_id: ID_T,
    ) -> dict:
        """Get a user's memory state.

        Args:
            user_id (ID_T): The user's ID.
            memory_function_id (ID_T): The memory function's ID.

        Returns:
            dict: The memory state.
        """
        response = self.client.get(
            f"/users/{_as_uuid(user_id)}/memory/{_as_uuid(memory_function_id)}/state"
        )
        raise_for_status_with_text(response)
        return response.json()

    def query_user_memory(
        self,
        user_id: ID_T,
        text: str,
        k: int = 200,
        memory_function_ids: Optional[Sequence[ID_T]] = None,
        weights: Optional[dict] = None,
    ) -> List:
        """Query a user's memory.

        Args:
            user_id (ID_T): The user's ID.
            text (str): The query text.
            k (int, optional): The number of results to return. Defaults to 200.

        Returns:
            List: The query results.
        """
        response = self.client.post(
            f"/users/{_as_uuid(user_id)}/memory/query",
            data=json.dumps(
                {
                    "text": text,
                    "k": k,
                    "memory_function_ids": memory_function_ids,
                    "weights": weights,
                },
                default=_default_serializer,
            ),
        )
        raise_for_status_with_text(response)
        return response.json()

    def create_memory_function(
        self,
        parameters: Union[BaseModel, dict],
        *,
        target_type: str = "user_state",
        name: Optional[str] = None,
        description: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        function_id: Optional[ID_T] = None,
    ) -> Dict[str, Any]:
        """Create a memory function.

        Args:
            parameters (Union[BaseModel, dict]): The memory function's parameters.
            target_type (str, optional): The memory function's target type. Defaults to "user_state".
            name (Optional[str], optional): The memory function's name. Defaults to None.
            description (Optional[str], optional): The memory function's description. Defaults to None.
            custom_instructions (Optional[str], optional): The memory function's custom instructions. Defaults to None.
            function_id (Optional[ID_T], optional): The memory function's ID. Defaults to None.

        Returns:
            Dict[str, Any]: The memory function's data.
        """
        if isinstance(parameters, dict):
            params = parameters
        else:
            params = parameters.model_json_schema()
        function_schema = {
            "name": name or params.pop("title", ""),
            "description": description or params.pop("description", ""),
            "parameters": params,
        }
        data = {
            "type": target_type,
            "custom_instructions": custom_instructions,
            "id": function_id or str(uuid.uuid4()),
            "schema": function_schema,
        }
        response = self.client.post("/memory-functions", json=data)
        raise_for_status_with_text(response)
        return response.json()

    def get_memory_function(self, memory_function_id: ID_T) -> Dict[str, Any]:
        """Get a memory function.

        Args:
            memory_function_id (ID_T): The memory function's ID.

        Returns:
            Dict[str, Any]: The memory function's data.
        """
        response = self.client.get(f"/memory-functions/{_as_uuid(memory_function_id)}")
        raise_for_status_with_text(response)
        return response.json()

    def list_memory_functions(
        self, *, target_type: Optional[Sequence[str]] = None
    ) -> Iterable[Dict[str, Any]]:
        """List memory functions.

        Args:
            target_type (Sequence[str], optional): The memory function's target type. Defaults to None.

        Returns:
            List[Dict[str, Any]]: The memory functions' data.
        """
        body = {}
        if target_type is not None:
            body["target_type"] = (
                [target_type] if isinstance(target_type, str) else target_type
            )
        cursor = None
        while True:
            if cursor is not None:
                body["cursor"] = cursor
            response = self.client.post("/memory-functions/query", json=body)
            raise_for_status_with_text(response)
            data = response.json()
            for function in data.get("memory_functions", []):
                yield function
            cursor = data.get("next_cursor")
            if cursor is None:
                break

    def update_memory_function(
        self,
        memory_function_id: ID_T,
        *,
        name: Optional[str] = None,
        schema: Optional[Union[BaseModel, dict]] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update a memory function.

        Args:
            memory_function_id (ID_T): The memory function's ID.
            name (Optional[str], optional): The memory function's name. Defaults to None.
            schema (Optional[Union[BaseModel, dict]], optional): The memory function's schema. Defaults to None.
            description (Optional[str], optional): The memory function's description. Defaults to None.

        Returns:
            Dict[str, Any]: The memory function's data.
        """
        data: dict = {}
        if name is not None:
            data["name"] = name
        if schema is not None:
            if isinstance(schema, dict):
                data["schema"] = schema
            else:
                data["schema"] = schema.model_json_schema()
        if description is not None:
            data["description"] = description
        response = self.client.patch(
            f"/memory-functions/{_as_uuid(memory_function_id)}", json=data
        )
        raise_for_status_with_text(response)
        return response.json()

    def delete_memory_function(
        self,
        memory_function_id: ID_T,
    ) -> None:
        """Delete a memory function.

        Args:
            memory_function_id (ID_T): The memory function's ID.
        """
        response = self.client.delete(
            f"/memory-functions/{_as_uuid(memory_function_id)}"
        )
        raise_for_status_with_text(response)
        return response.json()

    def create_thread(
        self,
        *,
        thread_id: Optional[ID_T] = None,
        messages: Optional[Sequence[Dict[str, Any]]] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Create a thread.

        Args:
            thread_id (ID_T): The thread's ID.
            messages (Sequence[Dict[str, Any]]): The messages to add.
            metadata (Dict[str, str], optional): The thread's metadata. Defaults to {}.

        Returns:
            Dict[str, Any]: The thread's data.
        """
        data = {
            "id": thread_id,
            "messages": messages,
            "metadata": metadata,
        }
        response = self.client.post("/threads", json=data)
        raise_for_status_with_text(response)
        return response.json()

    def add_messages(
        self, thread_id: ID_T, *, messages: Sequence[Dict[str, Any]]
    ) -> None:
        """Add messages to a thread.

        Args:
            thread_id (ID_T): The thread's ID.
            messages (Sequence[Dict[str, Any]]): The messages to add.
        """
        data = {"messages": messages}
        response = self.client.post(
            f"/threads/{_as_uuid(thread_id)}/add_messages", json=data
        )
        raise_for_status_with_text(response)
        return response.json()

    def get_thread(self, thread_id: ID_T) -> Dict[str, Any]:
        """Get a thread.

        Args:
            thread_id (ID_T): The thread's ID.

        Returns:
            Dict[str, Any]: The thread's data.
        """
        response = self.client.get(f"/threads/{_as_uuid(thread_id)}")
        raise_for_status_with_text(response)
        return response.json()

    def list_threads(self) -> Iterable[Dict[str, Any]]:
        """List threads.

        Returns:
            Iterable[Dict[str, Any]]: The threads' data.
        """
        response = self.client.get("/threads")
        raise_for_status_with_text(response)
        return response.json()

    def list_thread_memory(self, thread_id: ID_T) -> List[Dict[str, Any]]:
        """List a thread's memory.

        Args:
            thread_id (ID_T): The thread's ID.

        Returns:
            List[Dict[str, Any]]: The thread's memory.
        """
        response = self.client.get(f"/threads/{_as_uuid(thread_id)}/memory")
        raise_for_status_with_text(response)
        return response.json()

    def trigger_all_for_thread(self, thread_id: ID_T) -> None:
        """Trigger all memory functions for a thread.

        Args:
            thread_id (ID_T): The thread's ID.
        """
        response = self.client.post(f"/threads/{_as_uuid(thread_id)}/trigger-all")
        raise_for_status_with_text(response)
        return response.json()

    def add_thread_state(
        self, thread_id: ID_T, state: Dict[str, Any], *, key: Optional[str] = None
    ) -> None:
        """Add a thread state.

        Args:
            thread_id (ID_T): The thread's ID.
            state (Dict[str, Any]): The thread state.
        """
        response = self.client.post(
            f"/threads/{_as_uuid(thread_id)}/thread_state",
            json={"state": state, "key": key},
        )
        raise_for_status_with_text(response)
        return response.json()

    def get_thread_state(self, thread_id: ID_T, *, key: Optional[str] = None) -> dict:
        """Get a thread state.

        Args:
            thread_id (ID_T): The thread's ID.

        Returns:
            GetThreadStateResponse: The thread state.
        """
        response = self.client.post(
            f"/threads/{_as_uuid(thread_id)}/thread_state/query", json={"key": key}
        )
        raise_for_status_with_text(response)
        return response.json()

    def list_messages(
        self,
        thread_id: ID_T,
        *,
        page_size: Optional[int] = None,
        ascending_order: Optional[bool] = None,
    ) -> Iterable[Dict[str, Any]]:
        """List a thread's messages.

        Args:
            thread_id (ID_T): The thread's ID.
            page_size (Optional[int], optional): The page size. Defaults to None.

        Returns:
            Iterable[Dict[str, Any]]: The messages' data.
        """
        params: dict = {}
        if page_size is not None:
            params["page_size"] = page_size
        if ascending_order is not None:
            params["ascending_order"] = ascending_order
        cursor: Optional[str] = None
        while True:
            if cursor is not None:
                params["cursor"] = cursor
            response = self.client.get(
                f"/threads/{_as_uuid(thread_id)}/messages", params=params
            )
            raise_for_status_with_text(response)
            data = response.json()
            for message in data.get("messages", []):
                yield message
            cursor = data.get("next_cursor")
            if cursor is None:
                break
