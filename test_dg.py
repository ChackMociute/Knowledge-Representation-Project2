import unittest
from argumentation import ArgumentationFramework
from discussion_game import DiscussionGame

self_attack_af = ArgumentationFramework(['a'], [['a', 'a']])
two_cycle_af = ArgumentationFramework(['a', 'b'], [['a', 'b'], ['b', 'a']])
odd_cycle_af = ArgumentationFramework(['a', 'b', 'c'], [['a', 'b'], ['b', 'c'], ['c', 'a']])
four_cycle_af = ArgumentationFramework(['a', 'b', 'c', 'd'], [['a', 'b'], ['b', 'c'], ['c', 'd'], ['d', 'a']])
attacked_cycle = ArgumentationFramework(['a', 'b', 'c', 'd'], [['a', 'b'], ['b', 'c'], ['c', 'a'], ['d', 'a']])


class DGTerminationTests(unittest.TestCase):
    def test(self):
        pass


class DGArgSelectionTests(unittest.TestCase):
    def test(self):
        pass
    
    
class DGValidArgTests(unittest.TestCase):
    def test_self_attack(self):
        dg = DiscussionGame(self_attack_af)
        dg.in_.add('a')
        dg.find_valid_opp_arguments()
        
        expected = {'a'}
        actual = dg.valid
        
        self.assertCountEqual(expected, actual)
        
    def test_two_cycle(self):
        dg = DiscussionGame(two_cycle_af)
        dg.in_.add('a')
        dg.find_valid_opp_arguments()
        
        expected = {'b'}
        actual = dg.valid
        
        self.assertCountEqual(expected, actual)
        
    def test_odd_cycle1(self):
        dg = DiscussionGame(odd_cycle_af)
        dg.in_.add('a')
        dg.find_valid_opp_arguments()
        
        expected = {'b', 'c'}
        actual = dg.valid

        self.assertCountEqual(expected, actual)
        
    def test_odd_cycle2(self):
        dg = DiscussionGame(odd_cycle_af)
        dg.in_.add('a')
        dg.in_.add('b')
        dg.find_valid_opp_arguments()
        
        expected = {'a', 'b', 'c'}
        actual = dg.valid

        self.assertCountEqual(expected, actual)
        
    def test_four_cycle1(self):
        dg = DiscussionGame(four_cycle_af)
        dg.in_.add('a')
        dg.find_valid_opp_arguments()
        
        expected = {'b', 'd'}
        actual = dg.valid

        self.assertCountEqual(expected, actual)
        
    def test_four_cycle2(self):
        dg = DiscussionGame(four_cycle_af)
        dg.in_.add('a')
        dg.in_.add('c')
        dg.find_valid_opp_arguments()
        
        expected = {'b', 'd'}
        actual = dg.valid

        self.assertCountEqual(expected, actual)
        
    def test_four_cycle3(self):
        dg = DiscussionGame(four_cycle_af)
        dg.in_.add('a')
        dg.in_.add('b')
        dg.find_valid_opp_arguments()
        
        expected = {'a', 'b', 'c', 'd'}
        actual = dg.valid

        self.assertCountEqual(expected, actual)
        
    def test_attacked_cycle1(self):
        dg = DiscussionGame(attacked_cycle)
        dg.in_.add('a')
        dg.find_valid_opp_arguments()
        
        expected = {'b', 'c', 'd'}
        actual = dg.valid

        self.assertCountEqual(expected, actual)
        
    def test_attacked_cycle2(self):
        dg = DiscussionGame(attacked_cycle)
        dg.in_.add('d')
        dg.find_valid_opp_arguments()
        
        expected = {'a'}
        actual = dg.valid

        self.assertCountEqual(expected, actual)
        
    def test_attacked_cycle3(self):
        dg = DiscussionGame(attacked_cycle)
        dg.in_.add('b')
        dg.in_.add('d')
        dg.find_valid_opp_arguments()
        
        expected = {'a', 'c'}
        actual = dg.valid

        self.assertCountEqual(expected, actual)
        
    def test_attacked_cycle4(self):
        dg = DiscussionGame(attacked_cycle)
        dg.in_.add('a')
        dg.find_valid_opp_arguments()
        
        expected = {'b', 'c', 'd'}
        actual = dg.valid

        self.assertCountEqual(expected, actual)
    
    
if __name__ == "__main__":
    unittest.main()