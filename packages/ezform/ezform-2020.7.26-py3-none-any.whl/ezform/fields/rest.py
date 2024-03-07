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
# ezform.fields.rest

from rest_framework.fields import Field as _REST_Field

from .internal import DateRangeInput


class DateRangeField(_REST_Field):

    default_error_messages = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.backend = DateRangeInput(parent=self)

    def to_representation(self, value: tuple) -> str:
        return self.backend.internal_to_primitive(value)

    def to_internal_value(self, data: str) -> tuple:
        value = self.backend.primitive_to_internal(data)
        if (value is None or len(value) != 2) and not self.required:
            value = tuple()
        return value
