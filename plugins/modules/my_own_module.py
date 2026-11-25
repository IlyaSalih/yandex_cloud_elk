#!/usr/bin/python

# Copyright: (c) 2026, Ilya Salih
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: Creates a text file with given content

version_added: "1.0.0"

description:
    - Module creates a text file on the remote host at the path
      defined in the C(path) parameter with the content defined
      in the C(content) parameter. Idempotent - if the file already
      exists with the same content, nothing is changed.

options:
    path:
        description: Absolute path of the file to create.
        required: true
        type: str
    content:
        description: Content of the file.
        required: true
        type: str

author:
    - Ilya Salih (@IlyaSalih)
'''

EXAMPLES = r'''
# Create a text file
- name: Create file with my_own_module
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/my_file.txt
    content: "Hello world"
'''

RETURN = r'''
path:
    description: Path of the file.
    type: str
    returned: always
    sample: '/tmp/my_file.txt'
message:
    description: Human-readable result of the execution.
    type: str
    returned: always
    sample: 'File created'
'''

import os

from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        path='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']
    result['path'] = path

    # Идемпотентность: если файл существует и содержимое совпадает - ничего не делаем
    if os.path.exists(path):
        with open(path, 'r') as f:
            current_content = f.read()
        if current_content == content:
            result['message'] = 'File already exists with the same content'
            module.exit_json(**result)

    # Check mode: сообщаем, что файл был бы изменён, но ничего не трогаем
    if module.check_mode:
        result['changed'] = True
        result['message'] = 'File would be created or updated (check mode)'
        module.exit_json(**result)

    try:
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        with open(path, 'w') as f:
            f.write(content)
    except OSError as e:
        module.fail_json(msg='Failed to write file: %s' % str(e), **result)

    result['changed'] = True
    result['message'] = 'File created or updated'
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
