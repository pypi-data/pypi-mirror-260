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
# ezform.management.base

import json

from ezform.db import EzDBFactory


class ListLoader:

    def __init__(self, f):
        '''
        :param f: file-like object (file)
        '''

        super().__init__()
        assert f is not None
        self._input = f

    def do(self):
        raise NotImplementedError('virtual method')


class SkipListLoader(ListLoader):
    '''
    I load the skip-list into database
    '''

    CONFIG_LABEL = 'SKIP_LIST'

    @property
    def dbManager(self):
        return EzDBFactory().getManager(self.CONFIG_LABEL)

    def onReadInputError(self, exc=None):
        if getattr(self, 'use_exc', False):
            raise RuntimeError('fail to read input') from exc
        return None

    def onAddRecordError(self, exc=None):
        if getattr(self, 'use_exc', False):
            raise RuntimeError('error raises when adding record') from exc
        return None

    def readFromInput(self):
        self._pool = list()

        try:
            self._pool.extend(
                json.load(self._input)
            )
        except Exception as _ex:  # pylint: disable=W0718
            self.onReadInputError(_ex)
        return self

    def runAddLoop(self):
        for each in self._pool:
            self.addSingleRecord(each)
        return self

    def addSingleRecord(self, item):
        try:
            new_data = {
                'actual': item['date'],
            }

            origin = item.get('orig', None)
            if origin is not None:
                new_data['substitute'] = True
                new_data['origin'] = origin

            self.dbManager.model(**new_data)
        except Exception as _ex:  # pylint: disable=W0718
            self.onAddRecordError(_ex)
        return self

    def do(self):
        return self.readFromInput().runAddLoop()
