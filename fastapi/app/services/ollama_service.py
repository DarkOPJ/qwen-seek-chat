import json
from typing import AsyncGenerator, Dict, List, Any

import httpx
from loguru import logger as loguru_logger

from app.core.exceptions import AppException, AppExceptionCase
from config import settings


class OllamaService:
    """Async service for interacting with Ollama API."""

    def __init__(self):
        self.base_url = settings.ollama_host.rstrip("/")
        self.timeout = settings.ollama_timeout
        self.default_models = settings.ollama_default_models

    def _get_client(self) -> httpx.AsyncClient:
        """Create an async HTTP client with timeout configuration."""
        return httpx.AsyncClient(
            base_url=self.base_url,
            timeout=httpx.Timeout(self.timeout),
        )

    async def _handle_error(self, response: httpx.Response, operation: str) -> None:
        """Handle HTTP error responses from Ollama."""
        try:
            error_data = response.json()
            error_msg = error_data.get("error", response.text)
        except Exception:
            error_msg = response.text

        if response.status_code == 404:
            raise AppException.NotFoundException(
                error_message=f"Ollama {operation} failed: {error_msg}"
            )
        elif response.status_code >= 500:
            raise AppException.InternalServerException(
                error_message=f"Ollama server error during {operation}: {error_msg}"
            )
        else:
            raise AppException.BadRequestException(
                error_message=f"Ollama {operation} failed: {error_msg}"
            )

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str,
        stream: bool = False,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Generate a chat completion using Ollama.

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name to use (e.g., 'qwen3:1.7b')
            stream: Whether to stream the response
            **kwargs: Additional parameters (temperature, max_tokens, etc.)

        Returns:
            Dict with response data
        """
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream,
            **kwargs,
        }

        async with self._get_client() as client:
            try:
                response = await client.post("/api/chat", json=payload)
                if response.status_code >= 400:
                    await self._handle_error(response, "chat completion")

                return response.json()

            except httpx.TimeoutException as exc:
                loguru_logger.error(f"Ollama timeout during chat completion: {exc}")
                raise AppException.InternalServerException(
                    error_message=f"Ollama request timeout after {self.timeout}s"
                )
            except httpx.ConnectError as exc:
                loguru_logger.error(f"Ollama connection error: {exc}")
                raise AppException.InternalServerException(
                    error_message=f"Cannot connect to Ollama at {self.base_url}"
                )
            except AppExceptionCase:
                raise
            except Exception as exc:
                loguru_logger.error(f"Unexpected error during chat completion: {exc}")
                raise AppException.InternalServerException(
                    error_message=f"Unexpected error: {str(exc)}"
                )

    async def chat_completion_stream(
        self,
        messages: List[Dict[str, str]],
        model: str,
        **kwargs: Any,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Generate a streaming chat completion using Ollama.

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name to use
            **kwargs: Additional parameters (temperature, max_tokens, etc.)

        Yields:
            Dict with streaming response chunks
        """
        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
            **kwargs,
        }

        async with self._get_client() as client:
            try:
                async with client.stream("POST", "/api/chat", json=payload) as response:
                    if response.status_code >= 400:
                        await self._handle_error(response, "chat completion stream")

                    async for line in response.aiter_lines():
                        if not line.strip():
                            continue
                        try:
                            chunk = json.loads(line)
                            yield chunk
                        except json.JSONDecodeError as exc:
                            loguru_logger.warning(
                                f"Failed to parse Ollama stream chunk: {exc}"
                            )
                            continue

            except httpx.TimeoutException as exc:
                loguru_logger.error(f"Ollama timeout during streaming: {exc}")
                raise AppException.InternalServerException(
                    error_message=f"Ollama stream timeout after {self.timeout}s"
                )
            except httpx.ConnectError as exc:
                loguru_logger.error(f"Ollama connection error during streaming: {exc}")
                raise AppException.InternalServerException(
                    error_message=f"Cannot connect to Ollama at {self.base_url}"
                )
            except AppExceptionCase:
                raise
            except Exception as exc:
                loguru_logger.error(f"Unexpected error during streaming: {exc}")
                raise AppException.InternalServerException(
                    error_message=f"Unexpected error: {str(exc)}"
                )

    async def list_models(self) -> List[Dict[str, Any]]:
        """
        List available models in Ollama.

        Returns:
            List of model info dicts
        """
        async with self._get_client() as client:
            try:
                response = await client.get("/api/tags")
                if response.status_code >= 400:
                    await self._handle_error(response, "list models")

                data = response.json()
                return data.get("models", [])

            except httpx.TimeoutException as exc:
                loguru_logger.error(f"Ollama timeout during list models: {exc}")
                raise AppException.InternalServerException(
                    error_message=f"Ollama request timeout after {self.timeout}s"
                )
            except httpx.ConnectError as exc:
                loguru_logger.error(f"Ollama connection error: {exc}")
                raise AppException.InternalServerException(
                    error_message=f"Cannot connect to Ollama at {self.base_url}"
                )
            except AppExceptionCase:
                raise
            except Exception as exc:
                loguru_logger.error(f"Unexpected error listing models: {exc}")
                raise AppException.InternalServerException(
                    error_message=f"Unexpected error: {str(exc)}"
                )

    async def pull_model(self, model_name: str) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Pull a model from Ollama registry.

        Args:
            model_name: Name of the model to pull (e.g., 'qwen3:1.7b')

        Yields:
            Dict with pull progress
        """
        payload = {"name": model_name, "stream": True}

        async with self._get_client() as client:
            try:
                async with client.stream("POST", "/api/pull", json=payload) as response:
                    if response.status_code >= 400:
                        await self._handle_error(response, "pull model")

                    async for line in response.aiter_lines():
                        if not line.strip():
                            continue
                        try:
                            chunk = json.loads(line)
                            yield chunk
                        except json.JSONDecodeError as exc:
                            loguru_logger.warning(
                                f"Failed to parse Ollama pull chunk: {exc}"
                            )
                            continue

            except httpx.TimeoutException as exc:
                loguru_logger.error(f"Ollama timeout during model pull: {exc}")
                raise AppException.InternalServerException(
                    error_message=f"Ollama pull timeout after {self.timeout}s"
                )
            except httpx.ConnectError as exc:
                loguru_logger.error(f"Ollama connection error during pull: {exc}")
                raise AppException.InternalServerException(
                    error_message=f"Cannot connect to Ollama at {self.base_url}"
                )
            except AppExceptionCase:
                raise
            except Exception as exc:
                loguru_logger.error(f"Unexpected error pulling model: {exc}")
                raise AppException.InternalServerException(
                    error_message=f"Unexpected error: {str(exc)}"
                )

    async def check_model_exists(self, model_name: str) -> bool:
        """
        Check if a model exists in Ollama.

        Args:
            model_name: Name of the model to check

        Returns:
            True if model exists, False otherwise
        """
        try:
            models = await self.list_models()
            return any(model.get("name") == model_name for model in models)
        except AppExceptionCase:
            return False
        except Exception as exc:
            loguru_logger.error(f"Error checking model existence: {exc}")
            return False

    async def delete_model(self, model_name: str) -> bool:
        """
        Delete a model from Ollama.

        Args:
            model_name: Name of the model to delete

        Returns:
            True if successful
        """
        payload = {"name": model_name}

        async with self._get_client() as client:
            try:
                response = await client.request("DELETE", "/api/delete", json=payload)
                if response.status_code >= 400:
                    await self._handle_error(response, "delete model")
                return True

            except httpx.TimeoutException as exc:
                loguru_logger.error(f"Ollama timeout during model delete: {exc}")
                raise AppException.InternalServerException(
                    error_message=f"Ollama request timeout after {self.timeout}s"
                )
            except httpx.ConnectError as exc:
                loguru_logger.error(f"Ollama connection error during delete: {exc}")
                raise AppException.InternalServerException(
                    error_message=f"Cannot connect to Ollama at {self.base_url}"
                )
            except AppExceptionCase:
                raise
            except Exception as exc:
                loguru_logger.error(f"Unexpected error deleting model: {exc}")
                raise AppException.InternalServerException(
                    error_message=f"Unexpected error: {str(exc)}"
                )

    async def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """
        Get detailed information about a model.

        Args:
            model_name: Name of the model

        Returns:
            Model info dict
        """
        payload = {"name": model_name}

        async with self._get_client() as client:
            try:
                response = await client.post("/api/show", json=payload)
                if response.status_code >= 400:
                    await self._handle_error(response, "get model info")
                return response.json()

            except httpx.TimeoutException as exc:
                loguru_logger.error(f"Ollama timeout during get model info: {exc}")
                raise AppException.InternalServerException(
                    error_message=f"Ollama request timeout after {self.timeout}s"
                )
            except httpx.ConnectError as exc:
                loguru_logger.error(f"Ollama connection error: {exc}")
                raise AppException.InternalServerException(
                    error_message=f"Cannot connect to Ollama at {self.base_url}"
                )
            except AppExceptionCase:
                raise
            except Exception as exc:
                loguru_logger.error(f"Unexpected error getting model info: {exc}")
                raise AppException.InternalServerException(
                    error_message=f"Unexpected error: {str(exc)}"
                )

    async def health_check(self) -> bool:
        """
        Check if Ollama is reachable.

        Returns:
            True if Ollama is reachable, False otherwise
        """
        async with self._get_client() as client:
            try:
                response = await client.get("/api/tags")
                return response.status_code == 200
            except Exception:
                return False
