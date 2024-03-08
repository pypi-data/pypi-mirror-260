import traceback as _traceback
import math
import re
import sys
from time import time
import datetime
from dateutil.relativedelta import relativedelta
from dateutil.tz import tzutc
import calendar


M_ALPHAS = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
            'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}
DOW_ALPHAS = {'sun': 0, 'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6}
ALPHAS = dict(**M_ALPHAS, **DOW_ALPHAS)

step_search_re = re.compile(r'^([^-]+)-([^-/]+)(/(\d+))?$')
only_int_re = re.compile(r'^\d+$')

WEEKDAYS = '|'.join(DOW_ALPHAS.keys())
MONTHS = '|'.join(M_ALPHAS.keys())
star_or_int_re = re.compile(r'^(\d+|\*)$')
special_dow_re = re.compile(
    (r'^(?P<pre>((?P<he>(({WEEKDAYS})(-({WEEKDAYS}))?)').format(WEEKDAYS=WEEKDAYS) +
    (r'|(({MONTHS})(-({MONTHS}))?)|\w+)#)|l)(?P<last>\d+)$').format(MONTHS=MONTHS)
)
re_star = re.compile('[*]')
VALID_LEN_EXPRESSION = (5, 6)


def timedelta_to_seconds(td):
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) \
        / 10**6


def datetime_to_timestamp(d):
    if d.tzinfo is not None:
        d = d.replace(tzinfo=None) - d.utcoffset()

    return timedelta_to_seconds(d - datetime.datetime(1970, 1, 1))


class CroniterError(ValueError):
    """ General top-level Croniter base exception """
    pass


class CroniterBadTypeRangeError(TypeError):
    """."""


class CroniterBadCronError(CroniterError):
    """ Syntax, unknown value, or range error within a cron expression """
    pass


class CroniterUnsupportedSyntaxError(CroniterBadCronError):
    """ Valid cron syntax, but likely to produce inaccurate results """
    # Extending CroniterBadCronError, which may be contridatory, but this allows
    # catching both errors with a single exception.  From a user perspective
    # these will likely be handled the same way.
    pass


class CroniterBadDateError(CroniterError):
    """ Unable to find next timestamp match """
    pass


class CroniterNotAlphaError(CroniterBadCronError):
    """ Cron syntax contains an invalid day or month abbreviation """
    pass


