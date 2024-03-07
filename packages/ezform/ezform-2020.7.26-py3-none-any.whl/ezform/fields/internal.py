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
# ezform.fields.internal

import datetime

from django.core.exceptions import ValidationError
from django.utils import formats

from ezform.encoding import StringEncoding


class FieldBackend:

    def __init__(self, parent=None):
        super().__init__()
        self._parent = parent

    def primitive_to_internal(self, data, raise_exc=False):
        raise NotImplementedError('virtual method')

    def internal_to_primitive(self, value, raise_exc=False):
        raise NotImplementedError('virtual method')

    def onError(self, exc=None):  # pylint: disable=W0613
        pass


class CompactText(FieldBackend):
    '''
    compact text
    '''

    def primitive_to_internal(self, data, raise_exc=False):
        if data in self._parent.empty_values:
            return getattr(self._parent, 'empty', None)

        try:
            return StringEncoding().decode(data)
        except Exception as _ex:  # pylint: disable=W0718
            if raise_exc:
                raise ValueError('Unable to decode input') from _ex
            else:
                self.onError(_ex)

    def internal_to_primitive(self, value, raise_exc=False):
        try:
            return StringEncoding().encode(value)
        except Exception as _ex:  # pylint: disable=W0718
            if raise_exc:
                raise ValueError('Unable to encode value') from _ex
            else:
                self.onError(_ex)


class DateRangeInput(FieldBackend):
    '''
    I deal with validating date range input and conversion between internal representation and primitive datatype
    '''

    VALUE_ANYDATE = 'Any Date'
    SEP = ' - '
    DEFAULT_OUTPUT_FORMAT = '%Y-%m-%d'

    error_messages = {
        'invalid': 'Invalid input',
    }
    EMPTY_INPUT_VALUES = (None, '')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_formats = formats.get_format_lazy('DATE_INPUT_FORMATS')

    def primitive_to_internal(self, data, raise_exc=False):

        if data in getattr(self._parent, 'empty_values', self.EMPTY_INPUT_VALUES):
            return tuple()
        if isinstance(data, tuple):
            return data

        value = data.strip()
        rval = tuple()
        if value:
            if value == self.VALUE_ANYDATE:
                rval = tuple()
            elif self.SEP in value:
                tokens = value.split(self.SEP)
                rval = (
                    self.token_to_date(tokens[0]),
                    self.token_to_date(tokens[1])
                )
        return rval

    def internal_to_primitive(self, value, raise_exc=False):
        rval = self.VALUE_ANYDATE
        if value:
            try:
                rval = '{a}{sep}{b}'.format(
                    a=self.date_to_token(value[0]),
                    b=self.date_to_token(value[1]),
                    sep=self.SEP,
                )
            except:  # pylint: disable=W0702
                pass
        return rval

    def strptime(self, value, format):  # pylint: disable=W0622
        '''
        adapted from `DateField`
        '''

        return datetime.datetime.strptime(value, format).date()

    def token_to_date(self, value):
        '''
        adapted from `BaseTemporalField`
        '''

        value = value.strip()
        for format in getattr(self._parent, 'input_formats', self.input_formats):  # pylint: disable=W0622
            try:
                return self.strptime(value, format)
            except (ValueError, TypeError):
                continue
        raise ValidationError(self.error_messages['invalid'], code='invalid')

    def date_to_token(self, value):
        return value.strftime(self.DEFAULT_OUTPUT_FORMAT)
