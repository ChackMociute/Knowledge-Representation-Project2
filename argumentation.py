class ArgumentationFramework:
    def __init__(self, arguments=None, attack_relations=None):
        self.args = dict() if arguments is None else arguments
        self.ar = list() if attack_relations is None else attack_relations
        self.find_extentions()
    
    def find_extentions(self):
        self.find_conflict_free()
        self.find_admissible()
    
    def find_conflict_free(self):
        # Helper functions
        def check_next_level(level):
            new_sets = set()
            for cf in level: extend_and_add_set(cf, new_sets)
            return new_sets
        
        def extend_and_add_set(cf, new_sets):
            for arg in set(self.args).difference(cf):
                new = cf.union(arg)
                if conflict_free(new):
                    new_sets.add(new)

        def conflict_free(set):
            return all([[a, b] not in self.ar for a in set for b in set])
        
        # Iteratively add new elements to existing cf sets
        self.cf = {frozenset()}
        level = self.cf
        while len(level) > 0:
            level = check_next_level(level)
            self.cf = self.cf.union(level)
    
    def find_admissible(self):
        def defended(set):
            attacked = [b for a, b in self.ar if a in set]
            return {e for e in self.args if defends(e, attacked)}

        def defends(item, attacked):
            for a, b in self.ar:
                if b == item and not a in attacked:
                    return False
            return True

        self.adm = {cf for cf in self.cf if cf.issubset(defended(cf))}


if __name__ == "__main__":
    import json

    # af = json.load(open('example-argumentation-framework.json'))
    af = json.load(open('slide-example.json'))
    
    print(ArgumentationFramework(arguments=af['Arguments'], attack_relations=af['Attack Relations']).cf)