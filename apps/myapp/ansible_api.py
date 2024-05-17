#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import json
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

    def v2_runner_on_unreachable(self, result):
        host = result._host
        self.host_unreachable[host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        """Print a json representation of the result.

        Also, store the result in an instance attribute for retrieval later
        """
        host = result._host
        self.host_ok[host.get_name()] = result
        print(json.dumps({host.name: result._result}, indent=4))

    def v2_runner_on_failed(self, result, *args, **kwargs):
        host = result._host
        self.host_failed[host.get_name()] = result


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
                                        forks=10, verbosity=3, syntax=None, start_at_task=None,
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

    def run_playbook(self, playbooks):
        """
        run ansible palybook
        """
        try:
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
            print("error:", e)

    def print_results(self):
        self.display.v("Printing results.")
        print("UP ***********")
        for host, result in self.results_callback.host_ok.items():
            print('{0} >>> {1}'.format(host, result._result['stdout']))

        print("FAILED *******")
        for host, result in self.results_callback.host_failed.items():
            print('{0} >>> {1}'.format(host, result._result['msg']))

        print("DOWN *********")
        for host, result in self.results_callback.host_unreachable.items():
            print('{0} >>> {1}'.format(host, result._result['msg']))

    def get_result(self):
        self.results_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        for host, result in self.results_callback.host_ok.items():
            self.results_raw['success'][host] = result._result

        for host, result in self.results_callback.host_failed.items():
            self.results_raw['failed'][host] = result._result.get('msg') or result._result

        for host, result in self.results_callback.host_unreachable.items():
            self.results_raw['unreachable'][host] = result._result['msg']

        return self.results_raw


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
    ansible_runner = AnsibleRunner('/etc/ansible/hosts')
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
