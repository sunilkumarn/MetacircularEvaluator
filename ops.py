
def first(a):
	return a[0]

def rest(a):
	return a[1:]

def last(a):
	return a[-1]

def rest1(a):
	return a[:-1]

def null(a):
	return len(a) == 0

def cons(item, a):
	return [item] + a

def append(a, b):
	return a + b

def check(a,b):
	if null(a):
		return 0
	elif b==first(a):
	 	return 1
	else:
	 	return check(rest(a),b)

def app(a,b):
	if null(a) :
	 	return b
	else:
	 	return cons(first(a),app(rest(a),b))

def rev(a):
	if null(a):
		return a
	else:return append(rev(rest(a)),[(first(a))])

def inter(a,b):
	if null(a):
		return []
	elif (first(a)) in b:
	 	return cons(first(a),inter((rest(a)),b))
	else:
		return inter((rest(a)),b)

def flat(a):

	if null(a):
		return []
	elif type(first(a))==list:
	 	return append(flat(first(a)),flat(rest(a)))
 	else:
		return append([first(a)],flat(rest(a)))

def maxim(a):
	if rest(a)==[]:
		return a
	elif first(a)<first(rest(a)):
		return maxim(rest(a))
	else:
		return maxim(append([first(a)],rest(rest(a))))




