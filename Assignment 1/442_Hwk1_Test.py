import homework1_jch5769 as hw
import inspect

funlist = [x for x in inspect.getmembers(hw,inspect.isfunction)]
fundict2={}
booldict = {}

for x in funlist:
    fundict2[x[0]]=x[1]
    booldict[x[0]]=0

def test_case(func, inp, expected):
    fun_test = fundict2[func](inp)
    if fun_test == expected:
        print(f"Function {func} passd on test {expected} with answer {fun_test}")
        if booldict[func]==1:
            booldict[func]=1
        else:
            booldict[func]=2
    else:
        print(f"* Function {func} failed on test {expected} with answer {fun_test} *")
        booldict[func]=1

def all_clear_test(func):
    if booldict[func] == 0:
        print(f"* Function {func} has not been tested *\n")
    elif booldict[func]==1:
        print(f"* Function {func} has not passed all of its tests yet *\n")
    else:
        print(f"* Function {func} has passed all of its tests *\n")
        booldict[func]=2
    
def fun_check(booldict):
    for x in funlist:
        all_clear_test(x[0])

    print("-------------------------------------------------")
    not_pass = []
    not_test = []
    yes_pass = []
    for x in booldict:
        if booldict[x] == 0:
            not_test.append(x)
        if booldict[x] == 1:
            not_pass.append(x)
        if booldict[x] == 2:
            yes_pass.append(x)
    print("The following functions have not been tested:")
    for x in not_test:
        print(f"-> {x}")
    print("The following functions have passed all tests:")
    for x in yes_pass:
        print(f"-> {x}")
    print("The following functions have not passed all tests:")
    for x in not_pass:
        print(f"-> {x}")

    print("-------------------------------------------------")

############################################################
# Section 1: Working with Lists
############################################################

test_case("concatenate", [[1, 2], [3, 4]] , [1, 2, 3, 4])
test_case("concatenate", ["abc", (0, [0])] , ['a', 'b', 'c', 0, [0]])


test_case("transpose", [[1, 2, 3]] , [[1], [2], [3]])
test_case("transpose", [[1, 2], [3, 4], [5, 6]] , [[1, 3, 5], [2, 4, 6]])

############################################################
# Section 2: Sequence Slicing
############################################################

# assert list(prefixes([1, 2, 3])) == [[], [1], [1, 2], [1, 2, 3]]
# assert list(prefixes("abc")) == ['', 'a', 'ab', 'abc']

# assert list(suffixes([1, 2, 3])) == [[1, 2, 3], [2, 3], [3], []]
# assert list(suffixes("abc")) == ['abc', 'bc', 'c', '']

# assert list(slices([1, 2, 3])) == [[1], [1, 2], [1, 2, 3], [2], [2, 3], [3]]
# assert list(slices("abc")) == ['a', 'ab', 'abc', 'b', 'bc', 'c']


############################################################
# Section 4: Text Processing
############################################################

# assert normalize("This is an example.") == 'this is an example.'
# assert normalize("   EXTRA   SPACE   ") == 'extra space'

# assert no_vowels("This Is An Example.") == 'Ths s n xmpl.'
# assert no_vowels("We love Python!") == 'W lv Pythn!'

# assert digits_to_words("Zip Code: 19104") == 'one nine one zero four'
# assert digits_to_words("Pi is 3.1415...") == 'three one four one five'

############################################################
# Section 5: Polynomials
############################################################

# p, q = Polynomial([(2, 1), (1, 0)]), Polynomial([(2, 1), (-1, 0)])
# assert str(p) == '2x + 1'
# assert str(q) == '2x - 1'
# r = (p * p) + (q * q) - (p * q)
# assert str(r) == '4x^2 + 2x + 2x + 1 + 4x^2 - 2x - 2x + 1 - 4x^2 + 2x - 2x + 1'
# r.simplify()
# assert str(r) == '4x^2 + 3'
# assert [(x, r(x)) for x in range(-4, 5)] == [(-4, 67), (-3, 39), (-2, 19), (-1, 7), (0, 3), (1, 7), (2, 19), (3, 39), (4, 67)]

# p = Polynomial([(2, 1), (1, 0)])
# assert p.get_polynomial() == ((2, 1), (1, 0))

# p = Polynomial([(2, 1), (1, 0)])
# q = -p
# assert q.get_polynomial() == ((-2, 1), (-1, 0))

# p = Polynomial([(2, 1), (1, 0)])
# q = -(-p)
# assert q.get_polynomial() == ((2, 1), (1, 0))

# p = Polynomial([(2, 1), (1, 0)])
# q = p + p
# assert q.get_polynomial() == ((2, 1), (1, 0), (2, 1), (1, 0))

# p = Polynomial([(2, 1), (1, 0)])
# q = Polynomial([(4, 3), (3, 2)])
# r = p + q
# assert r.get_polynomial() == ((2, 1), (1, 0), (4, 3), (3, 2))

# p = Polynomial([(2, 1), (1, 0)])
# q = p - p
# assert q.get_polynomial() == ((2, 1), (1, 0), (-2, 1), (-1, 0))

# p = Polynomial([(2, 1), (1, 0)])
# q = Polynomial([(4, 3), (3, 2)])
# r = p - q
# assert r.get_polynomial() == ((2, 1), (1, 0), (-4, 3), (-3, 2))

# p = Polynomial([(2, 1), (1, 0)])
# q = p * p
# assert q.get_polynomial() == ((4, 2), (2, 1), (2, 1), (1, 0))

# p = Polynomial([(2, 1), (1, 0)])
# q = Polynomial([(4, 3), (3, 2)])
# r = p * q
# assert r.get_polynomial() == ((8, 4), (6, 3), (4, 3), (3, 2))

# p = Polynomial([(2, 1), (1, 0)])
# assert [p(x) for x in range(5)] == [1, 3, 5, 7, 9]

# p = Polynomial([(2, 1), (1, 0)])
# q = -(p * p) + p
# assert [q(x) for x in range(5)] == [0, -6, -20, -42, -72]

# p = Polynomial([(2, 1), (1, 0)])
# q = -p + (p * p)
# assert q.get_polynomial() == ((-2, 1), (-1, 0), (4, 2), (2, 1), (2, 1), (1, 0))
# q.simplify()

# assert q.get_polynomial() == ((4, 2), (2, 1))

# p = Polynomial([(2, 1), (1, 0)])
# q = p - p
# assert q.get_polynomial() == ((2, 1), (1, 0), (-2, 1), (-1, 0))

# q.simplify()
# assert q.get_polynomial() == ((0, 0),)

# p = Polynomial([(0, 1), (2, 3)])
# assert str(p) == '0x + 2x^3'
# assert str(p * p) == '0x^2 + 0x^4 + 0x^4 + 4x^6'
# assert str(-p * p) == '0x^2 + 0x^4 + 0x^4 - 4x^6'

# q = Polynomial([(1, 1), (2, 3)])
# assert str(q) == 'x + 2x^3'
# assert str(q * q) == 'x^2 + 2x^4 + 2x^4 + 4x^6'
# assert str(-q * q) == '-x^2 - 2x^4 - 2x^4 - 4x^6'

############################################################
# END OF TEST CASES
############################################################
fun_check(booldict)