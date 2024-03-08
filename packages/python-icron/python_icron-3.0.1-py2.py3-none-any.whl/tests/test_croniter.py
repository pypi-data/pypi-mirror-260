from datetime import datetime, timedelta
from time import sleep
import pytz

import pytest
import dateutil.tz

from icron import (
    croniter,
    croniter_range,
    CroniterBadDateError,
    CroniterBadCronError,
    datetime_to_timestamp,
    CroniterNotAlphaError,
    CroniterUnsupportedSyntaxError
)


def testOddRule():
    croniter('0 49 12,14,16 * * *', datetime(2023, 1, 1))


def testSecondSec():
    base = datetime(2012, 4, 6, 13, 26, 10)
    itr = croniter('15,25 * * * * *', base)
    n = itr.get_next(datetime)
    assert 15 == n.second
    n = itr.get_next(datetime)
    assert 25 == n.second
    n = itr.get_next(datetime)
    assert 15 == n.second
    assert 27 == n.minute


def testSecond():
    base = datetime(2012, 4, 6, 13, 26, 10)
    itr = croniter('*/1 * * * * *', base)
    n1 = itr.get_next(datetime)
    assert base.year == n1.year
    assert base.month == n1.month
    assert base.day == n1.day
    assert base.hour == n1.hour
    assert base.minute == n1.minute
    assert base.second + 1 == n1.second


def testSecond2():
    base = datetime(2023, 1, 1, 0, 0, 0)
    itr = croniter('* * * * * *', base)
    n1 = itr.get_next(datetime)
    assert base.year == n1.year
    assert base.month == n1.month
    assert base.day == n1.day
    assert base.hour == n1.hour
    assert base.minute == n1.minute
    assert base.second + 1 == n1.second


def testSecond3():
    base = datetime(2012, 4, 6, 13, 26, 36)
    itr = croniter('*/15 * * * * *', base)
    n1 = itr.get_next(datetime)
    n2 = itr.get_next(datetime)
    n3 = itr.get_next(datetime)
    assert base.year == n1.year
    assert base.month == n1.month
    assert base.day == n1.day
    assert base.hour == n1.hour
    assert base.minute == n1.minute
    assert 45 == n1.second
    assert base.year == n2.year
    assert base.month == n2.month
    assert base.day == n2.day
    assert base.hour == n2.hour
    assert base.minute + 1 == n2.minute
    assert 0 == n2.second
    assert base.year == n3.year
    assert base.month == n3.month
    assert base.day == n3.day
    assert base.hour == n3.hour
    assert base.minute + 1 == n3.minute
    assert 15 == n3.second


def testMinute():
    # minute asterisk
    base = datetime(2010, 1, 23, 12, 18)
    itr = croniter('*/1 * * * *', base)
    n1 = itr.get_next(datetime)    # 19
    assert base.year == n1.year
    assert base.month == n1.month
    assert base.day == n1.day
    assert base.hour == n1.hour
    assert base.minute == n1.minute - 1

    for i in range(39):  # ~ 58
        itr.get_next()

    n2 = itr.get_next(datetime)
    assert n2.minute == 59
    n3 = itr.get_next(datetime)
    assert n3.minute == 0
    assert n3.hour == 13

    itr = croniter('*/5 * * * *', base)
    n4 = itr.get_next(datetime)
    assert n4.minute == 20
    for i in range(6):
        itr.get_next()
    n5 = itr.get_next(datetime)
    assert n5.minute == 55
    n6 = itr.get_next(datetime)
    assert n6.minute == 0
    assert n6.hour == 13


def testHour():
    base = datetime(2010, 1, 24, 12, 2)
    itr = croniter('0 */3 * * *', base)
    n1 = itr.get_next(datetime)
    assert n1.hour == 15
    assert n1.minute == 0
    for i in range(2):
        itr.get_next()
    n2 = itr.get_next(datetime)
    assert n2.hour == 0
    assert n2.day == 25


def testDay():
    base = datetime(2010, 2, 24, 12, 9)
    itr = croniter('0 0 */3 * *', base)
    n1 = itr.get_next(datetime)
    # 1 4 7 10 13 16 19 22 25 28
    assert n1.day == 25
    n2 = itr.get_next(datetime)
    assert n2.day == 28
    n3 = itr.get_next(datetime)
    assert n3.day == 1
    assert n3.month == 3

    # test leap year
    base = datetime(1996, 2, 27)
    itr = croniter('0 0 * * *', base)
    n1 = itr.get_next(datetime)
    assert n1.day == 28
    assert n1.month == 2
    n2 = itr.get_next(datetime)
    assert n2.day == 29
    assert n2.month == 2

    base2 = datetime(2000, 2, 27)
    itr2 = croniter('0 0 * * *', base2)
    n3 = itr2.get_next(datetime)
    assert n3.day == 28
    assert n3.month == 2
    n4 = itr2.get_next(datetime)
    assert n4.day == 29
    assert n4.month == 2


def testWeekDay():
    base = datetime(2010, 2, 25)
    itr = croniter('0 0 * * sat', base)
    n1 = itr.get_next(datetime)
    assert n1.isoweekday() == 6
    assert n1.day == 27
    n2 = itr.get_next(datetime)
    assert n2.isoweekday() == 6
    assert n2.day == 6
    assert n2.month == 3

    base = datetime(2010, 1, 25)
    itr = croniter('0 0 1 * wed', base)
    n1 = itr.get_next(datetime)
    assert n1.month == 1
    assert n1.day == 27
    assert n1.year == 2010
    n2 = itr.get_next(datetime)
    assert n2.month == 2
    assert n2.day == 1
    assert n2.year == 2010
    n3 = itr.get_next(datetime)
    assert n3.month == 2
    assert n3.day == 3
    assert n3.year == 2010


def testNthWeekDay():
    base = datetime(2010, 2, 25)
    itr = croniter('0 0 * * sat#1', base)
    n1 = itr.get_next(datetime)
    assert n1.isoweekday() == 6
    assert n1.day == 6
    assert n1.month == 3
    n2 = itr.get_next(datetime)
    assert n2.isoweekday() == 6
    assert n2.day == 3
    assert n2.month == 4

    base = datetime(2010, 1, 25)
    itr = croniter('0 0 * * wed#5', base)
    n1 = itr.get_next(datetime)
    assert n1.month == 3
    assert n1.day == 31
    assert n1.year == 2010
    n2 = itr.get_next(datetime)
    assert n2.month == 6
    assert n2.day == 30
    assert n2.year == 2010
    n3 = itr.get_next(datetime)
    assert n3.month == 9
    assert n3.day == 29
    assert n3.year == 2010


