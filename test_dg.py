import unittest
from argumentation import ArgumentationFramework
from discussion_game import DiscussionGame

self_attack_af = ArgumentationFramework(['a'], [['a', 'a']])
two_cycle_af = ArgumentationFramework(['a', 'b'], [['a', 'b'], ['b', 'a']])
odd_cycle_af = ArgumentationFramework(['a', 'b', 'c'], [['a', 'b'], ['b', 'c'], ['c', 'a']])
four_cycle_af = ArgumentationFramework(['a', 'b', 'c', 'd'], [['a', 'b'], ['b', 'c'], ['c', 'd'], ['d', 'a']])
attacked_cycle = ArgumentationFramework(['a', 'b', 'c', 'd'], [['a', 'b'], ['b', 'c'], ['c', 'a'], ['d', 'a']])

empty_af = ArgumentationFramework([], [])
disconnected_af = ArgumentationFramework(['a', 'b', 'c', 'd'], [['a', 'b'], ['c', 'd']])
single_argument_af = ArgumentationFramework(['a'], [])
mutual_attack_cycle_af = ArgumentationFramework(['a', 'b'], [['a', 'b'], ['b', 'a']]) # same as two cycle
complex_af = ArgumentationFramework(['a', 'b', 'c', 'd', 'e'], [['a', 'b'], ['b', 'c'], ['c', 'a'], ['c', 'd'], ['d', 'e'], ['e', 'c']])
incomplete_af = ArgumentationFramework(['a', 'b', 'c'], [['a', 'b']])


class DGTerminationTests(unittest.TestCase):
    def test_empty(self):
        dg = DiscussionGame(self_attack_af)
        self.assertFalse(dg.termination('a'))
        
    def test_self_attack(self):
        dg = DiscussionGame(self_attack_af)
        dg.in_.add('a')
        dg.last_opp_arg = 'a'
        dg.out.add('a')
        
        self.assertTrue(dg.termination(dg.select_arg()))
        self.assertTrue(dg.win)
        
    def test_two_cycle(self):
        dg = DiscussionGame(two_cycle_af)
        dg.in_.add('a')
        dg.last_opp_arg = 'b'
        dg.out.add('b')
        
        self.assertTrue(dg.termination(dg.select_arg()))
        self.assertFalse(dg.win)

    def test_empty_argumentation_framework(self):
        # works -> same as test_empty?
        dg = DiscussionGame(empty_af)
        
        self.assertIsNone(dg.select_arg())
        self.assertFalse(hasattr(dg, 'win'))

    
    def test_disconnected_framework(self):
        # kind of same as un attacked network
        # works

        dg = DiscussionGame(disconnected_af)
        dg.in_.add('a')
        dg.find_valid_opp_arguments()
        
        expected = {'b'}
        actual = dg.valid
        
        self.assertCountEqual(expected, actual)
        
        # Check if the game terminates without selecting any arguments
        self.assertTrue(dg.termination(None))

        # Ensure that the win state matches the termination condition
        if len(dg.in_.intersection(dg.out)) > 0:
            self.assertFalse(dg.win)  # Expecting no win if 'in_' intersects with 'out'
        else:
            self.assertTrue(dg.win)  # Expecting a win if 'in_' and 'out' have no intersection


    def test_single_argument_framework(self):
            # works
            dg = DiscussionGame(single_argument_af)
            dg.in_.add('a')
            dg.find_valid_opp_arguments()
            
            # Ensure the game terminates immediately without any argument selection
            self.assertTrue(dg.termination(None))
            self.assertTrue(dg.win)
    

    def test_mutual_attack_cycle(self): 
        # works 
        dg = DiscussionGame(mutual_attack_cycle_af)
        dg.in_.add('a')
        dg.last_opp_arg = 'b'
        dg.out.add('b')

        self.assertTrue(dg.termination(dg.select_arg()))
        self.assertFalse(dg.win)

    # DOES NOT WORK YET
    # def test_complex_argumentation(self): 
    #     dg = DiscussionGame(complex_af)
    #     dg.in_.add('a')
    #     dg.in_.add('d')
    #     dg.last_opp_arg = 'c'
    #     dg.out.add('c')

    #     # assumed termination should occur without win 
    #     # because of cyclic nature 
    #     self.assertTrue(dg.termination(dg.select_arg()))


    def test_incomplete_attack_relations(self): 
        dg = DiscussionGame(incomplete_af)
        dg.in_.add('a')
        dg.last_opp_arg = 'b'
        dg.out.add('b')

        # Test if the game handles the incomplete relation and terminates without an error
        self.assertTrue(dg.termination(dg.select_arg()))




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


class DGArgSelectionTests(unittest.TestCase):
    def test_self_attack(self):
        dg = DiscussionGame(self_attack_af)
        dg.last_opp_arg = 'a'
        dg.out.add('a')
        
        expected = 'a'
        actual = dg.select_arg()
        
        self.assertEqual(expected, actual)
        
    def test_two_cycle(self):
        dg = DiscussionGame(two_cycle_af)
        dg.last_opp_arg = 'a'
        dg.out.add('a')
        
        expected = 'b'
        actual = dg.select_arg()
        
        self.assertEqual(expected, actual)
        
    def test_odd_cycle(self):
        dg = DiscussionGame(odd_cycle_af)
        dg.last_opp_arg = 'a'
        dg.out.add('a')
        
        expected = {'b', 'c'}
        actual = dg.select_arg()
        
        self.assertTrue(actual in expected)
        
    def test_attacked_cycle(self):
        dg = DiscussionGame(attacked_cycle)
        dg.last_opp_arg = 'd'
        dg.out.add('d')
        
        self.assertIsNone(dg.select_arg())
    
    
if __name__ == "__main__":
    unittest.main()