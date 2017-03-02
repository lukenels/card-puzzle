import z3

hearts_8 = z3.Int('8 of Hearts')
diamonds_10 = z3.Int('10 of Diamonds')
club_king = z3.Int('King of Clubs')
spades_10 = z3.Int('10 of Spades')
diamonds_queen = z3.Int('Queen of Diamonds')

cards = [hearts_8, diamonds_10, club_king, spades_10, diamonds_queen]

s = z3.Solver()

# Each card must be in [1..5]
for card in cards:
    s.add(z3.And(card >= 1, card <= 5))

# No two cards can be in the same position
s.add(z3.Distinct(*cards))

def adjacent(a, b):
    return z3.Or(a - b == 1, b - a == 1)

# The diamonds are adjacent
s.add(adjacent(diamonds_10, diamonds_queen))

# The 10s are not adjacent
s.add(z3.Not(adjacent(diamonds_10, spades_10)))

# The 8 is somewhere above both 10s
s.add(z3.And(hearts_8 < diamonds_10, hearts_8 < spades_10))

# The heart is not on top
s.add(hearts_8 != 1)

# The spade is not on bottom
s.add(spades_10 != 5)


sols = 0
while s.check() == z3.sat:
    sols += 1
    model = s.model()
    cards.sort(key=lambda c: model.eval(c).as_long())
    print cards
    s.add(z3.Or(*map(lambda c: c != model.eval(c), cards)))
print "{} Solution(s).".format(sols)