def testWeekDayDayAnd():
    base = datetime(2010, 1, 25)
    itr = croniter('0 0 1 * mon', base, day_or=False)
    n1 = itr.get_next(datetime)
    assert n1.month == 2
    assert n1.day == 1
    assert n1.year == 2010
    n2 = itr.get_next(datetime)
    assert n2.month == 3
    assert n2.day == 1
    assert n2.year == 2010
    n3 = itr.get_next(datetime)
    assert n3.month == 11
    assert n3.day == 1
    assert n3.year == 2010


def testDomDowVixieCronBug():
    expr = '0 16 */2 * sat'

    # UNION OF "every odd-numbered day" and "every Saturday"
    itr = croniter(expr, start_time=datetime(2023, 5, 2), ret_type=datetime)
    assert itr.get_next() == datetime(2023, 5, 3, 16, 0, 0)    # Wed May 3 2023
    assert itr.get_next() == datetime(2023, 5, 5, 16, 0, 0)    # Fri May 5 2023
    assert itr.get_next() == datetime(2023, 5, 6, 16, 0, 0)    # Sat May 6 2023
    assert itr.get_next() == datetime(2023, 5, 7, 16, 0, 0)    # Sun May 7 2023

    # INTERSECTION OF "every odd-numbered day" and "every Saturday"
    itr = croniter(expr, start_time=datetime(2023, 5, 2), ret_type=datetime, implement_cron_bug=True)
    assert itr.get_next() == datetime(2023, 5, 13, 16, 0, 0)    # Sat May  13 2023
    assert itr.get_next() == datetime(2023, 5, 27, 16, 0, 0)    # Sat May  27 2023
    assert itr.get_next() == datetime(2023, 6, 3, 16, 0, 0)     # Sat June  3 2023
    assert itr.get_next() == datetime(2023, 6, 17, 16, 0, 0)    # Sun June 17 2023


def testMonth():
    base = datetime(2010, 1, 25)
    itr = croniter('0 0 1 * *', base)
    n1 = itr.get_next(datetime)
    assert n1.month == 2
    assert n1.day == 1
    n2 = itr.get_next(datetime)
    assert n2.month == 3
    assert n2.day == 1
    for i in range(8):
        itr.get_next()
    n3 = itr.get_next(datetime)
    assert n3.month == 12
    assert n3.year == 2010
    n4 = itr.get_next(datetime)
    assert n4.month == 1
    assert n4.year == 2011


def testLastDayOfMonth():
    base = datetime(2015, 9, 4)
    itr = croniter('0 0 l * *', base)
    n1 = itr.get_next(datetime)
    assert n1.month == 9
    assert n1.day == 30
    n2 = itr.get_next(datetime)
    assert n2.month == 10
    assert n2.day == 31
    n3 = itr.get_next(datetime)
    assert n3.month == 11
    assert n3.day == 30
    n4 = itr.get_next(datetime)
    assert n4.month == 12
    assert n4.day == 31


def testRangeWithUppercaseLastDayOfMonth():
    base = datetime(2015, 9, 4)
    itr = croniter('0 0 29-L * *', base)
    n1 = itr.get_next(datetime)
    assert n1.month == 9
    assert n1.day == 29
    n2 = itr.get_next(datetime)
    assert n2.month == 9
    assert n2.day == 30


def testError():
    itr = croniter('* * * * *')
    assert pytest.raises(TypeError, itr.get_next, str)
    assert pytest.raises(ValueError, croniter, '* * * *')
    assert pytest.raises(ValueError, croniter, '* * 5-1 * *')
    assert pytest.raises(ValueError, croniter, '-90 * * * *')
    assert pytest.raises(ValueError, croniter, 'a * * * *')
    assert pytest.raises(ValueError, croniter, '* * * janu-jun *')
    assert pytest.raises(ValueError, croniter, '1-1_0 * * * *')
    assert pytest.raises(ValueError, croniter, '0-10/ * * * *')
    assert pytest.raises(CroniterBadCronError, croniter, "0-1& * * * *", datetime.now())


def testSundayToThursdayWithAlphaConversion():
    base = datetime(2010, 8, 25, 15, 56)  # wednesday
    itr = croniter("30 22 * * sun-thu", base)
    next = itr.get_next(datetime)

    assert base.year == next.year
    assert base.month == next.month
    assert base.day == next.day
    assert 22 == next.hour
    assert 30 == next.minute


def testOptimizeCronExpressions():
    """ Non-optimal cron expressions that can be simplified."""
    wildcard = ['*']
    # Test each field individually
    m, h, d, mon, dow = range(5)
    assert croniter('0-59 0 1 1 0').expanded[m] == wildcard
    assert croniter('0 0-23 1 1 0').expanded[h] == wildcard
    assert croniter('0 0 1-31 1 0').expanded[d] == wildcard
    assert croniter('0 0 1 1-12 0').expanded[mon] == wildcard
    assert croniter('0 0 1 1 0-6').expanded[dow] == wildcard
    assert croniter('0 0 1 1 1-7').expanded[dow] == wildcard
    # Real life examples
    assert croniter('30 1-12,0,10-23 15-21 * fri').expanded[h] == wildcard
    assert croniter('30 1-23,0 15-21 * fri').expanded[h] == wildcard
    assert croniter('0 0 1 1 1-7,sat#3').expanded[dow] == wildcard
    s, m, h, d, mon, dow = range(6)
    assert croniter('0-59 0 1 1 1 0').expanded[s] == wildcard


def testBlockDupRanges():
    """ Ensure that duplicate/overlapping ranges are squashed """
    s, m, h, d, mon, dow = range(6)
    assert croniter('* * 5,5,1-6 * *').expanded[h] == [1,2,3,4,5,6]
    assert croniter('* * * * 2-3,4-5,3,3,3').expanded[dow - 1] == [2,3,4,5]
    assert croniter('1,5,*/20,20,15 * * * * *').expanded[s] == [0, 1, 5, 15, 20, 40]
    assert croniter('* * 4,1-4,5,4 * *').expanded[h] == [1, 2, 3, 4, 5]
    # Real life example
    assert croniter('59 23 * 1 wed,fri,mon-thu,tue,tue').expanded[dow - 1] == [1,2,3,4,5]