class croniter(object):
    MONTHS_IN_YEAR = 12
    RANGES = {
        'sec': (0, 59),
        'min': (0, 59),
        'hour': (0, 23),
        'day': (1, 31),
        'month': (1, 12),
        'dow': (0, 7),
    }
    DAYS = (
        31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31
    )

    ALPHACONV = {
        'sec': {},
        'min': {},
        'hour': {},
        'day': {'l': 'l'},
        'month': M_ALPHAS,
        'dow': DOW_ALPHAS
    }

    LOWMAP = {
        'sec': {},
        'min': {},
        'hour': {},
        'day': {0: 1},
        'month': {0: 1},
        'dow': {7: 0},
    }

    LEN_MEANS_ALL = {
        'sec': 60,
        'min': 60,
        'hour': 24,
        'day': 31,
        'month': 12,
        'dow': 7
    }

    bad_length = 'Exactly 5 or 6 columns has to be specified for iterator ' \
                 'expression.'

    def __init__(self, expr_format, start_time=None, ret_type=float,
                 day_or=True, max_years_between_matches=None,
                 implement_cron_bug=False):
        self._ret_type = ret_type
        self._day_or = day_or
        self._implement_cron_bug = implement_cron_bug

        self._max_years_btw_matches_explicitly_set = (
            max_years_between_matches is not None)
        if not self._max_years_btw_matches_explicitly_set:
            max_years_between_matches = 50
        self._max_years_between_matches = max(int(max_years_between_matches), 1)

        if start_time is None:
            start_time = time()

        self.tzinfo = None

        self.start_time = None
        self.dst_start_time = None
        self.cur = None
        self.set_current(start_time, force=False)

        self.expanded, self.expressions, self.nth_weekday_of_month = self.expand(expr_format)

    @classmethod
    def _alphaconv(cls, index, key, expressions):
        try:
            return cls.ALPHACONV[index][key]
        except KeyError:
            raise CroniterNotAlphaError(
                "[{0}] is not acceptable".format(" ".join(expressions)))

    def get_next(self, ret_type=None, start_time=None):
        self.set_current(start_time, force=True)
        return self._get_next(ret_type or self._ret_type)

    def get_current(self, ret_type=None):
        ret_type = ret_type or self._ret_type
        if issubclass(ret_type, datetime.datetime):
            return self._timestamp_to_datetime(self.cur)
        return self.cur

    def set_current(self, start_time, force=True):
        if (force or (self.cur is None)) and start_time is not None:
            if isinstance(start_time, datetime.datetime):
                self.tzinfo = start_time.tzinfo
                start_time = self._datetime_to_timestamp(start_time)

            self.start_time = start_time
            self.dst_start_time = start_time
            self.cur = start_time
        return self.cur

    @classmethod
    def _datetime_to_timestamp(cls, d):
        """
        Converts a `datetime` object `d` into a UNIX timestamp.
        """
        return datetime_to_timestamp(d)

    def _timestamp_to_datetime(self, timestamp):
        """
        Converts a UNIX timestamp `timestamp` into a `datetime` object.
        """
        result = datetime.datetime.fromtimestamp(timestamp, tz=tzutc()).replace(tzinfo=None)
        if self.tzinfo:
            result = result.replace(tzinfo=tzutc()).astimezone(self.tzinfo)

        return result

    @classmethod
    def _timedelta_to_seconds(cls, td):
        """
        Converts a 'datetime.timedelta' object `td` into seconds contained in
        the duration.
        Note: We cannot use `timedelta.total_seconds()` because this is not
        supported by Python 2.6.
        """
        return timedelta_to_seconds(td)

    def _get_next(self, ret_type=None, start_time=None):
        self.set_current(start_time, force=True)
        expanded = self.expanded[:]
        seconds = len(expanded) == 6
        nth_weekday_of_month = self.nth_weekday_of_month.copy()

        ret_type = ret_type or self._ret_type

        if not issubclass(ret_type, (float, datetime.datetime)):
            raise TypeError("Invalid ret_type, only 'float' or 'datetime' "
                            "is acceptable.")

        # exception to support day of month and day of week as defined in cron
        dom_dow_exception_processed = False
        if (expanded[2 + seconds][0] != '*' and expanded[4 + seconds][0] != '*') and self._day_or:
            # If requested, handle a bug in vixie cron/ISC cron where day_of_month and day_of_week form
            # an intersection (AND) instead of a union (OR) if either field is an asterisk or starts with an asterisk
            # (https://crontab.guru/cron-bug.html)
            if self._implement_cron_bug and (re_star.match(self.expressions[2]) or re_star.match(self.expressions[4 + seconds])):
                # To produce a schedule identical to the cron bug, we'll bypass the code that
                # makes a union of DOM and DOW, and instead skip to the code that does an intersect instead
                pass
            else:
                bak = expanded[4 + seconds]
                expanded[4 + seconds] = ['*']
                t1 = self._calc(self.cur, expanded, nth_weekday_of_month)
                expanded[4 + seconds] = bak
                expanded[2 + seconds] = ['*']

                t2 = self._calc(self.cur, expanded, nth_weekday_of_month)
                result = t1 if t1 < t2 else t2
                dom_dow_exception_processed = True

        if not dom_dow_exception_processed:
            result = self._calc(self.cur, expanded,
                                nth_weekday_of_month)

        # DST Handling for cron job spanning across days
        dtstarttime = self._timestamp_to_datetime(self.dst_start_time)
        dtstarttime_utcoffset = (
            dtstarttime.utcoffset() or datetime.timedelta(0))
        dtresult = self._timestamp_to_datetime(result)
        lag = lag_hours = 0
        # do we trigger DST on next crontab (handle backward changes)
        dtresult_utcoffset = dtstarttime_utcoffset
        if dtresult and self.tzinfo:
            dtresult_utcoffset = dtresult.utcoffset()
            lag_hours = (
                self._timedelta_to_seconds(dtresult - dtstarttime) / (60 * 60)
            )
            lag = self._timedelta_to_seconds(
                dtresult_utcoffset - dtstarttime_utcoffset
            )
        hours_before_midnight = 24 - dtstarttime.hour
        if dtresult_utcoffset != dtstarttime_utcoffset:
            if (
                (lag > 0 and abs(lag_hours) >= hours_before_midnight)
                or (lag < 0 and
                    ((3600 * abs(lag_hours) + abs(lag)) >= hours_before_midnight * 3600))
            ):
                dtresult_adjusted = dtresult - datetime.timedelta(seconds=lag)
                result_adjusted = self._datetime_to_timestamp(dtresult_adjusted)
                # Do the actual adjust only if the result time actually exists
                if self._timestamp_to_datetime(result_adjusted).tzinfo == dtresult_adjusted.tzinfo:
                    dtresult = dtresult_adjusted
                    result = result_adjusted
                self.dst_start_time = result
        self.cur = result
        if issubclass(ret_type, datetime.datetime):
            result = dtresult
        return result

    # iterator protocol, to enable direct use of croniter
    # objects in a loop, like "for dt in croniter('5 0 * * *'): ..."
    # or for combining multiple croniters into single
    # dates feed using 'itertools' module
    def all_next(self, ret_type=None):
        '''Generator of all consecutive dates. Can be used instead of
        implicit call to __iter__, whenever non-default
        'ret_type' has to be specified.
        '''
        # In a Python 3.7+ world:  contextlib.suppress and contextlib.nullcontext could be used instead
        try:
            while True:
                yield self._get_next(ret_type or self._ret_type)
        except CroniterBadDateError:
            if self._max_years_btw_matches_explicitly_set:
                return
            else:
                raise

    def iter(self, *args, **kwargs):
        return self.all_next

    def __iter__(self):
        return self
    __next__ = next = _get_next

    def _calc(self, now, expanded, nth_weekday_of_month):
        now = math.floor(now)
        nearest_diff_method = self._get_next_nearest_diff
        sign = 1
        offset = (len(expanded) == 6) and 1 or 60

        dst = now = self._timestamp_to_datetime(now + sign * offset)

        month, year = dst.month, dst.year
        current_year = now.year
        DAYS = self.DAYS

        seconds = len(expanded) == 6

        def proc_month(d):
            rule = expanded[3 + seconds]
            if '*' not in rule:
                diff_month = nearest_diff_method(
                    d.month, rule, self.MONTHS_IN_YEAR)
                days = DAYS[month - 1]
                if month == 2 and self.is_leap(year) is True:
                    days += 1

                reset_day = 1

                if diff_month is not None and diff_month != 0:
                    d += relativedelta(months=diff_month, day=reset_day,
                                       hour=0, minute=0, second=0)
                    return True, d

            return False, d

        def proc_day_of_month(d):
            rule = expanded[2  + seconds]
            if '*' not in rule:
                days = DAYS[month - 1]
                if month == 2 and self.is_leap(year) is True:
                    days += 1
                if 'l' in rule and days == d.day:
                    return False, d

                diff_day = nearest_diff_method(d.day, rule, days)

                if diff_day is not None and diff_day != 0:
                    d += relativedelta(
                        days=diff_day, hour=0, minute=0, second=0)
                    return True, d

            return False, d

        def proc_day_of_week(d):
            rule = expanded[4 + seconds]
            if '*' not in rule:
                diff_day_of_week = nearest_diff_method(
                    d.isoweekday() % 7, rule, 7)
                if diff_day_of_week is not None and diff_day_of_week != 0:
                    d += relativedelta(days=diff_day_of_week,
                                       hour=0, minute=0, second=0)
                    return True, d

            return False, d

        def proc_day_of_week_nth(d):
            if '*' in nth_weekday_of_month:
                s = nth_weekday_of_month['*']
                for i in range(0, 7):
                    if i in nth_weekday_of_month:
                        nth_weekday_of_month[i].update(s)
                    else:
                        nth_weekday_of_month[i] = s
                del nth_weekday_of_month['*']

            candidates = []
            for wday, nth in nth_weekday_of_month.items():
                c = self._get_nth_weekday_of_month(d.year, d.month, wday)
                for n in nth:
                    if n == "l":
                        candidate = c[-1]
                    elif len(c) < n:
                        continue
                    else:
                        candidate = c[n - 1]
                    if d.day <= candidate:
                        candidates.append(candidate)

            if not candidates:
                days = DAYS[month - 1]
                if month == 2 and self.is_leap(year) is True:
                    days += 1
                d += relativedelta(days=(days - d.day + 1),
                                   hour=0, minute=0, second=0)
                return True, d

            candidates.sort()
            diff_day = candidates[0] - d.day
            if diff_day != 0:
                d += relativedelta(days=diff_day,
                                   hour=0, minute=0, second=0)
                return True, d
            return False, d

        def proc_hour(d):
            rule = expanded[1 + seconds]
            if '*' not in rule:
                diff_hour = nearest_diff_method(d.hour, rule, 24)
                if diff_hour is not None and diff_hour != 0:
                    d += relativedelta(hours=diff_hour, minute=0, second=0)
                    return True, d

            return False, d

        def proc_minute(d):
            rule = expanded[0 + seconds]
            if '*' not in rule:
                diff_min = nearest_diff_method(d.minute, rule, 60)
                if diff_min is not None and diff_min != 0:
                    d += relativedelta(minutes=diff_min, second=0)
                    return True, d

            return False, d

        def proc_second(d):
            if seconds:
                rule = expanded[0]
                if '*' not in rule:
                    diff_sec = nearest_diff_method(d.second, rule, 60)
                    if diff_sec is not None and diff_sec != 0:
                        d += relativedelta(seconds=diff_sec)
                        return True, d
            else:
                # we reset the seconds to zero *anyway*
                d += relativedelta(second=0)

            return False, d

        procs = [proc_month,
                 proc_day_of_month,
                 (proc_day_of_week_nth if nth_weekday_of_month
                     else proc_day_of_week),
                 proc_hour,
                 proc_minute,
                 proc_second]

        while abs(year - current_year) <= self._max_years_between_matches:
            next = False
            for proc in procs:
                (changed, dst) = proc(dst)
                if changed:
                    month, year = dst.month, dst.year
                    next = True
                    break
            if next:
                continue
            return self._datetime_to_timestamp(dst.replace(microsecond=0))

        raise CroniterBadDateError(f'failed to find next date for {expanded}')

    def _get_next_nearest(self, x, to_check):
        small = [item for item in to_check if item < x]
        large = [item for item in to_check if item >= x]
        large.extend(small)
        return large[0]

    def _get_next_nearest_diff(self, x, to_check, range_val):
        for i, d in enumerate(to_check):
            if d == "l":
                # if 'l' then it is the last day of month
                # => its value of range_val
                d = range_val
            if d >= x:
                return d - x
        return to_check[0] - x + range_val

    @staticmethod
    def _get_nth_weekday_of_month(year, month, day_of_week):
        """ For a given year/month return a list of days in nth-day-of-month order.
        The last weekday of the month is always [-1].
        """
        w = (day_of_week + 6) % 7
        c = calendar.Calendar(w).monthdayscalendar(year, month)
        if c[0][0] == 0:
            c.pop(0)
        return tuple(i[0] for i in c)

    def is_leap(self, year):
        if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
            return True
        else:
            return False

    @classmethod
    def _expand(cls, expr_format):
        # Split the expression in components, and normalize L -> l, MON -> mon,
        # etc. Keep expr_format untouched so we can use it in the exception
        # messages.
        efl = expr_format.lower()
        expressions = efl.split()

        if len(expressions) not in VALID_LEN_EXPRESSION:
            raise CroniterBadCronError(cls.bad_length)

        expanded = []
        nth_weekday_of_month = {}
        seconds = len(expressions) == 6

        if seconds:
            keys = ('sec', 'min', 'hour', 'day', 'month', 'dow')
        else:
            keys = ('min', 'hour', 'day', 'month', 'dow')

        for key, expr in zip(keys, expressions):
            e_list = expr.split(',')
            res = []

            while len(e_list) > 0:
                e = e_list.pop()
                nth = None

                if key == 'dow':
                    # Handle special case in the dow expression: 2#3, l3
                    special_dow_rem = special_dow_re.match(str(e))
                    if special_dow_rem:
                        g = special_dow_rem.groupdict()
                        he, last = g.get('he', ''), g.get('last', '')
                        if he:
                            e = he
                            try:
                                nth = int(last)
                                assert (nth >= 1 and nth <= 5)
                            except (KeyError, ValueError, AssertionError):
                                raise CroniterBadCronError(
                                    "[{0}] is not acceptable.  Invalid day_of_week "
                                    "value: '{1}'".format(expr_format, nth))
                        elif last:
                            e = last
                            nth = g['pre']  # 'l'

                rangemin = cls.RANGES[key][0]
                rangemax = cls.RANGES[key][1]

                # Before matching step_search_re, normalize "*" to "{min}-{max}".
                # Example: in the minute field, "*/5" normalizes to "0-59/5"
                t = re.sub(
                    r'^\*(\/.+)$',
                    r'%d-%d\1' % (rangemin, rangemax),
                    str(e)
                )
                m = step_search_re.search(t)

                if not m:
                    # Before matching step_search_re,
                    # normalize "{start}/{step}" to "{start}-{max}/{step}".
                    # Example: in the minute field, "10/5" normalizes to "10-59/5"
                    t = re.sub(
                        r'^(.+)\/(.+)$',
                        r'\1-%d/\2' % rangemax,
                        str(e)
                    )
                    m = step_search_re.search(t)

                if m:
                    # early abort if low/high are out of bounds

                    (low, high, step) = m.group(1), m.group(2), m.group(4) or 1
                    if key == 'day' and high == 'l':
                        high = '31'

                    if not only_int_re.search(low):
                        low = "{0}".format(cls._alphaconv(key, low, expressions))

                    if not only_int_re.search(high):
                        high = "{0}".format(cls._alphaconv(key, high, expressions))

                    if (
                        not low or not high or int(low) > int(high)
                        or not only_int_re.search(str(step))
                    ):
                        if key == 'dow' and high == '0':
                            # handle -Sun notation -> 7
                            high = '7'
                        else:
                            raise CroniterBadCronError(
                                '[{0}] is not acceptable'.format(expr_format)
                            )

                    low, high, step = map(int, [low, high, step])
                    if max(low, high) > max(rangemin, rangemax):
                        raise CroniterBadCronError(
                            '{0} is out of bounds'.format(expr_format)
                        )
                    try:
                        rng = range(low, high + 1, step)
                    except ValueError as exc:
                        raise CroniterBadCronError(
                            'invalid range: {0}'.format(exc)
                        )
                    e_list += (
                        ['{0}#{1}'.format(item, nth) for item in rng]
                        if key == 'dow' and nth and nth != 'l' else rng
                    )
                else:
                    if t.startswith('-'):
                        raise CroniterBadCronError((
                            '[{0}] is not acceptable, '
                            'negative numbers not allowed'
                        ).format(expr_format))
                    if not star_or_int_re.search(t):
                        t = cls._alphaconv(key, t, expressions)

                    try:
                        t = int(t)
                    except ValueError:
                        pass

                    if key in ('day', 'month') and isinstance(t, int):
                        if t < rangemin or t > rangemax:
                            raise CroniterBadCronError(
                                '[{0}] is not acceptable, out of range'.format(
                                    expr_format)
                            )

                    if key == 'dow' and t in cls.LOWMAP[key]:
                        t = cls.LOWMAP[key][t]

                    if (t not in ['*', 'l'] and
                        (int(t) < cls.RANGES[key][0] or
                         int(t) > cls.RANGES[key][1])):
                        raise CroniterBadCronError(
                            '[{0}] is not acceptable, out of range'.format(
                                expr_format)
                        )

                    res.append(t)

                    if key == 'dow' and nth:
                        if t not in nth_weekday_of_month:
                            nth_weekday_of_month[t] = set()
                        nth_weekday_of_month[t].add(nth)

            res = set(res)
            res = sorted(
                res,
                key=lambda it: '{:02}'.format(it) if isinstance(it, int) else it
            )
            if len(res) == cls.LEN_MEANS_ALL[key]:
                res = ['*']

            expanded.append(
                ['*'] if (len(res) == 1 and res[0] == '*') else res
            )

        # Check to make sure the dow combo in use is supported
        if nth_weekday_of_month:
            dow_expanded_set = set(expanded[4 + seconds])
            dow_expanded_set = dow_expanded_set.difference(nth_weekday_of_month.keys())
            dow_expanded_set.discard("*")
            if dow_expanded_set:
                raise CroniterUnsupportedSyntaxError(
                    "day-of-week field does not support mixing literal values and nth day of week"
                    " syntax.  "
                    "Cron: '{}'    dow={} vs nth={}".format(
                        expr_format, dow_expanded_set, nth_weekday_of_month
                    )
                )

        return expanded, expressions, nth_weekday_of_month

    @classmethod
    def expand(cls, expr_format):
        """Shallow non Croniter ValueError inside a nice CroniterBadCronError"""
        try:
            return cls._expand(expr_format)
        except (ValueError,) as exc:
            error_type, error_instance, traceback = sys.exc_info()
            if isinstance(exc, CroniterError):
                raise
            if int(sys.version[0]) >= 3:
                trace = _traceback.format_exc()
                raise CroniterBadCronError(trace)
            else:
                raise CroniterBadCronError("{0}".format(exc))

    @classmethod
    def is_valid(cls, expression):
        try:
            cls.expand(expression)
        except CroniterError:
            return False
        else:
            return True


