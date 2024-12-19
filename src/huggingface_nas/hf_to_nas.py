import os
import shutil
from typing import Optional

from datasets import load_dataset
from huggingface_hub import Repository
from synology_api.exceptions import FileStationError

from .webapi import WebAPI


def upload_dataset(
    name,
    base_folder,
    tmp_folder=".tmp_hf_to_nas",
    cache_tmp_folder=".cache_hf_to_nas",
    token=None,
    *,
    ip_address: Optional[str] = None,
    port: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    secure: bool = False,
    cert_verify: bool = False,
    dsm_version: int = 7,
    debug: bool = True,
    otp_code: Optional[str] = None,
    interactive_output: bool = True,
):
    local_dir = tmp_folder
    if not os.path.exists(local_dir):
        try:
            hf_data = load_dataset(name, token=token, cache_dir=cache_tmp_folder)
            hf_data.save_to_disk(local_dir)
        except Exception as e:
            shutil.rmtree(cache_tmp_folder)
            shutil.rmtree(local_dir)
            raise Exception(e)

    try:
        fi = WebAPI(
            ip_address=ip_address,
            port=port,
            username=username,
            password=password,
            secure=secure,
            cert_verify=cert_verify,
            dsm_version=dsm_version,
            debug=debug,
            otp_code=otp_code,
            interactive_output=interactive_output,
        )
        try:
            remote_folder = os.path.join(base_folder, name)
            res = fi.get_file_list(folder_path=remote_folder)
            if res["success"] and any(file["path"] for file in res["data"]["files"] if remote_folder in file["path"]):
                raise Exception("이미 존재하는 파일입니다")
        except FileStationError as e:
            if e.error_code != 408:
                raise FileStationError(error_code=e.error_code)
        for root, dirs, files in os.walk(local_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                dest_path = os.path.join(base_folder, name, os.path.relpath(file_path, local_dir))
                dest_path = os.path.split(dest_path)[0]
                fi.upload_file(
                    dest_path=dest_path,
                    file_path=file_path,
                    create_parents=True,
                    overwrite=False,     # default로 False로
                    verify=False,
                    progress_bar=True,
                )
    finally:
        if os.path.exists(local_dir):
            shutil.rmtree(local_dir)
        if os.path.exists(cache_tmp_folder):
            shutil.rmtree(cache_tmp_folder)


def upload_model(
    name,
    base_folder,
    cache_tmp_folder=".cache_hf_to_nas",
    token=None,
    *,
    ip_address: Optional[str] = None,
    port: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    secure: bool = False,
    cert_verify: bool = False,
    dsm_version: int = 7,
    debug: bool = True,
    otp_code: Optional[str] = None,
    interactive_output: bool = True,
):
    local_dir = os.path.join(cache_tmp_folder, name)
    if not os.path.exists(local_dir):
        try:
            Repository(local_dir=local_dir, clone_from=name)
        except Exception as e:
            shutil.rmtree(local_dir)
            raise Exception(e)

    try:
        fi = WebAPI(
            ip_address=ip_address,
            port=port,
            username=username,
            password=password,
            secure=secure,
            cert_verify=cert_verify,
            dsm_version=dsm_version,
            debug=debug,
            otp_code=otp_code,
            interactive_output=interactive_output,
        )
        try:
            remote_folder = os.path.join(base_folder, name)
            res = fi.get_file_list(folder_path=remote_folder)
            if res["success"] and any(file["path"] for file in res["data"]["files"] if remote_folder in file["path"]):
                raise Exception("이미 존재하는 파일입니다")
        except FileStationError as e:
            if e.error_code != 408:
                raise FileStationError(error_code=e.error_code)
        for root, dirs, files in os.walk(local_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                dest_path = os.path.join(base_folder, os.path.relpath(file_path, cache_tmp_folder))
                dest_path = os.path.split(dest_path)[0]
                fi.upload_file(
                    dest_path=dest_path,
                    file_path=file_path,
                    create_parents=True,
                    overwrite=False,     # default로 False로
                    verify=False,
                    progress_bar=True,
                )
    finally:
        if os.path.exists(cache_tmp_folder):
            shutil.rmtree(cache_tmp_folder)