def testISOWeekday():
    base = datetime(2010, 2, 25)
    assert croniter.expand('0 0 * * 7')[0] == [[0], [0], ['*'], ['*'], [0]]
    itr = croniter('0 0 * * 7', base)
    n1 = itr.get_next(datetime)
    assert n1.isoweekday() == 7
    assert n1.day == 28
    n2 = itr.get_next(datetime)
    assert n2.isoweekday() == 7
    assert n2.day == 7
    assert n2.month == 3


def testBug2():
    base = datetime(2012, 1, 1, 0, 0)
    iter = croniter('0 * * 3 *', base)
    n1 = iter.get_next(datetime)
    assert n1.year == base.year
    assert n1.month == 3
    assert n1.day == base.day
    assert n1.hour == base.hour
    assert n1.minute == base.minute

    n2 = iter.get_next(datetime)
    assert n2.year == base.year
    assert n2.month == 3
    assert n2.day == base.day
    assert n2.hour == base.hour + 1
    assert n2.minute == base.minute

    n3 = iter.get_next(datetime)
    assert n3.year == base.year
    assert n3.month == 3
    assert n3.day == base.day
    assert n3.hour == base.hour + 2
    assert n3.minute == base.minute


def testBug3():
    base = datetime(2013, 3, 1, 12, 17, 34, 257877)
    c = croniter('00 03 16,30 * *', base)

    n1 = c.get_next(datetime)
    assert n1.month == 3
    assert n1.day == 16

    n2 = c.get_next(datetime)
    assert n2.month == 3
    assert n2.day == 30

    n3 = c.get_next(datetime)
    assert n3.month == 4
    assert n3.day == 16


def test_bug34():
    # we can do better: forbid this
    base = datetime(2012, 2, 24, 0, 0, 0)
    itr = croniter('* * 31 2 *', base)
    try:
        itr.get_next(datetime)
    except (CroniterBadDateError,) as ex:
        assert "{0}".format(ex)[:24] == 'failed to find next date'


def testBug57():
    base = datetime(2012, 2, 24, 0, 0, 0)
    itr = croniter('0 4/6 * * *', base)
    n1 = itr.get_next(datetime)
    assert n1.hour == 4
    assert n1.minute == 0
    assert n1.month == 2
    assert n1.day == 24

    itr = croniter('0 0/6 * * *', base)
    n1 = itr.get_next(datetime)
    assert n1.hour == 6
    assert n1.minute == 0
    assert n1.month == 2
    assert n1.day == 24


def test_multiple_months():
    base = datetime(2016, 3, 1, 0, 0, 0)
    itr = croniter('0 0 1 3,6,9,12 *', base)
    n1 = itr.get_next(datetime)
    assert n1.hour == 0
    assert n1.month == 6
    assert n1.day == 1
    assert n1.year == 2016

    base = datetime(2016, 2, 15, 0, 0, 0)
    itr = croniter('0 0 1 3,6,9,12 *', base)
    n1 = itr.get_next(datetime)
    assert n1.hour == 0
    assert n1.month == 3
    assert n1.day == 1
    assert n1.year == 2016

    base = datetime(2016, 12, 3, 10, 0, 0)
    itr = croniter('0 0 1 3,6,9,12 *', base)
    n1 = itr.get_next(datetime)
    assert n1.hour == 0
    assert n1.month == 3
    assert n1.day == 1
    assert n1.year == 2017

    # The result with this parameters was incorrect.
    # self.assertEqual(p1.month, 12
    # AssertionError: 9 != 12
    base = datetime(2016, 3, 1, 0, 0, 0)
    itr = croniter('0 0 1 3,6,9,12 *', base)


def test_rangeGenerator():
    base = datetime(2013, 3, 4, 0, 0)
    itr = croniter('1-9/2 0 1 * *', base)
    n1 = itr.get_next(datetime)
    n2 = itr.get_next(datetime)
    n3 = itr.get_next(datetime)
    n4 = itr.get_next(datetime)
    n5 = itr.get_next(datetime)
    assert n1.minute == 1
    assert n2.minute == 3
    assert n3.minute == 5
    assert n4.minute == 7
    assert n5.minute == 9


def testGetCurrent():
    base = datetime(2012, 9, 25, 11, 24)
    itr = croniter('* * * * *', base)
    res = itr.get_current(datetime)
    assert base.year == res.year
    assert base.month == res.month
    assert base.day == res.day
    assert base.hour == res.hour
    assert base.minute == res.minute


def testTimezone():
    base = datetime(2013, 3, 4, 12, 15)
    itr = croniter('* * * * *', base)
    n1 = itr.get_next(datetime)
    assert n1.tzinfo is None

    tokyo = pytz.timezone('Asia/Tokyo')
    itr2 = croniter('* * * * *', tokyo.localize(base))
    n2 = itr2.get_next(datetime)
    assert n2.tzinfo.zone == 'Asia/Tokyo'


def testTimezoneDateutil():
    tokyo = dateutil.tz.gettz('Asia/Tokyo')
    base = datetime(2013, 3, 4, 12, 15, tzinfo=tokyo)
    itr = croniter('* * * * *', base)
    n1 = itr.get_next(datetime)
    assert n1.tzinfo.tzname(n1) == 'JST'


def testInitNoStartTime():
    itr = croniter('* * * * *')
    sleep(.01)
    itr2 = croniter('* * * * *')
    assert itr2.cur > itr.cur


def assertScheduleTimezone(callback, expected_schedule):
    for expected_date, expected_offset in expected_schedule:
        d = callback()
        assert expected_date == d.replace(tzinfo=None)
        assert expected_offset == croniter._timedelta_to_seconds(d.utcoffset())


def testTimezoneWinterTime():
    tz = pytz.timezone('Europe/Athens')

    expected_schedule = [
        (datetime(2013, 10, 27, 2, 30, 0), 10800),
        (datetime(2013, 10, 27, 3, 0, 0), 10800),
        (datetime(2013, 10, 27, 3, 30, 0), 10800),
        (datetime(2013, 10, 27, 3, 0, 0), 7200),
        (datetime(2013, 10, 27, 3, 30, 0), 7200),
        (datetime(2013, 10, 27, 4, 0, 0), 7200),
        (datetime(2013, 10, 27, 4, 30, 0), 7200),
        ]

    start = datetime(2013, 10, 27, 2, 0, 0)
    ct = croniter('*/30 * * * *', tz.localize(start))
    assertScheduleTimezone(lambda: ct.get_next(datetime), expected_schedule)


