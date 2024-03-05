import hashlib
import http
import json
import os.path
import uuid
import sys
import time
from queue import Empty, Queue
from threading import Thread

import requests
from minio import Minio
from minio.error import S3Error

_BAR_SIZE = 20
_KILOBYTE = 1024
_FINISHED_BAR = '#'
_REMAINING_BAR = '-'

_UNKNOWN_SIZE = '?'
_STR_MEGABYTE = ' MB'

_HOURS_OF_ELAPSED = '%d:%02d:%02d'
_MINUTES_OF_ELAPSED = '%02d:%02d'

_RATE_FORMAT = '%5.2f'
_PERCENTAGE_FORMAT = '%3d%%'
_HUMANINZED_FORMAT = '%0.2f'

_DISPLAY_FORMAT = '|%s| %s/%s %s [elapsed: %s left: %s, %s MB/sec]'

_REFRESH_CHAR = '\r'


class PandoraBox:
    def __init__(self, username, password, admin_host):
        self.is_login = False
        try:
            self.admin_host = admin_host

            if not username or not password:
                raise ValueError("登录失败，用户名或密码为空")

            info = json.dumps({
                'username': username,
                'password': password
            })
            resp = self._login_req(info)

            if resp.status_code == http.HTTPStatus.BAD_REQUEST:
                if not resp.text:
                    return
                raise ValueError(f"登录失败，错误消息: {resp.json().get('msg')}")

            if resp.status_code == http.HTTPStatus.OK:
                if not resp.text:
                    return
                code = resp.json().get("code")
                if code != 0:
                    raise ValueError(f"登录失败，错误消息: {resp.json().get('msg')}")

                self.key = resp.json()['gateway_info']['access_key']
                self.secret = resp.json()['gateway_info']['access_secret']
                self.bucket = resp.json()['gateway_info']['bucket']
                self.gateway = resp.json()['gateway_info']['gateway']

                self.client = Minio(
                    self.gateway,
                    access_key=self.key,
                    secret_key=self.secret,
                    secure=False,
                )
                self.user = username
                self.is_login = True
                print("登录成功")

        except Exception as e:
            print(f"登录过程中发生错误: {str(e)}")

    def model_init(self, model_name, description, library, data_set, task):
        try:
            if not self.is_login:
                raise ValueError("用户未登录")
            if not model_name:
                raise ValueError("参数 model_name 为空")

            info = json.dumps({
                'model_name': model_name,
                'description': description,
                'library': library,
                'data_set': data_set,
                'task': task,
                'creator': self.user,
            })

            resp = self._new_model_req(info)
            resp.raise_for_status()  # 引发HTTP错误

            print(resp.text)

        except ValueError as ve:
            print(f"Error: {str(ve)}")

        except requests.RequestException as re:
            print(f"HTTP请求错误: {str(re)}")

        except Exception as e:
            print(f"发生未知错误: {str(e)}")

    def my_models(self):
        try:
            if not self.is_login:
                raise ValueError("用户未登录")

            resp = self._get_user_model_list_req()
            resp.raise_for_status()

            if resp.status_code == http.HTTPStatus.OK:
                data = resp.json().get("data")
                print(data)
                return data

        except ValueError as ve:
            print(f"Error: {str(ve)}")

        except requests.RequestException as re:
            print(f"HTTP请求错误: {str(re)}")

        except Exception as e:
            print(f"发生未知错误: {str(e)}")

    def get_model(self, model_name, tag, destination_path):
        try:
            if not self.is_login:
                raise ValueError("用户未登录")
            if not tag:
                raise ValueError("参数 tag 为空")
            if not model_name:
                raise ValueError("参数 model_name 为空")
            if os.path.isfile(destination_path):
                raise ValueError("参数 destination_path 必须是一个文件夹")
            if not os.path.exists(destination_path):
                raise ValueError("目标路径不存在")

            resp = self._get_tag_storage_path_req(model_name, tag)
            resp.raise_for_status()

            blob_path = resp.json().get("blob_path")

            objects = self.client.list_objects(
                self.bucket, recursive=True, prefix=blob_path,
            )

            for obj in objects:
                parts = obj.object_name.split('/')
                full_path = '/'.join(parts[3:]) if len(parts) > 3 else ''

                err = self._download(obj.object_name, os.path.join(destination_path, full_path))

                if err:
                    raise ValueError(f"下载文件时发生错误: {err}")

            print("文件下载成功。")

        except ValueError as ve:
            print(f"错误: {str(ve)}")

        except requests.RequestException as re:
            print(f"HTTP请求错误: {str(re)}")

        except Exception as e:
            print(f"发生未知错误: {str(e)}")

    def version_list(self, model_name):
        try:
            if not self.is_login:
                raise ValueError("用户未登录")

            resp = self._get_model_version_list_req(model_name)
            resp.raise_for_status()

            if resp.status_code == http.HTTPStatus.OK:
                version_list = resp.json().get("version_list")
                print(version_list)
                return version_list

        except ValueError as ve:
            print(f"错误: {str(ve)}")

        except requests.RequestException as re:
            print(f"HTTP请求错误: {str(re)}")

        except Exception as e:
            print(f"发生未知错误: {str(e)}")

    def register_model(self, model_name, tag, local_path):
        try:
            if not self.is_login:
                raise ValueError("用户未登录")
            if not model_name:
                raise ValueError("参数 model_name 为空")
            if not local_path:
                raise ValueError("参数 local_path 为空")
            if not tag:
                raise ValueError("参数 tag 为空")

            blob_path = ""
            guid = str(uuid.uuid4())

            resp = self._get_model_id_req(model_name)
            resp.raise_for_status()

            # 获取文件名和哈希值列表
            file_hash = []

            if os.path.isfile(local_path):
                file_info = hash_files(local_path)
                file_hash.append(file_info)
                file_name = os.path.basename(local_path)
                destination_path = f"/models/{model_name}/{guid}/{file_name}"
                err = self._upload(local_path, destination_path)
                if err:
                    raise ValueError(f"上传文件时发生错误: {err}")

                blob_path = f"/models/{model_name}/{guid}/"
                print("文件上传成功。")

            elif os.path.isdir(local_path):
                local_path = os.path.abspath(local_path)
                allfiles = _allfiles(local_path)
                file_hash = hash_files_in_directory(local_path)
                for file in allfiles:
                    folder_name = os.path.basename(local_path)
                    file_path = file.split(folder_name + '/')[1]
                    destination_path = os.path.join('models', model_name, guid, file_path)
                    source_path = os.path.join(local_path, file)
                    err = self._upload(source_path, destination_path)
                    if err:
                        raise ValueError(f"上传文件时发生错误: {err}")

                blob_path = f"/models/{model_name}/{guid}/"
                print("文件上传成功。")

            else:
                raise ValueError("请输入正确的路径")

            info = json.dumps({
                'model_name': model_name,
                'tag': tag,
                'blob_path': blob_path,
                'guid': str(guid),
                'files_list': file_hash,
            })

            address = self._add_model_version_req(info)
            address.raise_for_status()

            if address.status_code == http.HTTPStatus.BAD_REQUEST:
                raise ValueError(address.json().get("msg"))

            print("模型注册成功。")

        except ValueError as ve:
            print(f"错误: {str(ve)}")

        except requests.RequestException as re:
            print(f"HTTP请求错误: {str(re)}")

        except Exception as e:
            print(f"发生未知错误: {str(e)}")

    def get_model_file_list(self, model_name, tag):
        try:
            if not self.is_login:
                raise ValueError("用户未登录")
            if not tag:
                raise ValueError("参数 tag 为空")
            if not model_name:
                raise ValueError("参数 model_name 为空")

            resp = self._get_model_tag_files_req(model_name, tag)
            resp.raise_for_status()

            if resp.status_code == http.HTTPStatus.OK:
                return resp.json().get("data")

        except ValueError as ve:
            print(f"错误: {str(ve)}")

        except requests.RequestException as re:
            print(f"HTTP请求错误: {str(re)}")

        except Exception as e:
            print(f"发生未知错误: {str(e)}")

    def _upload(self, local_path, destination):
        try:
            self.client.fput_object(
                self.bucket,
                destination,
                local_path,
                progress=Progress(),  # 在回调中调用线程对象的run方法
            )
            print("文件上传成功。")
            return None
        except S3Error as err:
            print(f"文件上传失败: {err}")
            return err

    def _download(self, source, destination):
        try:
            # Download data of an object.
            self.client.fget_object(
                self.bucket,
                source,
                destination,
                progress=Progress(),  # 在回调中调用线程对象的run方法
            )
            print("文件下载成功。")
            return None
        except S3Error as err:
            print(f"文件下载失败: {err}")
            return err

    # def _delete_model_version_req(self, model_name, model_version):
    #     base_url = "http://{host}/api/v1/model/version/{model_name}/{model_version}" \
    #         .format(host=ADMIN_HOST, model_name=model_name, model_version=model_version)
    #     resp = requests.delete(url=base_url)
    #     return resp
    #
    # def _delete_model_tag_req(self, model_name, model_tag):
    #     base_url = "http://{host}/api/v1/model/tag/{model_name}/{model_tag}" \
    #         .format(host=ADMIN_HOST, model_name=model_name, model_tag=model_tag)
    #     resp = requests.delete(url=base_url)
    #     return resp
    #
    # def _delete_model_req(self, model_name):
    #     base_url = "http://{host}/api/v1/model/{model_name}" \
    #         .format(host=ADMIN_HOST, model_name=model_name)
    #     resp = requests.delete(url=base_url)
    #     return resp

    def _get_model_id_req(self, model_name):
        headers = {'username': self.user}
        base_url = "{host}/api/v1/model/{model_name}/id" \
            .format(host=self.admin_host, model_name=model_name)
        resp = requests.get(url=base_url, headers=headers)
        return resp

    def _get_model_info_req(self, model_name):
        headers = {'username': self.user}
        base_url = "{host}/api/v1/model/{model_name}/info" \
            .format(host=self.admin_host, model_name=model_name)
        resp = requests.get(url=base_url, headers=headers)
        return resp

    def _get_tag_storage_path_req(self, model_name, model_tag):
        headers = {'username': self.user}
        base_url = "{host}/api/v1/model/tag/{model_name}/{model_tag}/storage" \
            .format(host=self.admin_host, model_name=model_name, model_tag=model_tag)
        resp = requests.get(url=base_url, headers=headers)
        return resp

    def _get_version_storage_path_req(self, model_name, model_version):
        headers = {'username': self.user}
        base_url = "{host}/api/v1/model/version/{model_name}/{model_version}/storage" \
            .format(host=self.admin_host, model_name=model_name, model_version=model_version)
        resp = requests.get(url=base_url, headers=headers)
        return resp

    def _get_model_version_list_req(self, model_name):
        headers = {'username': self.user}
        base_url = "{host}/api/v1/model/{model_name}/version/list" \
            .format(host=self.admin_host, model_name=model_name)
        resp = requests.get(url=base_url, headers=headers)
        return resp

    def _get_user_model_list_req(self):
        headers = {'username': self.user}
        base_url = "{host}/api/v1/{username}/model/list" \
            .format(host=self.admin_host, username=self.user)
        resp = requests.get(url=base_url, headers=headers)
        return resp

    def _add_model_version_req(self, json_info):
        headers = {'Content-Type': 'application/json', 'username': self.user}
        base_url = "{host}/api/v1/model/version/add".format(host=self.admin_host)
        resp = requests.post(url=base_url, data=json_info, headers=headers)
        return resp

    def _new_model_req(self, json_info):
        headers = {'Content-Type': 'application/json', 'username': self.user}
        base_url = "{host}/api/v1/model/init".format(host=self.admin_host)
        resp = requests.post(url=base_url, data=json_info, headers=headers)
        return resp

    def _login_req(self, json_info):
        headers = {'Content-Type': 'application/json'}
        base_url = "{host}/api/v1/login".format(host=self.admin_host)
        resp = requests.post(url=base_url, data=json_info, headers=headers)
        return resp

    def _get_model_tag_files_req(self, model_name, model_tag):
        headers = {'username': self.user}
        base_url = "{host}/api/v1/model/tag/{model_name}/{model_tag}/files" \
            .format(host=self.admin_host, model_name=model_name, model_tag=model_tag)
        resp = requests.get(url=base_url, headers=headers)
        return resp

    def get_login_status(self):
        return self.is_login


