import os
import hashlib
import base64
from re import I
from typing import Tuple, Union, List
import requests
import a0_baas_sdk.remote.auth as auth
from . import utils
from .config import get_baas_server_host, get_baas_file_resource_id
from urllib3.util import Retry
from requests import Session
from requests.adapters import HTTPAdapter


class File(object):
  id: str
  name: str
  size: int
  # checksum_md5: str
  url: str
  def __init__(self, id, name, size, url) -> None:
    self.id=id
    self.name=name
    self.size=size
    self.url=url

class FileDesc(object):
  id: str
  name: str
  size: int
  # checksum_md5: str
  url: str
  created_at: int
  updated_at: int
  def __init__(self, id, name, size, url, created_at, updated_at) -> None:
    self.id=id
    self.name=name
    self.size=size
    self.url=url
    self.created_at=created_at
    self.updated_at=updated_at

class PresignResult(object):
  url:str
  file:File
  additional_header:dict
  def __init__(self, url, file, additional_header) -> None:
    self.url=url
    self.file=file
    self.additional_header=additional_header

class Paginate(object):
  page_number:int
  page_size:int
  total_count:int
  def __init__(self, page_number, page_size, total_count) -> None:
    self.page_number=page_number
    self.page_size=page_size
    self.total_count=total_count

class ListFileResult(object):
  data: List[FileDesc]
  paginate: Paginate
  def __init__(self, data, paginate) -> None:
    self.data=data
    self.paginate=paginate

def _get_upload_presign_url(resource_id:str):
  return f"{get_baas_server_host()}/v1/baas/data/file/api/resource/{resource_id}/put/presign"

def _get_delete_url(resource_id:str,file_id:str):
  return f"{get_baas_server_host()}/v1/baas/data/file/api/resource/{resource_id}/file/{file_id}"

def _get_get_url(resource_id:str,file_id:str):
  return f"{get_baas_server_host()}/v1/baas/data/file/api/resource/{resource_id}/file/{file_id}"

def _get_list_url(resource_id:str):
  return f"{get_baas_server_host()}/v1/baas/data/file/api/resource/{resource_id}/list"


def presign_upload_file(data:bytes, name:str,resource_id:str, timeout:Union[float, Tuple[float]])->PresignResult:
  checksum = hashlib.md5(data).digest()
  checksum_base64 = base64.b64encode(checksum).decode('utf-8')
  url = _get_upload_presign_url(resource_id)
  resp = _get_baas_session().get(url, data={
    "Name": name,
    "Size": len(data),
    "CheckSumMD5":checksum_base64
  },headers=auth.get_auth_header(resource_id), timeout=_get_timeout(timeout))
  presign_resp = utils._parse_response(resp)
  file_desc = presign_resp["File"]
  file = File(file_desc["ID"], file_desc["Name"], file_desc["Size"], file_desc["URL"])
  return PresignResult(presign_resp["URL"], file, presign_resp["AdditionalHeader"])

def delete(file_id:str,resource_id:str, timeout:Union[float, Tuple[float, float]]=10)->None:
  """
  delete file by file_id
  """
  url = _get_delete_url(resource_id,file_id)
  resp = _get_baas_session().delete(url, headers=auth.get_auth_header(resource_id), timeout=_get_timeout(timeout))
  return utils._parse_response(resp)

def get_file_info(file_id:str,resource_id:str, timeout:Union[float, Tuple[float]])->File:
  """
  get file info by file_id
  """
  url = _get_get_url(resource_id, file_id)
  resp = _get_baas_session().get(url, headers=auth.get_auth_header(resource_id), timeout=_get_timeout(timeout))
  file_resp = utils._parse_response(resp)
  if file_resp is None:
    return None
  return File(file_resp["ID"], file_resp["Name"], file_resp["Size"], file_resp["URL"])

def list_file(resource_id:str ,page_number: Union[int, None], page_size: Union[int, None], prefix: Union[str, None], timeout:Union[Union[float, Tuple[float]], None])->Union[ListFileResult, None]:
  """
  list file info by page_number and page_size
  """
  url = _get_list_url(resource_id)
  requst_body = {
    "PaginateFilter": {
      "PageSize": page_size or 10,
      "PageNumber": page_number or 1,
    },
    "PrefixFilter": prefix or "",
  }
  resp = _get_baas_session().post(url, json = requst_body, headers=auth.get_auth_header(resource_id), timeout=_get_timeout(timeout))
  list_file_resp = utils._parse_response(resp)

  if list_file_resp["Data"] is None:
    list_file_resp["Data"] = []
  if list_file_resp is None or list_file_resp["Paginate"] is None:
    return None
  result_paginate = Paginate(list_file_resp["Paginate"]["PageNumber"], list_file_resp["Paginate"]["PageSize"], list_file_resp["Paginate"]["TotalCount"])
  result_data = []
  for file_desc in list_file_resp["Data"]:
    result_data.append(FileDesc(file_desc["ID"], file_desc["Name"], file_desc["Size"], file_desc["URL"], file_desc["CreatedAt"], file_desc["UpdatedAt"]))
  return ListFileResult(result_data, result_paginate)
  

def get_s3_session()->Session:
  s = Session()
  return s
  # retries = Retry(
  #     total=3,
  #     backoff_factor=0.1,
  #     status_forcelist=[502, 503, 504],
  #     allowed_methods={'POST'},
  # )
  # s.mount('http://', HTTPAdapter(max_retries=retries))
  # s.mount('https://', HTTPAdapter(max_retries=retries))

def _get_baas_session()->Session:
  s = Session()
  return s

def _get_timeout(timeout):
  if isinstance(timeout, tuple):
    return timeout
  else:
    return (2, timeout)

def get_s3_timeout(timeout):
  if isinstance(timeout, tuple):
    return timeout
  else:
    return (2, timeout)
  