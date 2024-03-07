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
# ezform.fields.html

import datetime

from django.core.exceptions import ValidationError
from django.forms.fields import CharField
from django.utils import formats
from django.utils.translation import gettext_lazy as _

from .internal import CompactText, DateRangeInput


class CompactTextField(CharField):
    '''
    compact text field
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.backend = CompactText(parent=self)

    def to_python(self, value):
        rval = None
        try:
            rval = self.backend.primitive_to_internal(value, raise_exc=True)
        except Exception as _ex:  # pylint: disable=W0718
            self.onError(_ex)
        return rval

    def onError(self, exc=None):  # pylint: disable=W0613
        return


class DateRangeField(CharField):
    '''
    customized date range field

    This class combines the logics from `CharField` and `DateField`.
    '''

    input_formats = formats.get_format_lazy('DATE_INPUT_FORMATS')
    default_error_messages = {
        'invalid': _('Enter a valid date.'),
    }

    def __init__(self, input_formats=None, **kwargs):
        super().__init__(**kwargs)
        if input_formats is not None:
            self.input_formats = input_formats
        self.backend = DateRangeInput(parent=self)

    def to_python(self, value):
        rval = self.backend.primitive_to_internal(value)
        return rval

    def validate(self, value):
        if value in self.empty_values:
            return None
        ex = ValidationError(
            self.error_messages['invalid'],
            code='invalid'
        )
        if len(value) not in (0, 2):
            raise ex
        for item in value:
            if not isinstance(item, datetime.date):
                raise ex
