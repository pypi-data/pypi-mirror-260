# -*- python -*-
#
# Copyright 2016, 2017, 2018, 2019, 2020 Xingeng Chen
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
# ezform.utils

from .base import DATE
from .db import EzDBFactory


class SkipDayProvider:
    '''
    I help looking up skip days
    '''

    CONFIG_LABEL = 'SKIP_LIST'

    def getSkipList(self, a, b):
        matches = list()
        qs = self.dbManager.filter(
            actual__gte=a
        ).filter(
            actual__lte=b
        ).order_by(
            'actual'
        )
        matches.extend(
            [ DATE(d) for d in qs ]
        )
        return matches

    @property
    def dbManager(self):
        return EzDBFactory().getManager(self.CONFIG_LABEL)


class DayCount:
    '''
    I can do day counting with skips
    '''

    def __init__(self, begin, end):
        '''
        :param begin: (datetime.date)
        :param end: (datetime.date)
        '''

        super().__init__()
        assert begin <= end
        self._begin = begin
        self._end = end
        self.setUp()

    def setUp(self):
        self.skipListProvider = SkipDayProvider()
        return self

    def getSkipCount(self):
        skips = self.skipListProvider.getSkipList(self._begin, self._end)
        return len(skips)

    def getGrossCount(self):
        gross = self._end - self._begin
        return gross.days

    def do(self):
        return self.getGrossCount() - self.getSkipCount()