def testTimezoneSummerTime():
    tz = pytz.timezone('Europe/Athens')

    expected_schedule = [
        (datetime(2013, 3, 31, 1, 30, 0), 7200),
        (datetime(2013, 3, 31, 2, 0, 0), 7200),
        (datetime(2013, 3, 31, 2, 30, 0), 7200),
        (datetime(2013, 3, 31, 4, 0, 0), 10800),
        (datetime(2013, 3, 31, 4, 30, 0), 10800),
        ]

    start = datetime(2013, 3, 31, 1, 0, 0)
    ct = croniter('*/30 * * * *', tz.localize(start))
    assertScheduleTimezone(lambda: ct.get_next(datetime), expected_schedule)


def test_std_dst():
    """
    DST tests

    This fixes https://github.com/taichino/croniter/issues/82

    """
    tz = pytz.timezone('Europe/Warsaw')
    # -> 2017-03-26 01:59+1:00 -> 03:00+2:00
    local_date = tz.localize(datetime(2017, 3, 26))
    val = croniter('0 0 * * *', local_date).get_next(datetime)
    assert val == tz.localize(datetime(2017, 3, 27))
    #
    local_date = tz.localize(datetime(2017, 3, 26, 1))
    cr = croniter('0 * * * *', local_date)
    val = cr.get_next(datetime)
    assert val == tz.localize(datetime(2017, 3, 26, 3))
    val = cr.get_current(datetime)
    assert val == tz.localize(datetime(2017, 3, 26, 3))

    # -> 2017-10-29 02:59+2:00 -> 02:00+1:00
    local_date = tz.localize(datetime(2017, 10, 29))
    val = croniter('0 0 * * *', local_date).get_next(datetime)
    assert val == tz.localize(datetime(2017, 10, 30))
    local_date = tz.localize(datetime(2017, 10, 29, 1, 59))
    val = croniter('0 * * * *', local_date).get_next(datetime)
    assert val.replace(tzinfo=None) == tz.localize(datetime(2017, 10, 29, 2)).replace(tzinfo=None)
    local_date = tz.localize(datetime(2017, 10, 29, 2))
    val = croniter('0 * * * *', local_date).get_next(datetime)
    assert val == tz.localize(datetime(2017, 10, 29, 3))
    local_date = tz.localize(datetime(2017, 10, 29, 3))
    val = croniter('0 * * * *', local_date).get_next(datetime)
    assert val == tz.localize(datetime(2017, 10, 29, 4))
    local_date = tz.localize(datetime(2017, 10, 29, 4))
    val = croniter('0 * * * *', local_date).get_next(datetime)
    assert val == tz.localize(datetime(2017, 10, 29, 5))
    local_date = tz.localize(datetime(2017, 10, 29, 5))
    val = croniter('0 * * * *', local_date).get_next(datetime)
    assert val == tz.localize(datetime(2017, 10, 29, 6))


def test_std_dst2():
    """
    DST tests

    This fixes https://github.com/taichino/croniter/issues/87

    São Paulo, Brazil: 18/02/2018 00:00 -> 17/02/2018 23:00

    """
    tz = pytz.timezone("America/Sao_Paulo")
    local_dates = [
        # 17-22: 00 -> 18-00:00
        (tz.localize(datetime(2018, 2, 17, 21, 0, 0)),
         '2018-02-18 00:00:00-03:00'),
        # 17-23: 00 -> 18-00:00
        (tz.localize(datetime(2018, 2, 17, 22, 0, 0)),
         '2018-02-18 00:00:00-03:00'),
        # 17-23: 00 -> 18-00:00
        (tz.localize(datetime(2018, 2, 17, 23, 0, 0)),
         '2018-02-18 00:00:00-03:00'),
        # 18-00: 00 -> 19-00:00
        (tz.localize(datetime(2018, 2, 18, 0, 0, 0)),
         '2018-02-19 00:00:00-03:00'),
        # 17-22: 00 -> 18-00:00
        (tz.localize(datetime(2018, 2, 17, 21, 5, 0)),
         '2018-02-18 00:00:00-03:00'),
        # 17-23: 00 -> 18-00:00
        (tz.localize(datetime(2018, 2, 17, 22, 5, 0)),
         '2018-02-18 00:00:00-03:00'),
        # 17-23: 00 -> 18-00:00
        (tz.localize(datetime(2018, 2, 17, 23, 5, 0)),
         '2018-02-18 00:00:00-03:00'),
        # 18-00: 00 -> 19-00:00
        (tz.localize(datetime(2018, 2, 18, 0, 5, 0)),
         '2018-02-19 00:00:00-03:00'),
    ]
    ret1 = [croniter("0 0 * * *", d[0]).get_next(datetime)
            for d in local_dates]
    sret1 = ['{0}'.format(d) for d in ret1]
    lret1 = ['{0}'.format(d[1]) for d in local_dates]
    assert sret1 == lret1


def test_error_alpha_cron():
    assert pytest.raises(CroniterNotAlphaError, croniter.expand,
                      '* * * janu-jun *')


def test_error_bad_cron():
    assert pytest.raises(CroniterBadCronError, croniter.expand,
                      '* * * *')
    assert pytest.raises(CroniterBadCronError, croniter.expand,
                      '* * * * * * *')


def test_is_valid():
    assert croniter.is_valid('0 * * * *')
    assert not croniter.is_valid('0 * *')
    assert not croniter.is_valid('* * * janu-jun *')


def test_next_when_now_satisfies_cron():
    ts_a = datetime(2018, 5, 21, 0, 3, 0)
    ts_b = datetime(2018, 5, 21, 0, 4, 20)
    test_cron = '4 * * * *'

    next_a = croniter(test_cron, start_time=ts_a).get_next()
    next_b = croniter(test_cron, start_time=ts_b).get_next()

    assert next_b > next_a


def test_invalid_zerorepeat():
    assert not croniter.is_valid('*/0 * * * *')


