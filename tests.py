import unittest
import json

from argumentation import ArgumentationFramework

class AFSlideExampleTests(unittest.TestCase):
    def setUp(self):
        af = json.load(open('slide-example.json'))
        self.af = ArgumentationFramework(
            arguments=af['Arguments'],
            attack_relations=af['Attack Relations'])
    
    def tearDown(self):
        delattr(self, 'af')

    def test_conflict_free(self):
        self.af.find_conflict_free()
        
        expected = {frozenset(), frozenset({'a'}), frozenset({'b'}), frozenset({'c'}), frozenset({'d'}),
                    frozenset({'a', 'c'}), frozenset({'a', 'd'}), frozenset({'b', 'd'})}
        actual = self.af.cf

        self.assertTrue(expected.issubset(actual))
        self.assertTrue(actual.issubset(expected))
    
    def test_admissible(self):
        self.af.find_conflict_free()
        self.af.find_admissible()
        
        expected = {frozenset(), frozenset({'a'}), frozenset({'c'}), frozenset({'d'}),
                    frozenset({'a', 'c'}), frozenset({'a', 'd'})}
        actual = self.af.adm

        self.assertTrue(expected.issubset(actual))
        self.assertTrue(actual.issubset(expected))

class AFSimpleCFTests(unittest.TestCase):
    def test_conflict_free1(self):
        af = ArgumentationFramework(['1', '2', '3'], [['1', '2'], ['2', '3'], ['3', '1']])
        af.find_conflict_free()
        
        expected = {frozenset(), frozenset({'1'}), frozenset({'2'}), frozenset({'3'})}
        actual = af.cf

        self.assertTrue(expected.issubset(actual))
        self.assertTrue(actual.issubset(expected))

    def test_conflict_free2(self):
        af = ArgumentationFramework(['1', '2', '3'], [])
        af.find_conflict_free()
        
        expected = {frozenset(), frozenset({'1'}), frozenset({'2'}), frozenset({'3'}),
                    frozenset({'1', '2'}), frozenset({'1', '3'}), frozenset({'2', '3'}),
                    frozenset({'1', '2', '3'})}
        actual = af.cf

        self.assertTrue(expected.issubset(actual))
        self.assertTrue(actual.issubset(expected))

    def test_conflict_free3(self):
        af = ArgumentationFramework(['1', '2'], [['1', '1']])
        af.find_conflict_free()
        
        expected = {frozenset(), frozenset({'2'})}
        actual = af.cf

        self.assertTrue(expected.issubset(actual))
        self.assertTrue(actual.issubset(expected))

    def test_conflict_free4(self):
        af = ArgumentationFramework([], [['a', 'a']])
        af.find_conflict_free()
        
        expected = {frozenset()}
        actual = af.cf

        self.assertTrue(expected.issubset(actual))
        self.assertTrue(actual.issubset(expected))

class AFSimpleADMTests(unittest.TestCase):
    # Add tests similar to the ones above
    pass


if __name__ == "__main__":
    unittest.main()