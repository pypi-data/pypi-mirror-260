import time

import pandas as pd

from .adapters import RhoApiGraphqlAdapter, UploadFileHttpAdapter
from .config import init_config
from .types import StoreDfResult


class RhoClient:
    def __init__(self, api_key: str):
        self._config = init_config()
        self._api_port = RhoApiGraphqlAdapter(
            base_url=self._config.API_URL,
            api_key=api_key
        )
        self._file_upload_port = UploadFileHttpAdapter()

    def get_table_url(self, table_id: str, workspace_id: str) -> str:
        return f"{self._config.CLIENT_URL}/app/tables/{table_id}?wid={workspace_id}"

    def store_df(self, data: pd.DataFrame, name: str = None) -> StoreDfResult:
        t1 = time.time()
        url, file_id = self._api_port.get_signed_url()
        t2 = time.time()
        self._file_upload_port.upload_dataframe(url, data)
        t3 = time.time()
        if name is None:
            name = "New table"
        table = self._api_port.create_table(name)
        table_id = table["id"]
        workspace_id = table["workspaceId"]
        t4 = time.time()
        self._api_port.process_file(file_id, table_id)
        t5 = time.time()
        print("- Get url: ", t2 - t1)
        print("- Upload file: ", t3 - t2)
        print("- Create table: ", t4 - t3)
        print("- Process file: ", t5 - t4)
        print("Total time: ", t5 - t1)
        client_url = self.get_table_url(table_id, workspace_id)
        return StoreDfResult(
            table_id=table["id"],
            client_url=client_url
        )

    def store_data(self, data: list[dict]) -> StoreDfResult:
        df = pd.DataFrame(data)
        return self.store_df(df)

    def get_df(self, table_id: str) -> pd.DataFrame:
        data = self.get_data(table_id)
        parsed_data = pd.DataFrame(data)
        if "_id" in parsed_data.columns:
            parsed_data.drop(columns=["_id"], inplace=True)
        return parsed_data

    def get_data(self, table_id: str) -> list[dict]:
        t1 = time.time()
        data = self._api_port.get_data(table_id)
        t2 = time.time()
        print("Got data in: ", t2 - t1)
        return data


__all__ = ["RhoClient"]