def croniter_range(start, stop, expr_format, ret_type=None, day_or=True, exclude_ends=False,
                   _croniter=None):
    """
    Generator that provides all times from start to stop matching the given cron expression.
    If the cron expression matches either 'start' and/or 'stop', those times will be returned as
    well unless 'exclude_ends=True' is passed.

    You can think of this function as sibling to the builtin range function for datetime objects.
    Like range(start,stop,step), except that here 'step' is a cron expression.
    """
    _croniter = _croniter or croniter
    auto_rt = datetime.datetime
    # type is used in first if branch for perfs reasons
    if (
        type(start) is not type(stop) and not (
            isinstance(start, type(stop)) or
            isinstance(stop, type(start)))
    ):
        raise CroniterBadTypeRangeError(
            "The start and stop must be same type.  {0} != {1}".
            format(type(start), type(stop)))
    if isinstance(start, (float, int)):
        start, stop = (datetime.datetime.fromtimestamp(t, tzutc()).replace(tzinfo=None) for t in (start, stop))
        auto_rt = float
    if ret_type is None:
        ret_type = auto_rt
    if not exclude_ends:
        ms1 = relativedelta(microseconds=1)
        if start < stop:    # Forward (normal) time order
            start -= ms1
            stop += ms1
        else:               # Reverse time order
            start += ms1
            stop -= ms1
    year_span = math.floor(abs(stop.year - start.year)) + 1
    ic = _croniter(expr_format, start, ret_type=datetime.datetime, day_or=day_or,
                   max_years_between_matches=year_span)
    # define a continue (cont) condition function and step function for the main while loop
    assert start <= stop
    def cont(v):
        return v < stop
    step = ic.get_next
    try:
        dt = step()
        while cont(dt):
            if ret_type is float:
                yield ic.get_current(float)
            else:
                yield dt
            dt = step()
    except CroniterBadDateError:
        # Stop iteration when this exception is raised; no match found within the given year range
        return