def _allfiles(folder):
    try:
        filepath_list = []
        for root, _, file_names in os.walk(folder):
            for file_name in file_names:
                file_path = os.path.join(root, file_name)
                filepath_list.append(file_path)
                print(file_path)
        # filepath_list = sorted(filepath_list, key=str.lower)
        return filepath_list

    except Exception as e:
        print(f"获取文件列表时发生错误: {str(e)}")
        return []


class Progress(Thread):
    """
        Constructs a :class:`Progress` object.
        :param interval: Sets the time interval to be displayed on the screen.
        :param stdout: Sets the standard output

        :return: :class:`Progress` object
    """

    def __init__(self, interval=1, stdout=sys.stdout):
        Thread.__init__(self)
        self.prefix = None
        self.daemon = True
        self.total_length = 0
        self.interval = interval
        self.object_name = None

        self.last_printed_len = 0
        self.current_size = 0

        self.display_queue = Queue()
        self.initial_time = time.time()
        self.stdout = stdout
        self.start()

    def set_meta(self, total_length, object_name):
        """
        Metadata settings for the object. This method called before uploading
        object
        :param total_length: Total length of object.
        :param object_name: Object name to be showed.
        """
        self.total_length = total_length
        self.object_name = object_name
        self.prefix = self.object_name + ': ' if self.object_name else ''

    def run(self):
        displayed_time = 0
        while True:
            try:
                # display every interval secs
                task = self.display_queue.get(timeout=self.interval)
            except Empty:
                elapsed_time = time.time() - self.initial_time
                if elapsed_time > displayed_time:
                    displayed_time = elapsed_time
                if self.total_length == 0:
                    continue
                self.print_status(current_size=self.current_size,
                                  total_length=self.total_length,
                                  displayed_time=displayed_time,
                                  prefix=self.prefix)
                continue

            current_size, total_length = task
            displayed_time = time.time() - self.initial_time
            if self.total_length == 0:
                continue
            self.print_status(current_size=current_size,
                              total_length=total_length,
                              displayed_time=displayed_time,
                              prefix=self.prefix)
            self.display_queue.task_done()
            if current_size == total_length:
                # once we have done uploading everything return
                self.done_progress()
                return

    def update(self, size):
        """
        Update object size to be showed. This method called while uploading
        :param size: Object size to be showed. The object size should be in
                     bytes.
        """
        if not isinstance(size, int):
            raise ValueError('{} type can not be displayed. '
                             'Please change it to Int.'.format(type(size)))

        self.current_size += size
        self.display_queue.put((self.current_size, self.total_length))

    def done_progress(self):
        self.total_length = 0
        self.object_name = None
        self.last_printed_len = 0
        self.current_size = 0

    def print_status(self, current_size, total_length, displayed_time, prefix):
        formatted_str = prefix + format_string(
            current_size, total_length, displayed_time)
        self.stdout.write(_REFRESH_CHAR + formatted_str + ' ' *
                          max(self.last_printed_len - len(formatted_str), 0))
        self.stdout.flush()
        self.last_printed_len = len(formatted_str)