def test_weekday_range():
    ret = []
    # jan 14 is monday
    dt = datetime(2019, 1, 14, 0, 0, 0, 0)
    for i in range(10):
        c = croniter("0 0 * * 2-4 *", start_time=dt)
        dt = datetime.fromtimestamp(
            c.get_next(), dateutil.tz.tzutc()
        ).replace(tzinfo=None)
        ret.append(dt)
        dt += timedelta(days=1)
    sret = ["{0}".format(r) for r in ret]
    assert sret == [
        '2019-02-01 00:00:00',
        '2019-02-02 01:00:00',
        '2019-02-03 02:00:00',
        '2019-02-04 03:00:00',
        '2019-02-05 04:00:00',
        '2019-02-06 05:00:00',
        '2019-02-07 06:00:00',
        '2019-02-08 07:00:00',
        '2019-02-09 08:00:00',
        '2019-02-10 09:00:00'
    ]
    ret = []
    dt = datetime(2019, 1, 14, 0, 0, 0, 0)
    for i in range(10):
        c = croniter("0 0 * * 1-7 *", start_time=dt)
        dt = datetime.fromtimestamp(
            c.get_next(), dateutil.tz.tzutc()
        ).replace(tzinfo=None)
        ret.append(dt)
        dt += timedelta(days=1)
    sret = ["{0}".format(r) for r in ret]
    assert sret == [
        '2019-01-14 01:00:00',
        '2019-01-15 02:00:00',
        '2019-01-16 03:00:00',
        '2019-01-17 04:00:00',
        '2019-01-18 05:00:00',
        '2019-01-19 06:00:00',
        '2019-01-20 07:00:00',
        '2019-01-21 08:00:00',
        '2019-01-22 09:00:00',
        '2019-01-23 10:00:00'
    ]


def test_issue_monsun_117():
    ret = []
    dt = datetime(2019, 1, 14, 0, 0, 0, 0)
    for i in range(10):
        c = croniter("0 0 0 * * Mon-Sun", start_time=dt)
        dt = datetime.fromtimestamp(
            c.get_next(), tz=dateutil.tz.tzutc()
        ).replace(tzinfo=None)
        ret.append(dt)
        dt += timedelta(days=1)
    sret = ["{0}".format(r) for r in ret]
    assert sret == [
        '2019-01-15 00:00:00',
        '2019-01-17 00:00:00',
        '2019-01-19 00:00:00',
        '2019-01-21 00:00:00',
        '2019-01-23 00:00:00',
        '2019-01-25 00:00:00',
        '2019-01-27 00:00:00',
        '2019-01-29 00:00:00',
        '2019-01-31 00:00:00',
        '2019-02-02 00:00:00'
    ]


def test_mixdow():
    base = datetime(2018, 10, 1, 0, 0)
    itr = croniter('1 1 7,14,21,L * *', base)
    assert isinstance(itr.get_next(), float)


def test_dst_iter():
    tz = pytz.timezone('Asia/Hebron')
    now = datetime(2022, 3, 26, 0, 0, 0, tzinfo=tz)
    it = croniter('0 0 * * *', now)
    ret = [
        it.get_next(datetime).isoformat(),
        it.get_next(datetime).isoformat(),
        it.get_next(datetime).isoformat(),
    ]
    assert ret == [
        '2022-03-26T00:00:00+02:00',
        '2022-03-27T01:00:00+03:00',
        '2022-03-28T00:00:00+03:00'
    ]


def test_nth_wday_simple():
    def f(y, m, w):
     return croniter._get_nth_weekday_of_month(y, m, w)

    sun, mon, tue, wed, thu, fri, sat = range(7)

    assert f(2000, 1, mon) == (3, 10, 17, 24, 31)
    assert f(2000, 2, tue) == (1, 8, 15, 22, 29) # Leap year
    assert f(2000, 3, wed) == (1, 8, 15, 22, 29)
    assert f(2000, 4, thu) == (6, 13, 20, 27)
    assert f(2000, 2, fri) == (4, 11, 18, 25)
    assert f(2000, 2, sat) == (5, 12, 19, 26)


def test_nth_as_last_wday_simple():
    def f(y, m, w):
        return croniter._get_nth_weekday_of_month(y, m, w)[-1]

    sun, mon, tue, wed, thu, fri, sat = range(7)
    assert f(2000, 2, tue) == 29
    assert f(2000, 2, sun) == 27
    assert f(2000, 2, mon) == 28
    assert f(2000, 2, wed) == 23
    assert f(2000, 2, thu) == 24
    assert f(2000, 2, fri) == 25
    assert f(2000, 2, sat) == 26


def test_wdom_core_leap_year():
    def f(y, m, w):
        return croniter._get_nth_weekday_of_month(y, m, w)[-1]

    sun, mon, tue, wed, thu, fri, sat = range(7)
    assert f(2000, 2, tue) == 29
    assert f(2000, 2, sun) == 27
    assert f(2000, 2, mon) == 28
    assert f(2000, 2, wed) == 23
    assert f(2000, 2, thu) == 24
    assert f(2000, 2, fri) == 25
    assert f(2000, 2, sat) == 26


def test_lwom_friday():
    it = croniter('0 0 * * L5', datetime(1987, 1, 15), ret_type=datetime)
    items = [next(it) for i in range(12)]
    assert items == [
        datetime(1987, 1, 30),
        datetime(1987, 2, 27),
        datetime(1987, 3, 27),
        datetime(1987, 4, 24),
        datetime(1987, 5, 29),
        datetime(1987, 6, 26),
        datetime(1987, 7, 31),
        datetime(1987, 8, 28),
        datetime(1987, 9, 25),
        datetime(1987, 10, 30),
        datetime(1987, 11, 27),
        datetime(1987, 12, 25),
    ]


def test_lwom_friday_2hours():
    # This works with +/- 'days=1' in proc_day_of_week_last() and I don't know WHY?!?
    it = croniter("0 1,5 * * L5", datetime(1987, 1, 15), ret_type=datetime)
    items = [next(it) for i in range(12)]
    assert items == [
        datetime(1987, 1, 30, 1),
        datetime(1987, 1, 30, 5),
        datetime(1987, 2, 27, 1),
        datetime(1987, 2, 27, 5),
        datetime(1987, 3, 27, 1),
        datetime(1987, 3, 27, 5),
        datetime(1987, 4, 24, 1),
        datetime(1987, 4, 24, 5),
        datetime(1987, 5, 29, 1),
        datetime(1987, 5, 29, 5),
        datetime(1987, 6, 26, 1),
        datetime(1987, 6, 26, 5),
    ]


def test_lwom_friday_2xh_2xm():
    it = croniter("0,30 1,5 * * L5", datetime(1987, 1, 15), ret_type=datetime)
    items = [next(it) for i in range(12)]
    assert items == [
        datetime(1987, 1, 30, 1, 0),
        datetime(1987, 1, 30, 1, 30),
        datetime(1987, 1, 30, 5, 0),
        datetime(1987, 1, 30, 5, 30),
        datetime(1987, 2, 27, 1, 0),
        datetime(1987, 2, 27, 1, 30),
        datetime(1987, 2, 27, 5, 0),
        datetime(1987, 2, 27, 5, 30),
        datetime(1987, 3, 27, 1, 0),
        datetime(1987, 3, 27, 1, 30),
        datetime(1987, 3, 27, 5, 0),
        datetime(1987, 3, 27, 5, 30),
    ]


