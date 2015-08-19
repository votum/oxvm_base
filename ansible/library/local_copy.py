#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil
import time

DOCUMENTATION = '''
---
module: local_copy
short_description: Copies files within remote machine
description:
  - The M(local_copy) module copies a file within the remote box.
options:
  src:
    description:
      - Remote absolute path of a file to copy from.
    required: true
    default: null
    aliases: []
  dest:
    description:
      - Remote absolute path where the file should be copied to.
    required: true
    default: null
author:
    - "OXID eSales"
'''

EXAMPLES = '''
# Example from Ansible Playbooks
- copy: src=/remmote/path/a dest=/remote/path/b
'''

RETURN = '''
src_checksum:
  description: SHA1 checksum of source file
  return: success
  type: string
dest_checksum:
  description: SHA1 checksum of destination file
  return: success
  type: string
'''

def main():
  module = AnsibleModule(
    # not checking because of daisy chain to file module
    argument_spec = dict(
      src = dict(required=False),
      dest = dict(required=True),
    ),
    supports_check_mode=True,
  )

  # Initial state
  error_msg = None
  changed = True
  dest_checksum = None
  copy_needed = True

  # Get parameters
  src = os.path.expanduser(module.params['src'])
  dest = os.path.expanduser(module.params['dest'])

  # Preconditions
  if not os.path.exists(src):
    error_msg = "Source {0} does not exist".format(src)
  if not os.path.isfile(src):
    error_msg = "Source {0} is not a file".format(src)
  if not os.access(src, os.R_OK):
    error_msg = "Source {0} is not readable".format(src)

  if os.path.exists(dest) and not os.path.isfile(dest):
    error_msg = "Destination {0} already exists and it's not a file".format(dest)

  if error_msg:
    module.fail_json(msg=error_msg)

  # Check if copy is really necessary
  src_checksum = module.sha1(src)

  if os.path.exists(dest):
    dest_checksum = module.sha1(dest)

  if src_checksum == dest_checksum:
    changed = False
    copy_needed = False

  # Make copy if necessary
  if copy_needed:
    try:
      shutil.copyfile(src, dest)
      dest_checksum = module.sha1(dest)
    except:
      error_msg = "There was an error while making copy from {0} to {1}".format(src, dest)
      module.fail_json(msg=error_msg)

  # Form results
  res_args = {
    'changed': changed,
    'src_checksum': src_checksum,
    'dest_checksum': dest_checksum,
  }

  module.exit_json(**res_args)

# import module snippets
from ansible.module_utils.basic import *
main()