def seconds_to_time(seconds):
    """
    Consistent time format to be displayed on the elapsed time in screen.
    :param seconds: seconds
    """
    minutes, seconds = divmod(int(seconds), 60)
    hours, m = divmod(minutes, 60)
    if hours:
        return _HOURS_OF_ELAPSED % (hours, m, seconds)
    else:
        return _MINUTES_OF_ELAPSED % (m, seconds)


def format_string(current_size, total_length, elapsed_time):
    """
    Consistent format to be displayed on the screen.
    :param current_size: Number of finished object size
    :param total_length: Total object size
    :param elapsed_time: number of seconds passed since start
    """

    n_to_mb = current_size / _KILOBYTE / _KILOBYTE
    elapsed_str = seconds_to_time(elapsed_time)

    rate = _RATE_FORMAT % (
            n_to_mb / elapsed_time) if elapsed_time else _UNKNOWN_SIZE
    frac = float(current_size) / total_length
    bar_length = int(frac * _BAR_SIZE)
    bar = (_FINISHED_BAR * bar_length +
           _REMAINING_BAR * (_BAR_SIZE - bar_length))
    percentage = _PERCENTAGE_FORMAT % (frac * 100)
    left_str = (
        seconds_to_time(
            elapsed_time / current_size * (total_length - current_size))
        if current_size else _UNKNOWN_SIZE)

    humanized_total = _HUMANINZED_FORMAT % (
            total_length / _KILOBYTE / _KILOBYTE) + _STR_MEGABYTE
    humanized_n = _HUMANINZED_FORMAT % n_to_mb + _STR_MEGABYTE

    return _DISPLAY_FORMAT % (bar, humanized_n, humanized_total, percentage,
                              elapsed_str, left_str, rate)


