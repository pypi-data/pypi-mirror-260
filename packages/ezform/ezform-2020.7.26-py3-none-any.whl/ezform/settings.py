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
# ezform.settings

from django.test.signals import setting_changed
from dsgen import DSetting


class EzFormSetting(DSetting):
    SETTING_NAME = 'EZFORM_SETTING'
    DEFAULT = {
        'MODELS': {
            'SKIP_LIST': 'dummyapp.SkipDate',
        }
    }


ez_setting = EzFormSetting()
setting_changed.connect(ez_setting.signal_handler_setting_changed)
