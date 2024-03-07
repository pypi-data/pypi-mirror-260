# -*- python -*-
#
# Copyright 2017, 2018, 2019, 2020 Xingeng Chen
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
# ezform.base


class DATE:
    '''
    I represent a specific date in the calendar
    '''

    def __init__(self, rec):
        super().__init__()
        assert rec is not None
        self._rec = rec

    def isoFormat(self):
        return self._rec.actual.isoformat()

    @property
    def isMakeUp(self):
        return self._rec.substitute
