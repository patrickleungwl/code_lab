
# name and qty of a component
#

class ComponentQty:
    def __init__(self,name,qty):
        self.name = name
        self.qty  = qty
        self.level = 0

    def name(self):
        return self.name
    
    def qty(self):
        return self.qty

    def set_level(self,lvl):
        self.level = lvl

    def level(self):
        return self.level


# Recipe
#
# Target ComponentQty with a list of
#   dependent ComponentQtys

class Recipe:
    def __init__(self,comp_qty):
        self.comp_qty  = comp_qty
        self.dependencies = []

    def target_comp(self):
        return self.comp_qty

    def set_target_comp_level(self,level):
        self.comp_qty.set_level(level)

    def add_dependent_component(self, comp_qty):
        self.dependencies.append(comp_qty)

    def dependent_components(self):
        return self.dependencies


# Clerk
#
# keeps a translation table- a recipe of component breakdowns
# keeps an inventory of assets
#

class Clerk:
    def __init__(self,recipe_file):
        self.max_level = 0
        self.recipes = {}
        self.component_level = {}
        self.read_recipes(recipe_file)
        self.rank_component_level()

    def get_component_level(self,target_comp):
        if target_comp.name in self.component_level:
            return self.component_level[target_comp.name]

        max_level = 1
        #print('Clerk top get_component_level %s' % target_comp.name)
        recipe = self.recipes[target_comp.name]
        for comp in recipe.dependent_components():
            cur_level = 0
            if comp.name == 'ORE':
                break
            #print(' Clerk get_component_level %s' % comp.name)
            cur_level = self.get_component_level(comp) + 1
            if cur_level > max_level:
                max_level = cur_level
        #print('Clerk top get_component_level %s return %i' % (target_comp.name, max_level))
        self.component_level[target_comp.name] = max_level
        return max_level

    def rank_component_level(self):
        self.max_level = 0
        for k in self.recipes.keys():
            comp_recipe = self.recipes[k]
            target_comp = comp_recipe.target_comp()
            level = self.get_component_level(target_comp)
            comp_recipe.set_target_comp_level(level)
            #print('Clerk rank_component_level %s %i\n' % (k, level))
            if level > self.max_level:
                self.max_level = level

    def max_level(self):
        return self.max_level

    def add_recipe(self,comp_name,recipe):
        self.recipes[comp_name] = recipe

    def translate_ComponentQty(self,txt):
        parts = txt.strip().split(' ')
        qty  = int(parts[0])
        name = parts[1]
        c = ComponentQty(name,qty)
        return c

    def show_recipes(self):
        for k in self.recipes.keys():
            r = self.recipes[k]
            self.show_recipe(r)

    def show_recipe(self,recipe):
        tc = recipe.target_comp()
        msg = 'show_recipe %s %i %i from' % (tc.name, tc.qty, tc.level)
        for c in recipe.dependent_components():
            msg += ' (%s %i)' % (c.name, c.qty)
        print(msg)

    def get_recipe(self,name):
        return self.recipes[name]

    def get_components(self,target_name,target_qty,convert_to_ores=False):
        # find the recipe for name
        recipe = self.recipes[target_name]
        required_components = []
        msg = 'Clerk: for (%s %i) require ' % (target_name, target_qty)

        # to make n number of targets, we need m number of these...
        for comp in recipe.dependent_components():
            # if convert to ores is True, so only convert to ores if True
            if comp.name == 'ORE':
                if convert_to_ores == False:
                    itself = ComponentQty(target_name,target_qty)
                    required_components.append(itself)
                    continue
            qty = 0
            total_comp_qty = 0
            while qty < target_qty:
                qty += recipe.target_comp().qty
                total_comp_qty += comp.qty 
            dep_comp = ComponentQty(comp.name, total_comp_qty)
            required_components.append(dep_comp)
            msg += ' (%s %i)' % (comp.name, total_comp_qty)

        #print(msg)
        return required_components


    def read_recipes(self,recipe_file):
        with open(recipe_file) as f:
            while True:
                line = f.readline().strip()
                if line == '':
                    break
                print(line.strip())
                # 7 A, 1 B => 1 C
                parts = line.strip().split('=>')
                sources_txt = parts[0]
                target_txt = parts[1]

                tc = self.translate_ComponentQty(target_txt)
                recipe = Recipe(tc)
                source_parts = sources_txt.split(',')
                for sp in source_parts:
                    sc = self.translate_ComponentQty(sp)
                    recipe.add_dependent_component(sc)
                self.add_recipe(tc.name,recipe)
        print()


