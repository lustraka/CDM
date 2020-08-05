﻿# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.

from datetime import datetime, timezone
import os
from typing import List, Optional

from .base import StorageAdapterBase


FILE_PATH = os.path.dirname(os.path.abspath(__file__))
RESOURCES_PATH = os.path.join(FILE_PATH, '..', 'resources')


class ResourceAdapter(StorageAdapterBase):
    """Resource storage adapter"""
    _ROOT = 'Microsoft.CommonDataModel.ObjectModel.Resources'

    def __init__(self) -> None:
        """The constructor can have a specified root for resources (used by internal code mostly, but can be used for external),
         by default it finds resources for a wheel generated by setuptools."""
        self.location_hint = None  # type: Optional[str]

        # --- internal ---
        self._resources_path = os.path.abspath(RESOURCES_PATH)  # type: str
        self._type = 'resource'

    def can_read(self) -> bool:
        return True

    def can_write(self) -> bool:
        return False

    async def read_async(self, corpus_path: str) -> str:
        adapter_path = self._resources_path + corpus_path

        if not os.path.exists(adapter_path):
            raise Exception('There is no resource found for {}'.format(corpus_path))

        with open(adapter_path, 'r', encoding='utf-8') as file:
            return file.read()

    async def write_async(self, corpus_path: str, data: str) -> None:
        raise NotImplementedError()

    def create_adapter_path(self, corpus_path: str) -> str:
        if not corpus_path:
            return None

        return self._ROOT + corpus_path

    def create_corpus_path(self, adapter_path: str) -> Optional[str]:
        if not adapter_path or not adapter_path.startswith(self._ROOT):
            return None
        return adapter_path[len(self._ROOT):]

    def clear_cache(self) -> None:
        pass

    async def compute_last_modified_time_async(self, corpus_path: str) -> Optional[datetime]:
        return datetime.now(timezone.utc)

    async def fetch_all_files_async(self, folder_corpus_path: str) -> List[str]:
        return None

    def fetch_config(self) -> str:
        raise NotImplementedError()

    def update_config(self, config: str) -> None:
        raise NotImplementedError()
