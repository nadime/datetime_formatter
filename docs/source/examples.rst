====================
Additional Examples
====================

Simplest example possible
-------------------------

.. code-block:: python

  >>> from datetime import date, datetime, time
   >>> from datetime_format import dtfmt, DateTimeFormatter
   >>> from dateutil.tz import gettz
   >>> import holidays
   >>>
   >>> dtfmt(20050301, "YMD")
   '20050301'
   >>> dtfmt(20050301, "HHMMSS")
   '00:00:00'

All Output Formats/Styles
-------------------------

Here is a code-built list of all of the possible output formats:

.. code-block:: python

  >>> from datetime_format.__formats import _SUPPORTED_DATETIME_OUTPUT_FORMATS
   >>>
   >>> dt = datetime(2022, 4, 12, 9, 30, 0, 0, tzinfo=gettz("EDT"))
   >>> for k in _SUPPORTED_DATETIME_OUTPUT_FORMATS.keys():
   ...     print(f"{k}:{' '*(15-len(k))}{dtfmt(dt, k)}")
   ...
   DATE:           2022-04-12
   DATETIME:       2022-04-12 09:30:00
   USDATE:         04/12/22
   USDATETIME:     04/12/22 09:30:00
   TIME:           09:30:00
   YEAR:           2022
   YMD:            20220412
   YYYYMM:         202204
   MMYYYY:         042022
   YYMM:           2204
   MMYY:           0422
   YYYYMMDD:       20220412
   MMDDYY:         041222
   MMDDYYYY:       04122022
   ISODATE:        2022-04-12
   ISODATETIME:    2022-04-12T09:30:00-04:00
   MONTH:          04
   MON:            04
   MONTHABV:       Apr
   MONTHNAME:      April
   DAYABV:         Tue
   DAYNAME:        Tuesday
   DAYNUM:         2
   DAYYEAR:        102
   TZOFF:          -0400
   TZNAME:         EDT
   WEEKNUM:        15
   DAY:            12
   DD:             12
   MM:             04
   YY:             22
   YYYY:           2022
   LOCALE_DT:      Tue Apr 12 09:30:00 2022
   HHMMSS:         09:30:00
   HHMMSSZZ:       09:30:00.000000
   AMPM:           AM
   HH:             09

Datetime Translations
---------------------
You can also translate these dates inline, inside your string formatting.  Why
would you do this, rather than translating in your Python code (using
``timedelta`` or ``dateutil.relativedelta``)?  One example might be if you
write configuration files read by Python (and potentially other interpreters)
in something like YAML and you want your configuration to be descriptive given
a starting datetime. Or if you want to run a tool with command-line parameters
involving dates without having to jump through hoops by translating multiple
dates as you invoke your command.

Here's a code-generated list of moving 2 "units" away from our date above,
in both directions (``-`` & ``+``), for every possible unit.  The choice to
move "2" units is, of course, arbitrary - any whole number (integer >= 0) is
allowed.  Negative integers are not allowed simply because we support "minus",
so there is no need to also support negative unit moves -- that would just
make our syntax clunky.

Below you can see every translation possible "2" units away from our existing
``datetime`` from above:

.. code-block:: python3

 >>> dt.isoformat()
  '2022-04-12T09:30:00-04:00'

All possible translations:

.. code-block:: python

 >>> from datetime_format.__formats import (
  ...     _SUPPORTED_TRANSLATION_DIRECTIONS,
  ...     _SUPPORTED_TRANSLATION_SIZES,
  ... )
  >>> from itertools import product
  >>> for (d,s) in product(_SUPPORTED_TRANSLATION_DIRECTIONS, _SUPPORTED_TRANSLATION_SIZES):
  ...     print(f"{d}2{s}:{' '*8}{dtfmt(dt, f'ISODATETIME-{d}2{s}')}")
  ...
  M2Y:        2020-04-12T09:30:00-04:00
  M2m:        2022-02-12T09:30:00-05:00
  M2D:        2022-04-10T09:30:00-04:00
  M2W:        2022-03-29T09:30:00-04:00
  M2H:        2022-04-12T07:30:00-04:00
  M2M:        2022-04-12T09:28:00-04:00
  M2S:        2022-04-12T09:29:58-04:00
  M2Z:        2022-04-12T09:29:59.999998-04:00
  M2B:        2022-04-08T09:30:00-04:00
  M2F:        2022-03-29T09:30:00-04:00
  M2P:        2022-02-11T09:30:00-05:00
  M2K:        2020-04-10T09:30:00-04:00
  P2Y:        2024-04-12T09:30:00-04:00
  P2m:        2022-06-12T09:30:00-04:00
  P2D:        2022-04-14T09:30:00-04:00
  P2W:        2022-04-26T09:30:00-04:00
  P2H:        2022-04-12T11:30:00-04:00
  P2M:        2022-04-12T09:32:00-04:00
  P2S:        2022-04-12T09:30:02-04:00
  P2Z:        2022-04-12T09:30:00.000002-04:00
  P2B:        2022-04-14T09:30:00-04:00
  P2F:        2022-04-26T09:30:00-04:00
  P2P:        2022-06-13T09:30:00-04:00
  P2K:        2024-04-12T09:30:00-04:00
  m2Y:        2020-04-12T09:30:00-04:00
  m2m:        2022-02-12T09:30:00-05:00
  m2D:        2022-04-10T09:30:00-04:00
  m2W:        2022-03-29T09:30:00-04:00
  m2H:        2022-04-12T07:30:00-04:00
  m2M:        2022-04-12T09:28:00-04:00
  m2S:        2022-04-12T09:29:58-04:00
  m2Z:        2022-04-12T09:29:59.999998-04:00
  m2B:        2022-04-08T09:30:00-04:00
  m2F:        2022-03-29T09:30:00-04:00
  m2P:        2022-02-11T09:30:00-05:00
  m2K:        2020-04-10T09:30:00-04:00
  p2Y:        2024-04-12T09:30:00-04:00
  p2m:        2022-06-12T09:30:00-04:00
  p2D:        2022-04-14T09:30:00-04:00
  p2W:        2022-04-26T09:30:00-04:00
  p2H:        2022-04-12T11:30:00-04:00
  p2M:        2022-04-12T09:32:00-04:00
  p2S:        2022-04-12T09:30:02-04:00
  p2Z:        2022-04-12T09:30:00.000002-04:00
  p2B:        2022-04-14T09:30:00-04:00
  p2F:        2022-04-26T09:30:00-04:00
  p2P:        2022-06-13T09:30:00-04:00
  p2K:        2024-04-12T09:30:00-04:00

You can also specify ``holidays`` to skip using
the `holidays <https://pypi.org/project/holidays>`_ module.

.. code-block:: python

  >>> import holidays
  >>>
  >>> # day before xmas -> day after xmas - 20201224=Thu
  >>> dtfmt(20201224, "YMD-P1D", holidays=holidays.US())
  '20201226'

Finally, as long as you've specified a ``timezone`` alongside the ``datetime`` you
are formatting and/or translating, you can also convert to a different timezone
before outputting anything.

.. code-block:: python

 >>> # start in EDT
  >>> dt.isoformat()
  '2022-04-12T09:30:00-04:00'
  >>> # end in UTC
  >>> dtfmt(dt, "ISODATETIME", output_tz=gettz("utc"))
  '2022-04-12T13:30:00+00:00'
