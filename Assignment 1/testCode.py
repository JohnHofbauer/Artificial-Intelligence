from homework1_jch5769 import *

############################################################
# Section 1: Working with Lists
############################################################

assert concatenate([[1, 2], [3, 4]]) == [1, 2, 3, 4]
assert concatenate(["abc", (0, [0])]) == ['a', 'b', 'c', 0, [0]]

assert transpose([[1, 2, 3]]) == [[1], [2], [3]]
assert transpose([[1, 2], [3, 4], [5, 6]]) == [[1, 3, 5], [2, 4, 6]]

############################################################
# Section 2: Sequence Slicing
############################################################

assert list(prefixes([1, 2, 3])) == [[], [1], [1, 2], [1, 2, 3]]
assert list(prefixes("abc")) == ['', 'a', 'ab', 'abc']

assert list(suffixes([1, 2, 3])) == [[1, 2, 3], [2, 3], [3], []]
assert list(suffixes("abc")) == ['abc', 'bc', 'c', '']

assert list(slices([1, 2, 3])) == [[1], [1, 2], [1, 2, 3], [2], [2, 3], [3]]
assert list(slices("abc")) == ['a', 'ab', 'abc', 'b', 'bc', 'c']


############################################################
# Section 4: Text Processing
############################################################

assert normalize("This is an example.") == 'this is an example.'
assert normalize("   EXTRA   SPACE   ") == 'extra space'

assert no_vowels("This Is An Example.") == 'Ths s n xmpl.'
assert no_vowels("We love Python!") == 'W lv Pythn!'

assert digits_to_words("Zip Code: 19104") == 'one nine one zero four'
assert digits_to_words("Pi is 3.1415...") == 'three one four one five'

############################################################
# Section 5: Polynomials
############################################################

p, q = Polynomial([(2, 1), (1, 0)]), Polynomial([(2, 1), (-1, 0)])
assert str(p) == '2x + 1'
assert str(q) == '2x - 1'
r = (p * p) + (q * q) - (p * q);
assert str(r) == '4x^2 + 2x + 2x + 1 + 4x^2 - 2x - 2x + 1 - 4x^2 + 2x - 2x + 1'
r.simplify();
assert str(r) == '4x^2 + 3'
assert [(x, r(x)) for x in range(-4, 5)] == [(-4, 67), (-3, 39), (-2, 19), (-1, 7), (0, 3), (1, 7), (2, 19), (3, 39), (4, 67)]

p = Polynomial([(2, 1), (1, 0)])
assert p.get_polynomial() == ((2, 1), (1, 0))

p = Polynomial([(2, 1), (1, 0)])
q = -p
assert q.get_polynomial() == ((-2, 1), (-1, 0))

p = Polynomial([(2, 1), (1, 0)])
q = -(-p)
assert q.get_polynomial() == ((2, 1), (1, 0))

p = Polynomial([(2, 1), (1, 0)])
q = p + p
assert q.get_polynomial() == ((2, 1), (1, 0), (2, 1), (1, 0))

p = Polynomial([(2, 1), (1, 0)])
q = Polynomial([(4, 3), (3, 2)])
r = p + q
assert r.get_polynomial() == ((2, 1), (1, 0), (4, 3), (3, 2))

p = Polynomial([(2, 1), (1, 0)])
q = p - p
assert q.get_polynomial() == ((2, 1), (1, 0), (-2, 1), (-1, 0))

p = Polynomial([(2, 1), (1, 0)])
q = Polynomial([(4, 3), (3, 2)])
r = p - q
assert r.get_polynomial() == ((2, 1), (1, 0), (-4, 3), (-3, 2))

p = Polynomial([(2, 1), (1, 0)])
q = p * p
assert q.get_polynomial() == ((4, 2), (2, 1), (2, 1), (1, 0))

p = Polynomial([(2, 1), (1, 0)])
q = Polynomial([(4, 3), (3, 2)])
r = p * q
assert r.get_polynomial() == ((8, 4), (6, 3), (4, 3), (3, 2))

p = Polynomial([(2, 1), (1, 0)])
assert [p(x) for x in range(5)] == [1, 3, 5, 7, 9]

p = Polynomial([(2, 1), (1, 0)])
q = -(p * p) + p
assert [q(x) for x in range(5)] == [0, -6, -20, -42, -72]

p = Polynomial([(2, 1), (1, 0)])
q = -p + (p * p)
assert q.get_polynomial() == ((-2, 1), (-1, 0), (4, 2), (2, 1), (2, 1), (1, 0))
q.simplify()

assert q.get_polynomial() == ((4, 2), (2, 1))

p = Polynomial([(2, 1), (1, 0)])
q = p - p
assert q.get_polynomial() == ((2, 1), (1, 0), (-2, 1), (-1, 0))

q.simplify()
assert q.get_polynomial() == ((0, 0),)

p = Polynomial([(0, 1), (2, 3)])
assert str(p) == '0x + 2x^3'
assert str(p * p) == '0x^2 + 0x^4 + 0x^4 + 4x^6'
assert str(-p * p) == '0x^2 + 0x^4 + 0x^4 - 4x^6'

q = Polynomial([(1, 1), (2, 3)])
assert str(q) == 'x + 2x^3'
assert str(q * q) == 'x^2 + 2x^4 + 2x^4 + 4x^6'
assert str(-q * q) == '-x^2 - 2x^4 - 2x^4 - 4x^6'

print("Congratulations, you're not completely retarded!!!")