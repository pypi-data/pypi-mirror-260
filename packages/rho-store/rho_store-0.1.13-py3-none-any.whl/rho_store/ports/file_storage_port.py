import abc

import pandas as pd


class FileStoragePort(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def upload_dataframe(self, name: str, data: pd.DataFrame):
        raise NotImplementedError

    @abc.abstractmethod
    async def download_dataframe(self, name: str) -> pd.DataFrame:
        raise NotImplementedError


__all__ = ["FileStoragePort"]