def hash_files(file_path):
    try:
        # 判断传入的路径是否为文件
        if os.path.isfile(file_path):
            # 计算文件的相对路径和哈希值
            rel_path = os.path.basename(file_path)
            hash_value = calculate_file_hash(file_path)

            # 返回文件名、哈希值和相对路径
            return {'file_name': os.path.basename(file_path),
                    'file_hash': hash_value,
                    'rel_path': rel_path}

        else:
            print(f"The provided path '{file_path}' is not a file.")

    except Exception as e:
        print(f"Error processing file '{file_path}': {str(e)}")

    return None


def hash_files_in_directory(directory):
    file_hashes = []

    try:
        # 遍历指定目录下的所有文件
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)

                try:
                    # 计算文件的相对路径和哈希值
                    rel_path = os.path.relpath(file_path, directory)
                    hash_value = calculate_file_hash(file_path)

                    # 存储文件名、哈希值和相对路径到字典
                    file_info = {
                        'file_name': file,
                        'file_hash': hash_value,
                        'rel_path': rel_path
                    }
                    file_hashes.append(file_info)

                except Exception as e:
                    print(f"Error processing file '{file_path}': {str(e)}")

    except Exception as e:
        print(f"Error accessing directory '{directory}': {str(e)}")

    return file_hashes


def calculate_file_hash(file_path, algorithm='sha256', chunk_size=8192):
    # 使用指定哈希算法打开文件
    hasher = hashlib.new(algorithm)

    try:
        # 以二进制模式打开文件并逐块读取，更新哈希值
        with open(file_path, 'rb') as file:
            while chunk := file.read(chunk_size):
                hasher.update(chunk)

    except Exception as e:
        raise Exception(f"Error reading file '{file_path}': {str(e)}")

    # 返回最终的哈希值
    return hasher.hexdigest()
