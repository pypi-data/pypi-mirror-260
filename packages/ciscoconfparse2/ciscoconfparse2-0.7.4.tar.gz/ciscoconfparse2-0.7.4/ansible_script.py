"""
See:
    https://docs.ansible.com/ansible/latest/dev_guide/developing_api.html

This API is intended for internal Ansible use. Ansible may make
changes to this API at any time that could break backward compatibility
with older versions of the API. Because of this, external use is not
supported by Ansible. If you want to use Python API only for executing
playbooks or modules, consider ansible-runner first.
"""

from ansible import context
from ansible.cli import CLI
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.playbook.play import Play
from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
import yaml

from ansible.plugins.callback import CallbackBase


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
        self.result = None

    def v2_runner_on_unreachable(self, result):
        host = result._host
        self.host_unreachable[host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        """Print a json representation of the result.

        Also, store the result in an instance attribute for retrieval later
        """
        host = result._host
        self.host_ok[host.get_name()] = result

        self.result = result._result
        self.host = host

    def v2_hostname(self):
        return self.host.name

    def v2_stdout(self):
        return self.result["stdout"]

    def v2_stderr(self):
        return self.result["stderr"]

    def v2_runner_on_failed(self, result, *args, **kwargs):
        host = result._host
        self.host_failed[host.get_name()] = result


def complex_ansible_stdout(inventory_path="inventory.ini",
                           playbook_path="playbook.yml") -> str:
    """Get stdout from a playbook run using TaskQueueManager()"""

    loader = DataLoader()

    # Define the ansible context variables
    context.CLIARGS = ImmutableDict(tags={},
                                    listtags=False,
                                    listtasks=False,
                                    listhosts=False,
                                    syntax=False,
                                    connection='ssh',
                                    module_path=None,
                                    forks=100,
                                    remote_user='mpenning',
                                    private_key_file=None,
                                    ssh_common_args=None,
                                    ssh_extra_args=None,
                                    sftp_extra_args=None,
                                    scp_extra_args=None,
                                    become=False,
                                    become_method='sudo',
                                    become_user='root',
                                    verbosity=True,
                                    check=False,
                                    start_at_task=None)

    # Build an inventory object from the inventory filepath
    inventory = InventoryManager(loader=loader, sources=(inventory_path,))

    variable_manager = VariableManager(loader=loader,
                                       inventory=inventory,
                                       version_info=CLI.version_info(gitinfo=False))

    results_callback = ResultsCollectorJSONCallback()

    passwords = {}

    tqm = TaskQueueManager(
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,
        passwords=passwords,
        # Use our custom callback instead of the ``default`` callback plugin, 
        # which prints to stdout
        stdout_callback=results_callback,
    )

    with open(playbook_path) as fd:
        playbook = yaml.safe_load(fd)

    play = Play().load(playbook[0],
                       variable_manager=variable_manager,
                       loader=loader)

    result = tqm.run(play)
    if tqm is not None:
        tqm.cleanup()

    # Return stdout from the ansible_playbook run
    return results_callback.v2_stdout()


if __name__ == "__main__":
    stdout = complex_ansible_stdout("ansible_inventory.ini",
                                    "ansible_playbook.yml")
    print(stdout)
