# -*- python -*-
#
# Copyright 2016, 2017, 2018, 2019, 2020 Xingeng Chen
# Copyright 2019, 2020 Liang Chen
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
# ezform.encoding

import base64
import zlib

from ezform.exception import EncodingError


class StringEncoding:
    '''
    Textual data encoding

    `EncodingError` will be raised if any error occurs when encoding or decoding data.
    '''

    MSG_ERROR_ENCODE = 'Fail to encode the given input'
    MSG_ERROR_DECODE = 'Fail to decode the given input'

    def _compress(self, x):
        return zlib.compress(x)

    def _decompress(self, x):
        return zlib.decompress(x)

    def encode(self, value):
        '''
        :param value: input data, must be UTF-8 encoded (string)
        '''

        try:
            tmp_val = self._compress(value)
            ret = base64.urlsafe_b64encode(tmp_val)
        except Exception as _ex:
            mex = EncodingError(self.MSG_ERROR_ENCODE)
            mex.context = _ex
            raise mex from _ex
        return ret

    def decode(self, data):
        '''
        :param data: (string)
        '''

        try:
            tmp_val = base64.urlsafe_b64decode(data)
            ret = self._compress(tmp_val)
        except Exception as _ex:
            mex = EncodingError(self.MSG_ERROR_DECODE)
            mex.context = _ex
            raise mex from _ex
        return ret