# Fueler
# 
# Main job is to get components from Clerk to make FUEL.
# Given components from Clerk, keep drilling down components
# until only ORE remains.
#

class Fueler:
    def __init__(self,the_clerk):
        self.target = 'FUEL'
        self.clerk = the_clerk

    def print_components(self, msg, comps):
        for c in comps:
            msg += ' (%s %i)' % (c.name, c.qty)
        #print(msg)

    def get_components_stamp(self, comps):
        msg = ''
        for c in comps:
            msg += '%s%i' % (c.name, c.qty)
        return msg

    def aggregate_components(self, comps):
        aggregated_comps = []
        aggregated_names = {}

        for i in range(0,len(comps)):
            c = comps[i]
            if c.name in aggregated_names:
                continue
            target_name = c.name
            target_qty  = c.qty

            for j in range(i+1,len(comps)):
                d = comps[j]
                if d.name == target_name:
                    target_qty += d.qty

            acomp = ComponentQty(c.name, target_qty)
            aggregated_comps.append(acomp)
            aggregated_names[target_name] = 1
                
        return aggregated_comps


    def get_components(self,comp_name,comp_qty):
        print('Fueler getting components for %s %i' % (comp_name, comp_qty))
        comps = self.clerk.get_components(comp_name,comp_qty)

        max_level = self.clerk.max_level
        current_level = max_level-1
        while True:
            nextcomps = []
            #print('get_components level %i' % current_level)
            self.print_components('\nFueler to review', comps)
            comps = self.aggregate_components(comps)
            self.print_components('Fueler to review', comps)
            
            for c in comps:
                comp_level = self.clerk.get_component_level(c)
                if comp_level >= current_level:
                    #print('Fueler getting components for (%s %i)' % (c.name, c.qty))
                    newcomps = self.clerk.get_components(c.name, c.qty)
                    nextcomps.extend(newcomps)
                else:
                    # this comp is on a lower level which we won't
                    # drill down yet until we aggregate all instances
                    # of this component and then convert all at once
                    nextcomps.append(c)

            comps = nextcomps
            if current_level == 1:
                break
            current_level -= 1


        # do final conversion to OREs
        nextcomps = []
        self.print_components('\nFueler to convert to OREs', comps)
        for c in comps:
            print('Fueler getting components for (%s %i)' % (c.name, c.qty))
            newcomps = self.clerk.get_components(c.name, c.qty, True)
            nextcomps.extend(newcomps)
        comps = nextcomps

        msg = '\nFinal'
        tqty = 0
        for c in comps:
            msg += ' (%s %i)' % (c.name, c.qty)
            tqty += c.qty
        #print(msg)
        print(tqty)
        return tqty

target = ComponentQty('NZVS',5)
depdt = ComponentQty('ORE',157)
nr = Recipe(target)
nr.add_dependent_component(depdt)

# 44 XJWVT
# 5 KHKGT
# 1 QDVJ
# 29 NZVS
# 9 GPVTF
# 48 HKGWZ

target = ComponentQty('FUEL',1)
fr = Recipe(target)
d1 = ComponentQty('XJWVT',44)
d2 = ComponentQty('KHKGT',5)
d3 = ComponentQty('QDVJ',1)
d4 = ComponentQty('NZVS',29)
d5 = ComponentQty('GPVTF',9)
d6 = ComponentQty('HKGWZ',48)
fr.add_dependent_component(d1)
fr.add_dependent_component(d2)
fr.add_dependent_component(d3)
fr.add_dependent_component(d4)
fr.add_dependent_component(d5)
fr.add_dependent_component(d6)

# to get each batch of fr
target = fr.target_comp()
assert(target.name=='FUEL')
assert(target.qty==1)

dep = fr.dependent_components()
assert(len(dep)==6)
comp1 = dep[0]
assert(comp1.name=='XJWVT')
assert(comp1.qty==44)
comp2 = dep[1]
assert(comp2.name=='KHKGT')
assert(comp2.qty==5)
comp3 = dep[2]
assert(comp3.name=='QDVJ')
assert(comp3.qty==1)
comp4 = dep[3]
assert(comp4.name=='NZVS')
assert(comp4.qty==29)
comp5 = dep[4]
assert(comp5.name=='GPVTF')
assert(comp5.qty==9)
comp6 = dep[5]
assert(comp6.name=='HKGWZ')
assert(comp6.qty==48)


clerk = Clerk('input.txt')
clerk.show_recipes()
print('Clerk max level = %i' % clerk.max_level)

print('*************************')
f = Fueler(clerk)
print(f.get_components('FUEL',1))


