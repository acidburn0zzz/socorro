# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import datetime
from nose.tools import eq_, ok_, assert_raises

from socorrolib.lib import MissingArgumentError, datetimeutil
from socorro.external.postgresql.releases import Releases

from .unittestbase import PostgreSQLTestCase


#==============================================================================
class IntegrationTestReleases(PostgreSQLTestCase):
    """Test socorro.external.postgresql.releases.Releases class. """

    #--------------------------------------------------------------------------
    def setUp(self):
        """Set up this test class by populating the reports table with fake
        data. """
        super(IntegrationTestReleases, self).setUp()

        cursor = self.connection.cursor()

        # Insert data
        now = datetimeutil.utc_now()
        build_date = now - datetime.timedelta(days=30)
        sunset_date = now + datetime.timedelta(days=30)

        cursor.execute("""
            INSERT INTO products
            (product_name, sort, release_name)
            VALUES
            (
                'Firefox',
                1,
                'firefox'
            ),
            (
                'FennecAndroid',
                2,
                'fennecandroid'
            ),
            (
                'Thunderbird',
                3,
                'thunderbird'
            );
        """)

        cursor.execute("""
            INSERT INTO product_versions
            (product_version_id, product_name, major_version, release_version,
             version_string, version_sort, build_date, sunset_date,
             featured_version, build_type)
            VALUES
            (
                1,
                'Firefox',
                '15.0',
                '15.0',
                '15.0a1',
                '000000150a1',
                '%(build_date)s',
                '%(sunset_date)s',
                't',
                'Nightly'
            ),
            (
                2,
                'Firefox',
                '14.0',
                '14.0',
                '14.0a2',
                '000000140a2',
                '%(build_date)s',
                '%(sunset_date)s',
                'f',
                'Aurora'
            ),
            (
                3,
                'Firefox',
                '13.0',
                '13.0',
                '13.0b1',
                '000000130b1',
                '%(build_date)s',
                '%(sunset_date)s',
                't',
                'Beta'
            ),
            (
                4,
                'FennecAndroid',
                '15.0',
                '15.0',
                '15.0a1',
                '000000150a1',
                '%(build_date)s',
                '%(sunset_date)s',
                't',
                'Nightly'
            ),
            (
                5,
                'FennecAndroid',
                '14.0',
                '14.0',
                '14.0a1',
                '000000140a1',
                '%(build_date)s',
                '%(sunset_date)s',
                'f',
                'Aurora'
            ),
            (
                6,
                'Thunderbird',
                '15.0',
                '15.0',
                '15.0a1',
                '000000150a1',
                '%(build_date)s',
                '%(sunset_date)s',
                't',
                'Nightly'
            ),
            (
                7,
                'Firefox',
                '24.5',
                '24.5.0esr',
                '24.5.0esr',
                '024005000x000',
                '%(build_date)s',
                '%(sunset_date)s',
                'f',
                'ESR'
            )
            ;
        """ % {"build_date": build_date, "sunset_date": sunset_date})

        self.connection.commit()

    #--------------------------------------------------------------------------
    def tearDown(self):
        """Clean up the database, delete tables and functions. """
        cursor = self.connection.cursor()
        cursor.execute("""
            TRUNCATE
                product_versions,
                products,
                releases_raw,
                release_channels,
                product_release_channels
            CASCADE
        """)
        self.connection.commit()
        super(IntegrationTestReleases, self).tearDown()

    def _insert_release_channels(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO release_channels
            (release_channel, sort)
            VALUES
            ('Nightly', 1),
            ('Aurora', 2),
            ('Beta', 3),
            ('Release', 4),
            ('ESR', 5);
        """)
        self.connection.commit()

    def _insert_product_release_channels(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO product_release_channels
            (product_name, release_channel, throttle)
            VALUES
            ('Firefox', 'Nightly', 1),
            ('Firefox', 'Aurora', 1),
            ('Firefox', 'Beta', 1),
            ('Firefox', 'Release', 1),
            ('Firefox', 'ESR', 1),
            ('Thunderbird', 'Nightly', 1),
            ('Thunderbird', 'Aurora', 1),
            ('Thunderbird', 'Beta', 1),
            ('Thunderbird', 'Release', 1),
            ('FennecAndroid', 'Nightly', 1),
            ('FennecAndroid', 'Aurora', 1),
            ('FennecAndroid', 'Beta', 1),
            ('FennecAndroid', 'Release', 1);
        """)
        self.connection.commit()

    #--------------------------------------------------------------------------
    def test_get_channels(self):
        self._insert_release_channels()
        self._insert_product_release_channels()
        service = Releases(config=self.config)

        #......................................................................
        # Test 1: one product
        params = {
            "products": ["Firefox"]
        }
        res = service.get_channels(**params)
        res_expected = {
            "Firefox": ["Beta", "Aurora", "Nightly", "ESR"]
        }
        eq_(res, res_expected)

        #......................................................................
        # Test 2: several products
        params = {
            "products": ["Firefox", "FennecAndroid"]
        }
        res = service.get_channels(**params)
        res_expected = {
            "FennecAndroid": ["Aurora", "Nightly"],
            "Firefox": ["Beta", "Aurora", "Nightly", "ESR"]
        }
        eq_(res, res_expected)

        #......................................................................
        # Test 3: an unknown product
        params = {
            "products": ["Unknown"]
        }
        res = service.get_channels(**params)
        res_expected = {}
        eq_(res, res_expected)

        #......................................................................
        # Test 4: all products
        res = service.get_channels()
        res_expected = {
            "Thunderbird": ["Nightly"],
            "FennecAndroid": ["Aurora", "Nightly"],
            "Firefox": ["Beta", "Aurora", "Nightly", "ESR"]
        }
        eq_(res, res_expected)

    #--------------------------------------------------------------------------
    def test_get_featured(self):
        self._insert_release_channels()
        self._insert_product_release_channels()
        service = Releases(config=self.config)

        #......................................................................
        # Test 1: one product
        params = {
            "products": ["Firefox"]
        }
        res = service.get_featured(**params)
        res_expected = {
            "hits": {
                "Firefox": ["13.0b1", "15.0a1"]
            },
            "total": 2
        }
        eq_(res, res_expected)

        #......................................................................
        # Test 2: several products, several versions
        params = {
            "products": ["Firefox", "FennecAndroid", "Thunderbird"]
        }
        res = service.get_featured(**params)
        res_expected = {
            "hits": {
                "Firefox": ["13.0b1", "15.0a1"],
                "FennecAndroid": ["15.0a1"],
                "Thunderbird": ["15.0a1"]
            },
            "total": 4
        }
        eq_(res, res_expected)

        #......................................................................
        # Test 3: an unknown product
        params = {
            "products": ["Unknown"]
        }
        res = service.get_featured(**params)
        res_expected = {
            "hits": {},
            "total": 0
        }
        eq_(res, res_expected)

        #......................................................................
        # Test 4: all products
        res = service.get_featured()
        res_expected = {
            "hits": {
                "Firefox": ["13.0b1", "15.0a1"],
                "FennecAndroid": ["15.0a1"],
                "Thunderbird": ["15.0a1"]
            },
            "total": 4
        }
        eq_(res, res_expected)

    #--------------------------------------------------------------------------
    def test_update_featured(self):
        self._insert_release_channels()
        self._insert_product_release_channels()

        service = Releases(config=self.config)

        #......................................................................
        # Test 1: one product, several versions
        params = {
            "Firefox": [
                "15.0a1",
                "14.0a2",
                "13.0b1"
            ]
        }
        res = service.update_featured(**params)
        ok_(res)

        res = service.get_featured()
        res_expected = {
            "hits": {
                "Firefox": ["13.0b1", "14.0a2", "15.0a1"],
                "Thunderbird": ["15.0a1"],
                "FennecAndroid": ["15.0a1"]
            },
            "total": 5
        }
        eq_(res, res_expected)

        #......................................................................
        # Test 2: several products, several versions
        params = {
            "Firefox": [
                "13.0b1"
            ],
            "FennecAndroid": [
                "14.0a1"
            ]
        }
        res = service.update_featured(**params)
        ok_(res)

        res = service.get_featured()
        res_expected = {
            "hits": {
                "Firefox": ["13.0b1"],
                "Thunderbird": ["15.0a1"],
                "FennecAndroid": ["14.0a1"]
            },
            "total": 3
        }
        eq_(res, res_expected)

        #......................................................................
        # Test 3: an unknown product
        params = {
            "Unknown": [
                "15.0a1"
            ]
        }
        res = service.update_featured(**params)
        ok_(not res)

        res = service.get_featured()
        res_expected = {
            "hits": {
                "Firefox": ["13.0b1"],
                "Thunderbird": ["15.0a1"],
                "FennecAndroid": ["14.0a1"]
            },
            "total": 3
        }
        eq_(res, res_expected)

        #......................................................................
        # Test 4: an unknown product and an existing product
        params = {
            "Firefox": [
                "14.0a2"
            ],
            "Unknown": [
                "15.0a1"
            ]
        }
        res = service.update_featured(**params)
        ok_(res)

        res = service.get_featured()
        res_expected = {
            "hits": {
                "Firefox": ["14.0a2"],
                "Thunderbird": ["15.0a1"],
                "FennecAndroid": ["14.0a1"]
            },
            "total": 3
        }
        eq_(res, res_expected)

        #......................................................................
        # Test 4: an unknown version
        params = {
            "Firefox": [
                "200.0a1"  # that's like, in 2035, dude
            ]
        }
        res = service.update_featured(**params)
        ok_(res)

        res = service.get_featured()
        res_expected = {
            "hits": {
                "Thunderbird": ["15.0a1"],
                "FennecAndroid": ["14.0a1"]
            },
            "total": 2
        }
        eq_(res, res_expected)

    def test_create_release(self):
        self._insert_release_channels()
        service = Releases(config=self.config)

        now = datetimeutil.utc_now()
        build_id = now.strftime('%Y%m%d%H%M')
        params = dict(
            product='Firefox',
            version='1.0',
            update_channel='beta',
            build_id=build_id,
            platform='Windows',
            beta_number=1,
            release_channel='Beta',
            throttle=1
        )

        res = service.create_release(**params)
        ok_(res)

    def test_create_release_with_beta_number_null(self):
        self._insert_release_channels()
        service = Releases(config=self.config)

        now = datetimeutil.utc_now()
        build_id = now.strftime('%Y%m%d%H%M')
        params = dict(
            product='Firefox',
            version='1.0',
            update_channel='beta',
            build_id=build_id,
            platform='Windows',
            beta_number=None,
            release_channel='Beta',
            throttle=1
        )

        res = service.create_release(**params)
        ok_(res)

        # but...
        params['beta_number'] = 0
        assert_raises(
            MissingArgumentError,
            service.create_release,
            **params
        )

    def test_update_release_missingargumenterror(self):
        self._insert_release_channels()
        service = Releases(config=self.config)

        now = datetimeutil.utc_now()
        build_id = now.strftime('%Y%m%d%H%M')
        params = dict(
            product='',
            version='1.0',
            update_channel='beta',
            build_id=build_id,
            platform='Windows',
            beta_number=1,
            release_channel='Beta',
            throttle=1
        )
        assert_raises(
            MissingArgumentError,
            service.create_release,
            **params
        )