def test_lwom_tue_thu():
    it = croniter("0 0 * * L2,L4", datetime(2016, 6, 1), ret_type=datetime)
    items = [next(it) for i in range(10)]
    assert items == [
        datetime(2016, 6, 28),
        datetime(2016, 6, 30),
        datetime(2016, 7, 26),
        datetime(2016, 7, 28),
        datetime(2016, 8, 25),  # last tuesday comes before the last thursday
        datetime(2016, 8, 30),
        datetime(2016, 9, 27),
        datetime(2016, 9, 29),
        datetime(2016, 10, 25),
        datetime(2016, 10, 27),
    ]


def test_hash_mixup_all_fri_3rd_sat():
    # It appears that it's not possible to MIX a literal dow with a `dow#n` format
    cron_a = "0 0 * * 6#3"
    cron_b = "0 0 * * 5"
    cron_c = "0 0 * * 5,6#3"
    start = datetime(2021, 3, 1)
    expect_a = [ datetime(2021, 3, 20) ]
    expect_b = [
        datetime(2021, 3, 5),
        datetime(2021, 3, 12),
        datetime(2021, 3, 19),
        datetime(2021, 3, 26),
    ]
    def getn(expr, n):
        it = croniter(expr, start, ret_type=datetime)
        return [next(it) for i in range(n)]
    assert getn(cron_a, 1) == expect_a
    assert getn(cron_b, 4) == expect_b
    with pytest.raises(CroniterUnsupportedSyntaxError):
        getn(cron_c, 5)


def test_lwom_mixup_all_fri_last_sat():
    # Based on the failure of test_hash_mixup_all_fri_3rd_sat, we should expect this to fail too as this implementation simply extends nth_weekday_of_month
    cron_a = "0 0 * * L6"
    cron_b = "0 0 * * 5"
    cron_c = "0 0 * * 5,L6"
    start = datetime(2021, 3, 1)
    expect_a = [ datetime(2021, 3, 27) ]
    expect_b = [
        datetime(2021, 3, 5),
        datetime(2021, 3, 12),
        datetime(2021, 3, 19),
        datetime(2021, 3, 26),
    ]
    def getn(expr, n):
        it = croniter(expr, start, ret_type=datetime)
        return [next(it) for i in range(n)]
    assert getn(cron_a, 1) == expect_a
    assert getn(cron_b, 4) == expect_b
    with pytest.raises(CroniterUnsupportedSyntaxError):
        getn(cron_c, 5)


def test_lwom_mixup_firstlast_sat():
    # First saturday, last saturday
    start = datetime(2021, 3, 1)
    cron_a = "0 0 * * 6#1"
    cron_b = "0 0 * * L6"
    cron_c = "0 0 * * L6,6#1"
    expect_a = [
        datetime(2021, 3, 6),
        datetime(2021, 4, 3),
        datetime(2021, 5, 1),
    ]
    expect_b = [
        datetime(2021, 3, 27),
        datetime(2021, 4, 24),
        datetime(2021, 5, 29),
    ]
    expect_c = sorted(expect_a + expect_b)
    def getn(expr, n):
        it = croniter(expr, start, ret_type=datetime)
        return [next(it) for i in range(n)]
    assert getn(cron_a, 3) == expect_a
    assert getn(cron_b, 3) == expect_b
    assert getn(cron_c, 6) == expect_c


def test_lwom_mixup_4th_and_last():
    # 4th and last monday
    start = datetime(2021, 11, 1)
    cron_a = "0 0 * * 1#4"
    cron_b = "0 0 * * L1"
    cron_c = "0 0 * * 1#4,L1"
    expect_a = [
        datetime(2021, 11, 22),
        datetime(2021, 12, 27),
        datetime(2022, 1, 24)
    ]
    expect_b = [
        datetime(2021, 11, 29),
        datetime(2021, 12, 27),
        datetime(2022, 1, 31),
    ]
    expect_c = sorted(set(expect_a) | set(expect_b))

    def getn(expr, n):
        it = croniter(expr, start, ret_type=datetime)
        return [next(it) for i in range(n)]

    assert getn(cron_a, 3) == expect_a
    assert getn(cron_b, 3) == expect_b
    assert getn(cron_c, 5) == expect_c


def test_nth_out_of_range():
    with pytest.raises(CroniterBadCronError):
        croniter("0 0 * * 1#7")
    with pytest.raises(CroniterBadCronError):
        croniter("0 0 * * 1#0")


def test_last_out_of_range():
    with pytest.raises(CroniterBadCronError):
        croniter("0 0 * * L-1")
    with pytest.raises(CroniterBadCronError):
        croniter("0 0 * * L8")


maxDiff = None
def test_issue_142_dow():
    ret = []
    for i in range(1, 31):
        ret.append((i,
            croniter('35 * 1-l/8 * *', datetime(2020, 1, i),
                     ret_type=datetime).get_next())
        )
        i += 1
    assert ret == [
        (1, datetime(2020, 1, 1, 0, 35)),
        (2, datetime(2020, 1, 9, 0, 35)),
        (3, datetime(2020, 1, 9, 0, 35)),
        (4, datetime(2020, 1, 9, 0, 35)),
        (5, datetime(2020, 1, 9, 0, 35)),
        (6, datetime(2020, 1, 9, 0, 35)),
        (7, datetime(2020, 1, 9, 0, 35)),
        (8, datetime(2020, 1, 9, 0, 35)),
        (9, datetime(2020, 1, 9, 0, 35)),
        (10, datetime(2020, 1, 17, 0, 35)),
        (11, datetime(2020, 1, 17, 0, 35)),
        (12, datetime(2020, 1, 17, 0, 35)),
        (13, datetime(2020, 1, 17, 0, 35)),
        (14, datetime(2020, 1, 17, 0, 35)),
        (15, datetime(2020, 1, 17, 0, 35)),
        (16, datetime(2020, 1, 17, 0, 35)),
        (17, datetime(2020, 1, 17, 0, 35)),
        (18, datetime(2020, 1, 25, 0, 35)),
        (19, datetime(2020, 1, 25, 0, 35)),
        (20, datetime(2020, 1, 25, 0, 35)),
        (21, datetime(2020, 1, 25, 0, 35)),
        (22, datetime(2020, 1, 25, 0, 35)),
        (23, datetime(2020, 1, 25, 0, 35)),
        (24, datetime(2020, 1, 25, 0, 35)),
        (25, datetime(2020, 1, 25, 0, 35)),
        (26, datetime(2020, 2, 1, 0, 35)),
        (27, datetime(2020, 2, 1, 0, 35)),
        (28, datetime(2020, 2, 1, 0, 35)),
        (29, datetime(2020, 2, 1, 0, 35)),
        (30, datetime(2020, 2, 1, 0, 35))
    ]


