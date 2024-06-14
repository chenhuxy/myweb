#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import requests
import zipfile
import shutil
import logging
import datetime
from glob import glob
import contextlib
# 使用Python 2.6运行Python 2.7代码
# AttributeError: ZipFile instance has no attribute '__exit__'
from typing import List, Optional


class ProjectDownloader:
    def __init__(self, host: str, headers: dict, download_dir: str, unzip_dir: str, deploy_dir: str, pkg_name: str,
                 project_id: str, project_tag: str, job_name: str):
        self.host = host
        self.headers = headers
        self.download_dir = download_dir
        self.unzip_dir = unzip_dir
        self.deploy_dir = deploy_dir
        self.pkg_name = pkg_name
        self.project_id = project_id
        self.project_tag = project_tag
        self.job_name = job_name

    def get_project_name(self) -> str:
        gitlab_url = "{}/api/v4/projects/{}".format(self.host, self.project_id)
        response = requests.get(gitlab_url, headers=self.headers)
        response.raise_for_status()
        project_name = response.json()['path']
        return project_name

    def get_sub_dirs(self, dirs: str, list_name: List[str]) -> Optional[List[str]]:
        if not os.path.exists(dirs):
            return None
        if os.path.isfile(dirs):
            return None
        for i in os.listdir(dirs):
            t = os.path.join(dirs, i)
            if os.path.isdir(t):
                self.get_sub_dirs(t, list_name)
            else:
                list_name.append(t)
        return list_name

    def chunk_read(self, response: requests.Response, chunk_size: int = 65536) -> int:
        total_size = int(response.headers.get('Content-Length').strip())
        bytes_so_far = 0
        project_name = self.get_project_name()
        project_name_zip = "{}.zip".format(project_name)
        download_path = os.path.join(self.download_dir, project_name_zip)

        print("\033[42m {} 开始下载，下载目录：{} \033[0m".format(project_name_zip, self.download_dir))
        # logging.info("{} 开始下载，下载目录：{}".format(project_name_zip, self.download_dir))

        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

        with open(download_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                bytes_so_far += len(chunk)
                percent = round((bytes_so_far / total_size) * 100, 2)
                if percent % 1 == 0:
                    # msg = "已下载 {} 字节，总共 {} 字节 (下载进度为：{:.2f}%)".format(bytes_so_far, total_size, percent)
                    msg = "已下载 {} 字节，总共 {} 字节 (下载进度为：{:.2f}%)\n".format(bytes_so_far, total_size, percent)
                    sys.stdout.write(msg)
                    # logging.info(msg)
                if bytes_so_far >= total_size:
                    sys.stdout.write('下载完成\n')
                    # logging.info('下载完成')
        return bytes_so_far

    def download_project_artifact(self) -> Optional[str]:
        try:
            gitlab_url = "{}/api/v4/projects/{}/jobs/artifacts/{}/download?job={}".format(
                self.host, self.project_id, self.project_tag, self.job_name)
            response = requests.get(gitlab_url, headers=self.headers, stream=True)
            response.raise_for_status()
            self.chunk_read(response)
            project_name = self.get_project_name()
            project_name_zip = "{}.zip".format(project_name)
            print("\033[42m {} 下载完成，下载目录：{} \033[0m".format(project_name_zip, self.download_dir))
            # logging.info("{} 下载完成，下载目录：{}".format(project_name_zip, self.download_dir))
            return project_name_zip
        except Exception as e:
            print("下载失败: {}".format(e))
            # logging.error("下载失败: {}".format(e))
            return None

    def unzip_project_artifact(self, file_name: str) -> None:
        if not os.path.exists(self.unzip_dir):
            os.makedirs(self.unzip_dir)
        # with zipfile.ZipFile(os.path.join(download_dir,file_name), 'r') as zip_ref:
        with contextlib.closing(zipfile.ZipFile(os.path.join(self.download_dir, file_name), 'r')) as zip_ref:
            zip_ref.extractall(self.unzip_dir)
            print("\033[42m 解压 {} 至目录：{} \033[0m".format(file_name, self.unzip_dir))
            # logging.info("解压 {} 至目录：{}".format(file_name, self.unzip_dir))

    def bak(self, src_file: str) -> None:
        if not os.path.isfile(src_file):
            msg = "{} 不存在！跳过备份步骤。".format(src_file)
            # print("\033[43m{}\033[0m".format(msg))
            logging.warning(msg)
        elif not os.path.isfile("{}-bak-{}".format(src_file, datetime.date.today().strftime('%Y-%m-%d'))):
            os.rename(src_file, "{}-bak-{}".format(src_file, datetime.date.today().strftime('%Y-%m-%d')))
            msg = "重命名 {} -> {}-bak-{}".format(src_file, src_file, datetime.date.today().strftime('%Y-%m-%d'))
            print("\033[42m{}\033[0m".format(msg))
            # logging.info(msg)
        else:
            msg = "备份文件 {}-bak-{} 已存在，无需再备份！".format(src_file, datetime.date.today().strftime('%Y-%m-%d'))
            print("\033[43m{}\033[0m".format(msg))
            # logging.warning(msg)

        for i in glob(os.path.join(self.deploy_dir, self.pkg_name, "files", "*")):
            if i not in (src_file, "{}-bak-{}".format(src_file, datetime.date.today().strftime('%Y-%m-%d'))):
                os.remove(i)
                msg = "删除备份文件 {}".format(i)
                print("\033[42m{}\033[0m".format(msg))
                # logging.info(msg)

    def publish(self, src_file: str) -> None:
        if not os.path.isfile(src_file):
            msg = "{} 不存在!!!".format(src_file)
            print("\033[41m{}\033[0m".format(msg))
            # logging.error(msg)
        else:
            deploy_dir = os.path.join(self.deploy_dir, self.pkg_name, "files")
            if not os.path.exists(deploy_dir):
                os.makedirs(deploy_dir)
            shutil.move(src_file, os.path.join(deploy_dir, os.path.basename(src_file)))
            msg = "移动 {} -> {}".format(src_file, os.path.join(self.deploy_dir, self.pkg_name, "files",
                                                                os.path.basename(src_file)))
            print("\033[42m{}\033[0m".format(msg))
            # logging.info(msg)

    def clean(self, dirs: str) -> None:
        if not os.path.exists(dirs):
            return
        if os.path.isfile(dirs):
            os.remove(dirs)
            return
        for i in os.listdir(dirs):
            t = os.path.join(dirs, i)
            if os.path.isdir(t):
                self.clean(t)
            else:
                os.unlink(t)
        if os.path.exists(dirs):
            os.removedirs(dirs)
        msg = "删除成功!!! {}".format(dirs)
        print("\033[42m{}\033[0m".format(msg))
        # logging.info(msg)
