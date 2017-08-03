# -*- coding: utf-8 -*-
# MIT LICENSE
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from enum import Flag, unique
from datetime import datetime, timedelta, date


@unique
class WeekDay(Flag):
    monday    = 1 << 0
    tuesday   = 1 << 1
    wednesday = 1 << 2
    thursday  = 1 << 3
    friday    = 1 << 4
    saturday  = 1 << 5
    sunday    = 1 << 6
    weekday   = monday | tuesday | wednesday | thursday | friday
    weekend   = saturday | sunday

    def __str__(self):
        return self.name.capitalize()


class Week:
    def __init__(self, year: int, week: int):
        self.monday = datetime.strptime('{:4d}-{:2d}-mon'.format(year, week), '%Y-%W-%a').date()
        if date(year, 1, 4).isoweekday() > 4:
            self.monday -= timedelta(days=7)
        self.tuesday = self.monday + timedelta(days=1)
        self.wednesday = self.monday + timedelta(days=2)
        self.thursday = self.monday + timedelta(days=3)
        self.friday = self.monday + timedelta(days=4)
        self.saturday = self.monday + timedelta(days=5)
        self.sunday = self.monday + timedelta(days=6)


def get_day_of_the_week_from_date(value: date) -> WeekDay:
    return WeekDay(1 << value.weekday())


def get_first_weekend_after_date(value: date) -> {date, date}:
    weekend = set()
    day_of_week = get_day_of_the_week_from_date(value)
    if day_of_week == WeekDay.monday:
        weekend.add(value + timedelta(days=5))
        weekend.add(value + timedelta(days=6))
    elif day_of_week == WeekDay.tuesday:
        weekend.add(value + timedelta(days=4))
        weekend.add(value + timedelta(days=5))
    elif day_of_week == WeekDay.wednesday:
        weekend.add(value + timedelta(days=3))
        weekend.add(value + timedelta(days=4))
    elif day_of_week == WeekDay.thursday:
        weekend.add(value + timedelta(days=2))
        weekend.add(value + timedelta(days=3))
    elif day_of_week == WeekDay.friday:
        weekend.add(value + timedelta(days=1))
        weekend.add(value + timedelta(days=2))
    elif day_of_week == WeekDay.saturday:
        weekend.add(value + timedelta(days=0))
        weekend.add(value + timedelta(days=1))
    elif day_of_week == WeekDay.sunday:
        weekend.add(value + timedelta(days=-1))
        weekend.add(value + timedelta(days=0))
    return weekend


def get_weekends_from_period(first_date: date, last_date: date) -> []:
    weekends = []
    next_date = first_date
    while next_date <= last_date:
        weekends.append(get_first_weekend_after_date(next_date))
        next_date += timedelta(days=7)
    return weekends