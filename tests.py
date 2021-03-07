import unittest
from main import *
class TestEveryMethodInMain(unittest.TestCase):
    #def test_GetContainer(self):
    #    self.assertIsNotNone(getPricesContainer())
    #    self.assertIsNotNone(returnListedPricesToServer())
    #    self.assertIsNotNone(returnInOrderedPricesToServer())
    '''
    FUNKCJE
        not none returnListedPricesToServer, returnInOrderedPricesToServer
    checkPriceDiffWithDatabase
        calculateQuickSellPrice
        takeMinPriceFromRange
    getSearchedItems
    '''
    def test_takeMinPriceFromRange(self):
        _input = [{"CRL Eastern [Dominus]":{"Normal":{"price":[200,300]}}},{"Alchemist":{"Black":{"price":[2300,2500]}}},{"Overgrowth":{"Titanium White":{"price":[350,450]}},"Dominus":{"Lime":{"price":[4900,5300]}}}]
        _output = [{"CRL Eastern [Dominus]":{"Normal":{"price":200}}},{"Alchemist":{"Black":{"price":2300}}},{"Overgrowth":{"Titanium White":{"price":350}},"Dominus":{"Lime":{"price":4900}}}]
        self.assertEqual(takeMinPriceFromRange(_input), _output)
        self.assertEqual(takeMinPriceFromRange([{"Item": {"paint": {"price":[21,37]}}}]), [{"Item": {"paint": {"price":21}}}])
    # tests = [{input: [], expected: []},{items: [], expected: []}]
    # for test in tests:
    #   asssert(test.expected, takeMinPriceFromRange(test.items))
    def test_calculateQuickSellPrice(self):
        _input = [{"CRL Eastern [Dominus]":{"Normal":{"price":200}}},{"Alchemist":{"Black":{"price":2300}}},{"Overgrowth":{"Titanium White":{"price":350}},"Dominus":{"Lime":{"price":4900}}}]
        _output = [{"CRL Eastern [Dominus]":{"Normal":{"price":100}}},{"Alchemist":{"Black":{"price":2200}}},{"Overgrowth":{"Titanium White":{"price":250}},"Dominus":{"Lime":{"price":4800}}}]
        self.assertEqual(calculateQuickSellPrice(_input, 100), _output)

if __name__ == "__main__":
    unittest.main()