def test_issue145_getnext():
    # Example of quarterly event cron schedule
    start = datetime(2020, 9, 24)
    cron = '0 13 8 1,4,7,10 wed'
    with pytest.raises(CroniterBadDateError):
        it = croniter(cron, start, day_or=False, max_years_between_matches=1)
        it.get_next()
    # New functionality (0.3.35) allowing croniter to find spare
    # matches of cron patterns across multiple years
    it = croniter(cron, start, day_or=False, max_years_between_matches=5)
    assert it.get_next(datetime) == datetime(2025, 1, 8, 13)


def test_explicit_year_forward():
    start = datetime(2020, 9, 24)
    cron = '0 13 8 1,4,7,10 wed'

    # Expect exception because no explicit range was provided.
    # Therefore, the caller should be made aware that an implicit
    # limit was hit.
    ccron = croniter(cron, start, day_or=False)
    ccron._max_years_between_matches = 1
    iterable = ccron.all_next()
    with pytest.raises(CroniterBadDateError):
        next(iterable)

    iterable = croniter(
        cron, start, day_or=False, max_years_between_matches=5
    ).all_next(datetime)
    n = next(iterable)
    assert n == datetime(2025, 1, 8, 13)

    # If the explicitly given lookahead isn't enough to reach the next
    # date, that's fine.  The caller specified the maximum gap, so no
    # just stop iteration
    iterable = croniter(
        cron, start, day_or=False, max_years_between_matches=2
    ).all_next(datetime)
    with pytest.raises(StopIteration):
        next(iterable)


def test_overflow():
    assert pytest.raises(
        CroniterBadCronError,
        croniter , '0-10000000 * * * *',
        datetime.now()
    )


def test_issue156():
    dt = croniter(
        '* * * * *,0', datetime(2019, 1, 14, 11, 0, 59, 999999)
    ).get_next()
    assert 1547463660.0 == dt
    assert pytest.raises(CroniterBadCronError, croniter, "* * * * *,b")
    dt = croniter("0 0 * * *,sat#3", datetime(2019, 1, 14, 11, 0, 59, 999999)).get_next()
    assert 1547856000.0 == dt


def test_confirm_sort():
    m, h, d, mon, dow, s = range(6)
    assert croniter('0 8,22,10,23 1 1 0').expanded[h] == [8, 10, 22, 23]
    assert croniter('0 0 25-L 1 0').expanded[d] == [25, 26, 27, 28, 29, 30, 31]
    assert croniter("1 1 7,14,21,L * *").expanded[d] == [7, 14, 21, "l"]
    assert croniter("0 0 * * *,sat#3").expanded[dow] == ["*", 6]


def test_issue_k6():
    assert pytest.raises(CroniterBadCronError, croniter, '0 0 0 0 0')
    assert pytest.raises(CroniterBadCronError, croniter, '0 0 0 1 0')


def test_issue_k11():
    now = pytz.timezone('America/New_York').localize(datetime(2019, 1, 14, 11, 0, 59))
    nextnow = croniter('* * * * * ').next(datetime, start_time=now)
    nextnow2 = croniter('* * * * * ', now).next(datetime)
    for nt in nextnow, nextnow2:
        assert nt.tzinfo.zone == 'America/New_York'
        assert int(croniter._datetime_to_timestamp(nt)) == 1547481660


def test_issue_k12():
    tz = pytz.timezone('Europe/Athens')
    base = datetime(2010, 1, 23, 12, 18, tzinfo=tz)
    itr = croniter('* * * * *')
    itr.set_current(start_time=base)
    n1 = itr.get_next()   # 19

    assert n1 == datetime_to_timestamp(base) + 60


def test_issue_k34():
    # invalid cron, but should throw appropriate exception
    assert pytest.raises(CroniterBadCronError, croniter, "4 0 L/2 2 0")


def test_issue_k33():
    y = 2018
    # At 11:30 PM, between day 1 and 7 of the month, Monday through Friday, only in January
    ret = []
    for i in range(10):
        cron = croniter("30 23 1-7 JAN MON-FRI#1", datetime(y+i, 1, 1), ret_type=datetime)
        for j in range(7):
            d = cron.get_next()
            if d.year == y + i:
                ret.append(d)
    rets = [datetime(2018, 1, 1, 23, 30),
            datetime(2018, 1, 2, 23, 30),
            datetime(2018, 1, 3, 23, 30),
            datetime(2018, 1, 4, 23, 30),
            datetime(2018, 1, 5, 23, 30),
            datetime(2019, 1, 1, 23, 30),
            datetime(2019, 1, 2, 23, 30),
            datetime(2019, 1, 3, 23, 30),
            datetime(2019, 1, 4, 23, 30),
            datetime(2019, 1, 7, 23, 30),
            datetime(2020, 1, 1, 23, 30),
            datetime(2020, 1, 2, 23, 30),
            datetime(2020, 1, 3, 23, 30),
            datetime(2020, 1, 6, 23, 30),
            datetime(2020, 1, 7, 23, 30),
            datetime(2021, 1, 1, 23, 30),
            datetime(2021, 1, 4, 23, 30),
            datetime(2021, 1, 5, 23, 30),
            datetime(2021, 1, 6, 23, 30),
            datetime(2021, 1, 7, 23, 30),
            datetime(2022, 1, 3, 23, 30),
            datetime(2022, 1, 4, 23, 30),
            datetime(2022, 1, 5, 23, 30),
            datetime(2022, 1, 6, 23, 30),
            datetime(2022, 1, 7, 23, 30),
            datetime(2023, 1, 2, 23, 30),
            datetime(2023, 1, 3, 23, 30),
            datetime(2023, 1, 4, 23, 30),
            datetime(2023, 1, 5, 23, 30),
            datetime(2023, 1, 6, 23, 30),
            datetime(2024, 1, 1, 23, 30),
            datetime(2024, 1, 2, 23, 30),
            datetime(2024, 1, 3, 23, 30),
            datetime(2024, 1, 4, 23, 30),
            datetime(2024, 1, 5, 23, 30),
            datetime(2025, 1, 1, 23, 30),
            datetime(2025, 1, 2, 23, 30),
            datetime(2025, 1, 3, 23, 30),
            datetime(2025, 1, 6, 23, 30),
            datetime(2025, 1, 7, 23, 30),
            datetime(2026, 1, 1, 23, 30),
            datetime(2026, 1, 2, 23, 30),
            datetime(2026, 1, 5, 23, 30),
            datetime(2026, 1, 6, 23, 30),
            datetime(2026, 1, 7, 23, 30),
            datetime(2027, 1, 1, 23, 30),
            datetime(2027, 1, 4, 23, 30),
            datetime(2027, 1, 5, 23, 30),
            datetime(2027, 1, 6, 23, 30),
            datetime(2027, 1, 7, 23, 30)]
    assert ret == rets
    croniter.expand("30 6 1-7 MAY MON#1")


