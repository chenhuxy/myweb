#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
import logging
import shutil

import ansible.constants as C
from ansible import context
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory.group import Group
from ansible.inventory.host import Host
from ansible.inventory.manager import InventoryManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.plugins.callback import CallbackBase
from ansible.utils.display import Display
from ansible.vars.manager import VariableManager


# Create a callback plugin so we can capture the output
class ResultsCollectorJSONCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in.

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin.
    """

    def __init__(self, *args, **kwargs):
        super(ResultsCollectorJSONCallback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}
        self.task_results = []  # 初始化 task_results

    def v2_runner_on_unreachable(self, result):
        host = result._host
        self.host_unreachable.setdefault(host.get_name(), []).append(result)
        self.task_results.append({'host': host.get_name(), 'status': 'unreachable', 'result': result._result})
        # self.log_task_result(host, "unreachable", result._result)

    def v2_runner_on_ok(self, result, *args, **kwargs):
        """Print a json representation of the result.

        Also, store the result in an instance attribute for retrieval later
        """
        host = result._host
        self.host_ok.setdefault(host.get_name(), []).append(result)
        self.task_results.append({'host': host.get_name(), 'status': 'ok', 'result': result._result})
        # self.log_task_result(host, "ok", result._result)

    def v2_runner_on_failed(self, result, *args, **kwargs):
        host = result._host
        self.host_failed.setdefault(host.get_name(), []).append(result)
        self.task_results.append({'host': host.get_name(), 'status': 'failed', 'result': result._result})
        # self.log_task_result(host, "failed", result._result)

    def log_task_result(self, host, status, result):
        task_name = result.get('task', 'Unnamed Task')
        result_msg = result.get('msg', 'No message')
        logging.info(f"Task '{task_name}' on host '{host.get_name()}' - Status: {status} - Result: {result_msg}")
        self.task_results.append({
            'host': host.get_name(),
            'task': task_name,
            'status': status,
            'result': result_msg
        })


class AnsibleRunner(object):
    def __init__(self, sources):
        self.sources = sources
        self.display = Display()
        # Instantiate our ResultsCollectorJSONCallback for handling results as they come in.
        # Ansible expects this to be one of its main display outlets
        self.results_callback = ResultsCollectorJSONCallback()
        # initialize needed objects
        self.loader = DataLoader()  # Takes care of finding and reading yaml, json and ini import
        self.inventory = None
        self.variable_manager = None
        self.passwords = None
        self.tqm = None
        self._setup()
        self.results_raw = None

    def _setup(self):
        self.display.v("Inside setup method.")
        # since the API is constructed for CLI it expects certain options to always be set in the context object
        #  verbosity=3,
        context.CLIARGS = ImmutableDict(connection='smart', module_path=['~/.ansible/plugins/modules,'
                                                                         '/usr/share/ansible/plugins/modules'],
                                        forks=10, verbosity=0, syntax=None, start_at_task=None,
                                        become=None, become_method='sudo', become_user=None, check=False, diff=False,
                                        remote_user=None, ask_pass=False, private_key_file=None, ssh_common_args=None,
                                        ssh_extra_args=None,
                                        sftp_extra_args=None, scp_extra_args=None, ask_vault_pass=False,
                                        vault_password_file=None, vault_id=None,
                                        listhosts=False, deprecation_warnings=False,
                                        listtasks=False, listtags=False, ask_become_pass=False,
                                        )
        """
        # required for
        # https://github.com/ansible/ansible/blob/devel/lib/ansible/inventory/manager.py#L204
        sources = ','.join(self.host_list)
        if len(self.host_list) == 1:
          sources += ','
        # create inventory, use path to host config file as source or hosts in a comma separated string
        """
        self.inventory = InventoryManager(loader=self.loader, sources=self.sources)

        # self.inventory = MyInventory(resources=self.sources)
        # variable manager takes care of merging all the different sources
        # to give you a unified view of variables available in each context
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        # self.passwords = dict(vault_pass='secret')
        # self.passwords = dict(conn_pass='secret')

    def _cleanup(self):
        if self.tqm is not None:
            self.tqm.cleanup()
        if self.loader:
            self.loader.cleanup_all_tmp_files()
        # Remove ansible tmpdir
        shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

    def run(self, hosts, module_name, module_args):
        self.display.v("Inside run_playbook method.")
        play_source = dict(
            name="Ansible Play",
            hosts=hosts,
            gather_facts='no',
            tasks=[
                # dict(action=dict(module='shell', args='ls'), register='shell_out'),
                # dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}'))),
                # dict(action=dict(module='command', args=dict(cmd='/usr/bin/uptime'))),
                dict(action=dict(module=module_name, args=module_args))
            ]
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        # instantiate task queue manager, which takes care of forking and setting up all objects to iterate over host
        # list and tasks IMPORTANT: This also adds library dirs paths to the module loader IMPORTANT: and so it must
        # be initialized before calling `Play.load()`.
        self.tqm = TaskQueueManager(
            inventory=self.inventory,
            variable_manager=self.variable_manager,
            loader=self.loader,
            passwords=self.passwords,
            # Use our custom callback instead of the ``default`` callback plugin,
            # which prints to stdout
            stdout_callback=self.results_callback,

        )
        try:
            result = self.tqm.run(play)  # most interesting data for a play is actually sent to the callback's methods
        finally:
            # we always need to cleanup child procs and the structures we use to communicate with them
            self._cleanup()

    def run_playbook(self, playbooks, tags=None):
        """
        run ansible palybook
        """
        try:
            # 创建新的 ImmutableDict 包含 tags
            cliargs = {**context.CLIARGS, 'tags': tags.split(',') if tags else []}
            context.CLIARGS = ImmutableDict(cliargs)

            # 调试日志
            logging.info(f"Running playbook with CLIARGS: {context.CLIARGS}")

            # actually run it
            self.tqm = PlaybookExecutor(
                playbooks=playbooks,
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                passwords=self.passwords,
            )
            self.tqm._tqm._stdout_callback = self.results_callback
            self.tqm.run()
        except Exception as e:
            logging.error(f"An error occurred while running the playbook: {e}")

    def print_results(self):
        self.display.v("Printing results.")

        # Collect task results
        task_results = {}

        # Collect host status
        host_stats = {
            'up': {},
            'failed': {},
            'down': {}
        }

        print("Up ************************************************************************************")
        for host, results in self.results_callback.host_ok.items():
            host_stats['up'][host] = len(results)
            for result in results:
                stdout = result._result.get('stdout')
                task_name = result._task.get_name() if hasattr(result,
                                                               '_task') and result._task is not None else 'Unknown Task'
                if stdout is not None:
                    print(f'{host} >>> Task: {task_name}, Stdout: {stdout}')
                else:
                    print(f'{host} >>> Task: {task_name}, No stdout available')

        print("Failed ************************************************************************************")
        for host, results in self.results_callback.host_failed.items():
            host_stats['failed'][host] = len(results)
            for result in results:
                msg = result._result.get('msg')
                task_name = result._task.get_name() if hasattr(result,
                                                               '_task') and result._task is not None else 'Unknown Task'
                if msg is not None:
                    print(f'{host} >>> Task: {task_name}, Error: {msg}')
                else:
                    print(f'{host} >>> Task: {task_name}, No error message available')

        print("Down ************************************************************************************")
        for host, results in self.results_callback.host_unreachable.items():
            host_stats['down'][host] = len(results)
            for result in results:
                msg = result._result.get('msg')
                task_name = result._task.get_name() if hasattr(result,
                                                               '_task') and result._task is not None else 'Unknown Task'
                if msg is not None:
                    print(f'{host} >>> Task: {task_name}, Error: {msg}')
                else:
                    print(f'{host} >>> Task: {task_name}, No error message available')
            '''
            # Print task results
            print("TASK RESULTS *********")
            for result in self.results_callback.task_results:
                host = result.get('host', 'Unknown Host')
                status = result.get('status', 'Unknown Status')
                result_msg = result.get('result', 'No result message')

                # Get task name from result
                task_name = result.get('task', 'Unknown Task')
                if task_name == 'Unknown Task':
                    # If task name is not directly available, try to get it from the result's task object
                    task_name = result.get('_task', {}).get('_attributes', {}).get('name', 'Unknown Task')

                # Update host status
                if status == 'ok':
                    host_stats['up'][host] = host_stats['up'].get(host, 0) + 1
                elif status == 'failed':
                    host_stats['failed'][host] = host_stats['failed'].get(host, 0) + 1
                elif status == 'unreachable':
                    host_stats['down'][host] = host_stats['down'].get(host, 0) + 1

                # Print task result
                print(f"TASK [{task_name}] ******************************************")
                print(f" {status}: [{host}]")
            '''
        # 打印任务统计结果
        print("TASK STATISTICS ************************************************************************************")
        for status, hosts in host_stats.items():
            for host, count in hosts.items():
                print(f'{host} >>> {status.capitalize()}: {count}')

    def get_result(self):
        self.results_raw = {'success': {}, 'failed': {}, 'unreachable': {}}

        for host, results in self.results_callback.host_ok.items():
            for result in results:
                task_name = result._task.get_name() if hasattr(result,
                                                               '_task') and result._task is not None else 'Unknown Task'
                stdout = result._result.get('stdout')
                if stdout is not None:
                    self.results_raw['success'][host] = self.results_raw['success'].get(host, []) + [{
                        'task': task_name,
                        'stdout': stdout
                    }]
                else:
                    self.results_raw['success'][host] = self.results_raw['success'].get(host, []) + [{
                        'task': task_name,
                        'stdout': 'No stdout available'
                    }]

        for host, results in self.results_callback.host_failed.items():
            for result in results:
                task_name = result._task.get_name() if hasattr(result,
                                                               '_task') and result._task is not None else 'Unknown Task'
                msg = result._result.get('msg')
                if msg is not None:
                    self.results_raw['failed'][host] = self.results_raw['failed'].get(host, []) + [{
                        'task': task_name,
                        'msg': msg
                    }]
                else:
                    self.results_raw['failed'][host] = self.results_raw['failed'].get(host, []) + [{
                        'task': task_name,
                        'msg': 'No error message available'
                    }]

        for host, results in self.results_callback.host_unreachable.items():
            for result in results:
                task_name = result._task.get_name() if hasattr(result,
                                                               '_task') and result._task is not None else 'Unknown Task'
                msg = result._result.get('msg')
                if msg is not None:
                    self.results_raw['unreachable'][host] = self.results_raw['unreachable'].get(host, []) + [{
                        'task': task_name,
                        'msg': msg
                    }]
                else:
                    self.results_raw['unreachable'][host] = self.results_raw['unreachable'].get(host, []) + [{
                        'task': task_name,
                        'msg': 'No error message available'
                    }]

        # print(self.results_raw)

        # return self.results_raw

        # 以主机维度统计各个状态值
        host_status_count = {}

        for status, hosts in self.results_raw.items():
            for host, tasks in hosts.items():
                host_status_count.setdefault(host, {"success": 0, "failed": 0, "unreachable": 0})
                if isinstance(tasks, list):
                    host_status_count[host][status] += len(tasks)
                else:
                    host_status_count[host][status] += 1

        return host_status_count


if __name__ == "__main__":
    # host_list = ['localhost', '192.168.38.132', 'www.google.com']
    resource = [
        {'hostname': 'localtest', 'ip': 'localhost', 'username': 'root', 'password': 'redhat'},
        {'hostname': 'localtest2', 'ip': '192.168.38.132', 'username': 'root', 'password': 'redhat'}
        # 有个小坑，hostname中不能有空格，否则这个host会被ansible无视
    ]
    resource_data = {
        "group1": {
            "hosts": [{"hostname": "10.0.0.0", "port": 22, "username": "test", "password": "pass"}],
            "vars": {"var1": "value1", "var2": "value2"}
        }
    }
    playbooks = ['/etc/ansible/core-start.yml']
    ansible_runner = AnsibleRunner('/etc/ansible/core-start.ini')
    # ansible_runner.run()

    # 开始模拟以ad-hoc方式运行ansible命令
    ansible_runner.run(
        ['test'],  # 指出本次运行涉及的主机，在resource中定义
        'command',  # 本次运行使用的模块
        'hostname'  # 模块的参数
    )
    ansible_runner.run_playbook(playbooks)
    ansible_runner.print_results()
    # 获取结果，是一个字典格式，如果是print可以用json模块美化一下
    # print(json.dumps(ansible_runner.get_result(), indent=4))
