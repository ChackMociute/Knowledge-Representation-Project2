import unittest
import json

from argumentation import ArgumentationFramework

class AFSlideExampleTests(unittest.TestCase):
    def setUp(self):
        af = json.load(open('slide-example.json'))
        self.af = ArgumentationFramework(
            arguments=af['Arguments'],
            attack_relations=af['Attack Relations'])
        self.af.find_extentions()
    
    def tearDown(self):
        delattr(self, 'af')

    def test_conflict_free(self):
        expected = {frozenset(), frozenset({'a'}), frozenset({'b'}), frozenset({'c'}), frozenset({'d'}),
                    frozenset({'a', 'c'}), frozenset({'a', 'd'}), frozenset({'b', 'd'})}
        actual = self.af.cf

        self.assertCountEqual(expected, actual)
    
    def test_admissible(self):
        expected = {frozenset(), frozenset({'a'}), frozenset({'c'}), frozenset({'d'}),
                    frozenset({'a', 'c'}), frozenset({'a', 'd'})}
        actual = self.af.adm

        self.assertCountEqual(expected, actual)
    
    def test_preferred(self):
        expected = {frozenset({'a', 'c'}), frozenset({'a', 'd'})}
        actual = self.af.pref

        self.assertCountEqual(expected, actual)
    
    def test_complete(self):
        expected = {frozenset({'a', 'c'}), frozenset({'a', 'd'}), frozenset({'a'})}
        actual = self.af.comp

        self.assertCountEqual(expected, actual)

class AFSimpleCFTests(unittest.TestCase):
    def test_conflict_free1(self):
        af = ArgumentationFramework(['1', '2', '3'], [['1', '2'], ['2', '3'], ['3', '1']])
        af.find_conflict_free()
        
        expected = {frozenset(), frozenset({'1'}), frozenset({'2'}), frozenset({'3'})}
        actual = af.cf

        self.assertCountEqual(expected, actual)

    def test_conflict_free2(self):
        af = ArgumentationFramework(['1', '2', '3'], [])
        af.find_conflict_free()
        
        expected = {frozenset(), frozenset({'1'}), frozenset({'2'}), frozenset({'3'}),
                    frozenset({'1', '2'}), frozenset({'1', '3'}), frozenset({'2', '3'}),
                    frozenset({'1', '2', '3'})}
        actual = af.cf

        self.assertCountEqual(expected, actual)

    def test_conflict_free3(self):
        af = ArgumentationFramework(['1', '2'], [['1', '1']])
        af.find_conflict_free()
        
        expected = {frozenset(), frozenset({'2'})}
        actual = af.cf

        self.assertCountEqual(expected, actual)

    def test_conflict_free4(self):
        af = ArgumentationFramework([], [['a', 'a']])
        af.find_conflict_free()
        
        expected = {frozenset()}
        actual = af.cf

        self.assertCountEqual(expected, actual)

class AFSimplePreferredTests(unittest.TestCase):
    # Add tests similar to the ones above for admissible and preferred
    pass


if __name__ == "__main__":
    unittest.main()