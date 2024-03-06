import datetime
import unittest
from src.tbgutils.dt import is_holiday_observed, yyyymmdd2dt, eom


class DTTests(unittest.TestCase):
    def test_is_holiday(self):
        expected = [[20140101, 'Wednesday New Years Day'],
                    [20140120, 'Monday MLK Day'],
                    [20140217, 'Monday Presidents Day'],
                    [20140418, 'Friday Easter Friday'],
                    [20140526, 'Monday Memorial Day'],
                    [20140704, 'Friday Independence Day'],
                    [20140901, 'Monday Labor Day'],
                    [20141127, 'Thursday Thanksgiving Day'],
                    [20141225, 'Thursday Christmas Day'],
                    [20150101, 'Thursday New Years Day'],
                    [20150119, 'Monday MLK Day'],
                    [20150216, 'Monday Presidents Day'],
                    [20150403, 'Friday Easter Friday'],
                    [20150525, 'Monday Memorial Day'],
                    [20150703, 'Friday Independence Day'],
                    [20150704, 'Saturday Independence Day'],
                    [20150907, 'Monday Labor Day'],
                    [20151126, 'Thursday Thanksgiving Day'],
                    [20151225, 'Friday Christmas Day'],
                    [20160101, 'Friday New Years Day'],
                    [20160118, 'Monday MLK Day'],
                    [20160215, 'Monday Presidents Day'],
                    [20160325, 'Friday Easter Friday'],
                    [20160530, 'Monday Memorial Day'],
                    [20160704, 'Monday Independence Day'],
                    [20160905, 'Monday Labor Day'],
                    [20161124, 'Thursday Thanksgiving Day'],
                    [20161225, 'Sunday Christmas Day'],
                    [20161226, 'Monday Christmas Day'],
                    [20170101, 'Sunday New Years Day'],
                    [20170102, 'Monday New Years Day'],
                    [20170116, 'Monday MLK Day'],
                    [20170220, 'Monday Presidents Day'],
                    [20170414, 'Friday Easter Friday'],
                    [20170529, 'Monday Memorial Day'],
                    [20170704, 'Tuesday Independence Day'],
                    [20170904, 'Monday Labor Day'],
                    [20171123, 'Thursday Thanksgiving Day'],
                    [20171225, 'Monday Christmas Day'],
                    [20180101, 'Monday New Years Day'],
                    [20180115, 'Monday MLK Day'],
                    [20180219, 'Monday Presidents Day'],
                    [20180330, 'Friday Easter Friday'],
                    [20180528, 'Monday Memorial Day'],
                    [20180704, 'Wednesday Independence Day'],
                    [20180903, 'Monday Labor Day'],
                    [20181122, 'Thursday Thanksgiving Day'],
                    [20181225, 'Tuesday Christmas Day'],
                    [20190101, 'Tuesday New Years Day'],
                    [20190121, 'Monday MLK Day'],
                    [20190218, 'Monday Presidents Day'],
                    [20190419, 'Friday Easter Friday'],
                    [20190527, 'Monday Memorial Day'],
                    [20190704, 'Thursday Independence Day'],
                    [20190902, 'Monday Labor Day'],
                    [20191128, 'Thursday Thanksgiving Day'],
                    [20191225, 'Wednesday Christmas Day'],
                    [20200101, 'Wednesday New Years Day'],
                    [20200120, 'Monday MLK Day'],
                    [20200217, 'Monday Presidents Day'],
                    [20200410, 'Friday Easter Friday'],
                    [20200525, 'Monday Memorial Day'],
                    [20200703, 'Friday Independence Day'],
                    [20200704, 'Saturday Independence Day'],
                    [20200907, 'Monday Labor Day'],
                    [20201126, 'Thursday Thanksgiving Day'],
                    [20201225, 'Friday Christmas Day'],
                    [20210101, 'Friday New Years Day'],
                    [20210118, 'Monday MLK Day'],
                    [20210215, 'Monday Presidents Day'],
                    [20210402, 'Friday Easter Friday'],
                    [20210531, 'Monday Memorial Day'],
                    [20210704, 'Sunday Independence Day'],
                    [20210705, 'Monday Independence Day'],
                    [20210906, 'Monday Labor Day'],
                    [20211125, 'Thursday Thanksgiving Day'],
                    [20211224, 'Friday Christmas Day'],
                    [20211225, 'Saturday Christmas Day'],
                    [20211231, 'Friday New Years Day'],
                    [20220101, 'Saturday New Years Day'],
                    [20220117, 'Monday MLK Day'],
                    [20220221, 'Monday Presidents Day'],
                    [20220415, 'Friday Easter Friday'],
                    [20220530, 'Monday Memorial Day'],
                    [20220704, 'Monday Independence Day'],
                    [20220905, 'Monday Labor Day'],
                    [20221124, 'Thursday Thanksgiving Day'],
                    [20221225, 'Sunday Christmas Day'],
                    [20221226, 'Monday Christmas Day'],
                    [20230101, 'Sunday New Years Day'],
                    [20230102, 'Monday New Years Day'],
                    [20230116, 'Monday MLK Day'],
                    [20230220, 'Monday Presidents Day'],
                    [20230407, 'Friday Easter Friday'],
                    [20230529, 'Monday Memorial Day'],
                    [20230704, 'Tuesday Independence Day'],
                    [20230904, 'Monday Labor Day'],
                    [20231123, 'Thursday Thanksgiving Day'],
                    [20231225, 'Monday Christmas Day'],
                    [20240101, 'Monday New Years Day'],
                    [20220619, 'Weekend'],
                    [20220620, 'Junteenth Observed'],
                    [20230619, 'Junteenth']
                    ]

        expected = [yyyymmdd2dt(i).date() for i, j in expected]
        d = yyyymmdd2dt(20140101).date()
        flag = True
        for i in range(3657):
            if is_holiday_observed(d, weekend_f=False):
                if d not in expected:
                    flag = False

            d = d + datetime.timedelta(days=1)

        self.assertTrue(flag)

    def test_eom(self):
        d = datetime.date(2024, 10, 21)
        d = eom(d)
        self.assertEquals(d.month, 10)
        self.assertEquals(d.day, 31)

        d = datetime.date(2024, 12, 21)
        d = eom(d)
        self.assertEquals(d.year, 2024)
        self.assertEquals(d.month, 12)
        self.assertEquals(d.day, 31)
