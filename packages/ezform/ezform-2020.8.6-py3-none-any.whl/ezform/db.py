# -*- python -*-
#
# Copyright 2018, 2019, 2020 Xingeng Chen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ezform.db

from django.apps import apps

from ezform.settings import ez_setting


class EzDBFactory:
    '''
    This class provides datamodel managers
    '''

    def __init__(self):
        super().__init__()
        self.setting = ez_setting
        self._cache_map = dict()

    def getManager(self, mod_config=None):
        '''
        :param mod_config: (string)
        '''

        assert mod_config is not None
        mod_name = self.setting.MODELS.get(mod_config, None)
        try:
            mod = self._get_model_cls(mod_name)
        except Exception as _ex:
            raise ValueError('invalid model config') from _ex
        return mod.objects

    def _get_model_cls(self, mod_name):
        try:
            mod = self._cache_map[mod_name]
        except KeyError:
            mod = apps.get_model(mod_name)
            self._cache_map[mod_name] = mod
        return mod