# range

class mydatetime(datetime):
    """."""


def test_1day_step():
    start = datetime(2016, 12, 2)
    stop = datetime(2016, 12, 10)
    fwd = list(
        croniter_range(start, stop, '0 0 * * *')
    )
    assert len(fwd) == 9
    assert fwd[0] == start
    assert fwd[-1] == stop


def test_1day_step_no_ends():
    # Test without ends (exclusive)
    start = datetime(2016, 12, 2)
    stop = datetime(2016, 12, 10)
    fwd = list(
        croniter_range(start, stop, '0 0 * * *', exclude_ends=True)
    )
    assert len(fwd) == 7
    assert fwd[0] != start
    assert fwd[-1] != stop


def test_1month_step():
    start = datetime(1982, 1, 1)
    stop = datetime(1983, 12, 31)
    res = list(
        croniter_range(start, stop, '0 0 1 * *')
    )
    assert len(res) == 24
    assert res[0] == start
    assert res[5].day == 1
    assert res[-1] == datetime(1983, 12, 1)


def test_1minute_step_float():
    start = datetime(2000, 1, 1, 0, 0)
    stop =  datetime(2000, 1, 1, 0, 1)
    res = list(
        croniter_range(start, stop, '* * * * *', ret_type=float)
    )
    assert len(res) == 2
    assert res[0] == 946684800.0
    assert res[-1] - res[0] == 60


def test_auto_ret_type():
    data = [
        (datetime(2019, 1, 1), datetime(2020, 1, 1), datetime),
        (1552252218.0, 1591823311.0, float),
    ]
    for start, stop, rtype in data:
        ret = list(
            croniter_range(start, stop, "0 0 * * *")
        )
        assert isinstance(ret[0], rtype)


def test_input_type_exceptions():
    dt_start1 = datetime(2019, 1, 1)
    dt_stop1 = datetime(2020, 1, 1)
    f_start1 = 1552252218.0
    f_stop1 = 1591823311.0
    # Mix start/stop types
    with pytest.raises(TypeError):
        list(
            croniter_range(dt_start1, f_stop1, "0 * * * *"), ret_type=datetime
        )
    with pytest.raises(TypeError):
        list(
            croniter_range(f_start1, dt_stop1, "0 * * * *")
        )


def test_timezone_dst():
    """ Test across DST transition, which technically is a timzone change. """
    tz = pytz.timezone("US/Eastern")
    start = tz.localize(datetime(2020, 10, 30))
    stop =  tz.localize(datetime(2020, 11, 10))
    res = list(
        croniter_range(start, stop, '0 0 * * *')
    )
    assert res[0].tzinfo != res[-1].tzinfo
    assert len(res) == 12


def test_extra_hour_day_prio():
    def datetime_tz(*args, **kw):
        """ Defined this in another branch.  single-use-version """
        tzinfo = kw.pop("tzinfo")
        return tzinfo.localize(datetime(*args))

    tz = pytz.timezone("US/Eastern")
    cron = "0 3 * * *"
    start = datetime_tz(2020, 3, 7, tzinfo=tz)
    end = datetime_tz(2020, 3, 11, tzinfo=tz)
    ret = [
        i.isoformat()
        for i in croniter_range(start, end, cron)
    ]
    assert ret == [
        '2020-03-07T03:00:00-05:00',
        '2020-03-08T03:00:00-04:00',
        '2020-03-09T03:00:00-04:00',
        '2020-03-10T03:00:00-04:00'
    ]


def test_issue145_range():
    cron = "0 13 8 1,4,7,10 wed"
    matches = list(
        croniter_range(datetime(2020, 1, 1), datetime(2020, 12, 31), cron, day_or=False)
    )
    assert len(matches) == 3
    assert matches[0] == datetime(2020, 1, 8, 13)
    assert matches[1] == datetime(2020, 4, 8, 13)
    assert matches[2] == datetime(2020, 7, 8, 13)

    # No matches within this range; therefore expect empty list
    matches = list(
        croniter_range(datetime(2020, 9, 30), datetime(2020, 10, 30), cron, day_or=False)
    )
    assert len(matches) == 0


def test_croniter_range_derived_class():
    # trivial example extending croniter

    class croniter_nosec(croniter):
        """ Like croniter, but it forbids second-level cron expressions. """
        @classmethod
        def expand(cls, expr_format, *args, **kwargs):
            if len(expr_format.split()) == 6:
                raise CroniterBadCronError("Expected 'min hour day mon dow'")
            return croniter.expand(expr_format, *args, **kwargs)

    cron = '0 13 8 1,4,7,10 wed'
    matches = list(
        croniter_range(
            datetime(2020, 1, 1),
            datetime(2020, 12, 31),
            cron,
            day_or=False,
            _croniter=croniter_nosec
        )
    )
    assert len(matches) == 3

    cron = "0 1 8 1,15,L wed 15,45"
    with pytest.raises(CroniterBadCronError):
        # Should fail using the custom class that forbids the seconds
        # expression
        croniter_nosec(cron)

    with pytest.raises(CroniterBadCronError):
        # Should similarly fail because the custom class rejects
        # seconds expr
        i = croniter_range(
            datetime(2020, 1, 1), datetime(2020, 12, 31), cron, _croniter=croniter_nosec
        )
        next(i)


def test_dt_types():
    start = mydatetime(2020, 9, 24)
    stop = datetime(2020, 9, 28)
    list(
        croniter_range(start, stop, '0 0 * * *')
    )
