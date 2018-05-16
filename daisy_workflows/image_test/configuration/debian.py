#!/usr/bin/env python2
# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import generic_distro
import utils


class DebianTests(generic_distro.GenericDistroTests):
  def TestPackageInstallation(self):
    utils.Execute(['apt-get', 'update'])
    utils.Execute(['apt-get', 'install', '--reinstall', '-y', 'tree'])

  def IsPackageInstalled(self, package_name):
    # the following command returns zero if package is installed
    rc, output = utils.Execute(['dpkg', '-s', package_name],
                               raise_errors=False)
    return rc == 0

  def GetGoogleAptSource(self):
    return 'packages.cloud.google.com'

  def TestPackageManagerConfig(self):
    desired_source = self.GetGoogleAptSource()
    command = ['grep', '-r', desired_source, '/etc/apt/']
    utils.Execute(command)

  def TestAutomaticSecurityUpdates(self):
    package_name = 'unattended-upgrades'
    if not self.IsPackageInstalled(package_name):
      raise Exception('%s package is not installed' % package_name)

    # check unattended upgrade configuration
    command = ['unattended-upgrade', '-v']
    rc, output = utils.Execute(command, capture_output=True)
    for line in output.split('\n'):
      token = "Allowed origins are:"
      if line.find(token) >= 0:
        if len(line) > len(token):
          # There is some repository used for unattended upgrades
          return
    raise Exception('No origin repository used by unattended-upgrade')
