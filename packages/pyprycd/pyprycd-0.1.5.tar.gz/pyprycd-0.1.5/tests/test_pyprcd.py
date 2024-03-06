import unittest

from pyprycd import PyPrycd


class TestPyPrycd(unittest.TestCase):

    def test_get_fips_code(self):
        fips1 = PyPrycd.get_fips_code('Autauga County AL')
        self.assertEqual(fips1, 1001)

    def test_get_counties(self):
        counties = PyPrycd.get_counties_in_state("AZ")
        self.assertEqual(len(counties), 15)
        expected_results = ['Apache County AZ',
                            'Cochise County AZ',
                            'Coconino County AZ',
                            'Gila County AZ',
                            'Graham County AZ',
                            'Greenlee County AZ',
                            'La Paz County AZ',
                            'Maricopa County AZ',
                            'Mohave County AZ',
                            'Navajo County AZ',
                            'Pima County AZ',
                            'Pinal County AZ',
                            'Santa Cruz County AZ',
                            'Yavapai County AZ',
                            'Yuma County AZ']
        self.assertListEqual(counties, expected_results)

        counties2 = PyPrycd.get_counties_in_state("Arizona")
        self.assertListEqual(counties2, expected_results)
