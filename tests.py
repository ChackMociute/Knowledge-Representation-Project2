import unittest
import json
import yaml

from argumentation import ArgumentationFramework

class AFSlideExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        af = json.load(open('slide-example.json'))
        self.af = ArgumentationFramework(
            arguments=af['Arguments'],
            attack_relations=af['Attack Relations'])
        self.af.find_extentions()

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
    
    def test_grounded(self):
        expected = {frozenset({'a'})}
        actual = self.af.grd

        self.assertCountEqual(expected, actual)
    
    def test_stable(self):
        expected = {frozenset({'a', 'd'})}
        actual = self.af.stb

        self.assertCountEqual(expected, actual)


def setUpClassFactory(args, ar):
    @classmethod
    def setUpClass(self):
        self.af = ArgumentationFramework(args, ar)
        self.af.find_extentions()
    return setUpClass

def test_method_factory(exp, attr):
    def test_method(self):
        expected = exp
        actual = getattr(self.af, attr)
        self.assertCountEqual(expected, actual)
    return test_method


classes = yaml.safe_load(open('tests.yaml', 'r'))

for cls in classes:
    globals()[cls['name']] =\
        type(cls['name'], (unittest.TestCase,), {
            'setUpClass': setUpClassFactory(cls['args'], cls['ar'])
        } | {
            meth: test_method_factory(eval(val['exp']), val['attr'])
            for meth, val in cls['methods'].items()
        })

if __name__ == "__main__":
    unittest.main()