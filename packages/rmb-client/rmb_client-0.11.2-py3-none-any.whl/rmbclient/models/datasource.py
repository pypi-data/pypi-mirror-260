import os

from rmbcommon.models import DataSourceCore, MetaData
from rmbclient.models.chat import ChatList
from rmbclient.models.base import convert_to_object, BaseResourceList
from rmbcommon.exceptions.client import DataSourceNotFound, UnsupportedFileType
from rmbclient.upload import upload_to_oss


class MetaDataClientModel(MetaData):

    def sync(self):
        new_meta_dict = self.api.send(endpoint=f"/datasources/{self.datasource_id}/meta", method="POST")
        self.update_from_dict(new_meta_dict)
        return self


class DataSourceClientModel(DataSourceCore):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.temp_chat = None  # 初始化时没有chat实例

    @property
    @convert_to_object(cls=MetaDataClientModel)
    def meta(self):
        return self.api.send(endpoint=f"/datasources/{self.id}/meta", method="GET")

    @property
    @convert_to_object(cls=MetaDataClientModel)
    def meta_runtime(self):
        return self.api.send(
            endpoint=f"/datasources/{self.id}/meta",
            method="GET",
            params={"from_where": "runtime"}
        )

    def delete(self):
        return self.api.send(endpoint=f"/datasources/{self.id}", method="DELETE")

    @property
    def download_url(self):
        resp = self.api.send(endpoint=f"/datasources/{self.id}/download_url", method="GET")
        return resp.get('url')

    def ask(self, question):
        """
        使用临时chat实例提问。如果不存在，将创建一个新的chat实例并缓存起来。

        参数:
            question (str): 要提问的问题。

        返回:
            答案或相关响应。
        """
        if not self.temp_chat:
            self.temp_chat = self._create_or_get_temp_chat()

        # 使用缓存的chat实例提问
        answer = self.temp_chat.ask(question)
        return answer

    def _create_or_get_temp_chat(self):
        """
        创建一个临时的chat实例，并将其与当前数据源绑定。

        返回:
            ChatClientModel: 创建的临时chat实例。
        """
        # 假设有一个创建chat的方法在 ChatList 类中，这里直接使用 ChatList 来创建
        # 注意：这里需要提供正确的APIRequest实例给 ChatList
        chat_list = ChatList(self.api, "/chats")
        temp_chat = chat_list.create(datasource_ids=[self.id])

        return temp_chat


class DataResourceList(BaseResourceList):
    __do_not_print_properties__ = ['tenant_id', 'access_config', 'sample_questions']

    @convert_to_object(cls=DataSourceClientModel)
    def _get_all_resources(self):
        return self._get_all_resources_request()

    def _get_all_resources_request(self):
        # 获取资源
        params = {
            "order": self.order,
            "page_number": self.page_number,
            "page_size": self.page_size
        }
        datasources = self.api.send(endpoint=self.endpoint, method="GET", params=params)
        return datasources

    @property
    @convert_to_object(cls=DataSourceClientModel)
    def latest(self):
        # 获取最后一个资源
        return self._get_all_resources_request()[0]

    def page(self, page_number=1):
        return DataResourceList(self.api, self.endpoint, page_number=page_number)

    def all(self):
        return DataResourceList(self.api, self.endpoint, page_number=0, page_size=0)

    @convert_to_object(cls=DataSourceClientModel)
    def get(self, id=None, name=None):
        if name:
            ds_list = self.api.send(endpoint=f"{self.endpoint}?name={name}", method="GET")
            if ds_list:
                return ds_list
            else:
                raise DataSourceNotFound(f"Data Source {name} not found")

        if not id:
            raise ValueError("No ID or Name provided")
        # 通过资源ID来获取
        return self.api.send(endpoint=f"{self.endpoint}/{id}", method="GET")

    @convert_to_object(cls=DataSourceClientModel)
    def register(self, ds_type, ds_access_config, ds_name=None):
        data = {
            "type": ds_type, "name": ds_name,
            "access_config": ds_access_config
        }
        return self.api.send(endpoint=self.endpoint, method="POST", data=data)

    def upload_file_to_oss(self, local_file_path):
        oss_info = self.create_upload_params()['oss']
        file_name = os.path.basename(local_file_path)
        oss_file_uri = f"{oss_info['oss_uri_prefix']}{file_name}"
        download_url = upload_to_oss(oss_info, local_file_path, oss_file_uri)
        return download_url

    def create_upload_params(self, expiration=None, file_max_size=None):
        params = {'expiration': expiration, 'file_max_size': file_max_size}
        return self.api.send(endpoint=f"{self.endpoint}/upload_params", method="POST", params=params)

    def upload_file_to_server(self, local_file_path) -> str:
        # 上传文件到服务器
        resp = self.api.send(
            endpoint=f"{self.endpoint}/upload_file",
            method="POST",
            files={'file': open(local_file_path, 'rb')}
        )
        return resp.get('url')

    def create_from_local_file(self, local_file_path, direct_to_oss=True):
        file_ext = os.path.splitext(local_file_path)[-1]
        if file_ext not in ['.csv', '.xls', '.xlsx']:
            raise UnsupportedFileType(f"File type {file_ext} not supported")

        if direct_to_oss:
            download_url = self.upload_file_to_oss(local_file_path)
        else:
            download_url = self.upload_file_to_server(local_file_path)

        if file_ext == '.csv':
            return self.register(ds_type="CSV", ds_access_config={
                "location_type": "http",
                "location_url": download_url,
            })
        elif file_ext in ['.xls', '.xlsx']:
            return self.register(ds_type="Excel", ds_access_config={
                "location_type": "http",
                "location_url": download_url,
            })
        else:
            raise UnsupportedFileType(f"File type {file_ext} not supported")

    def get_download_url(self, upload_url):
        resp = self.api.send(
            endpoint=f"{self.endpoint}/download_file_url",
            method="GET",
            params={
                'upload_url': upload_url
            }
        )
        return resp.get('url')
