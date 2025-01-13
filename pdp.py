from math import gcd, sqrt
from random import randint, seed
from time import time
from phi import phi
from pow import binpow_m as binpow

class secret_key:
	def __init__(self, e, d):
		self.e = e
		self.d = d

class public_key:
	def __init__(self, n, g):
		self.n = n
		self.g = g

class file:
	def __init__(self, message, tags, pk):
		self.message = message
		self.tags = tags
		self.pk = pk

class challenge:
	def __init__(self, i, q_len, k1, k2):
		self.i = i
		self.q_len = q_len
		self.k1 = k1
		self.k2 = k2

class proof:
	def __init__(self, t, p):
		self.t = t
		self.p = p

class client:
	def __init__(self):
		self.pk, self.sk = key_gen()
	def new_file(self):
		message = [randint(0, 2**128) for _ in range(randint(1, 10**3))]
		tags = [tag_block(i, self.pk, self.sk) for i in message]
		self.len = len(message)
		return file(message, tags, self.pk)
	def store_index(self, i):
		self.i = i
	def new_challenge(self):
		return challenge(self.i, randint(1, self.len), randint(0, 2**1024), randint(0, 2**1024))
	def verify(self, prf):
		t, p = check_proof(prf.t, prf.p, self.pk, self.sk)
		return t == p

class server:
	def __init__(self):
		self.files = []
	def add(self, file):
		self.files.append(file)
		return len(self.files)-1
	def proof(self, chal):
		t, p = gen_proof(self.files[chal.i].tags, self.files[chal.i].message, chal.q_len, chal.k1, chal.k2, self.files[chal.i].pk)
		return proof(t, p)

def inv(a, m):
	return binpow(a, phi(m)-1, m)

def inv_mods(a, mods):
	phi_m = 1
	m = 1
	for i in mods:
		phi_m*=i-1
		m*=i
	return binpow(a, phi_m-1, m)
	
def key_gen():
	pp = 567930029861
	qp = 618077191793
	p = 2 * pp + 1
	q = 2 * qp + 1
	n = p*q
	seed(time())
	a = randint(1, n)
	while gcd(a - 1, n) != 1 or gcd(a + 1, n) != 1:
		a = randint(1, n)
	g = (a ** 2) % n
	e = 65537
	d = inv_mods(e, [pp, qp])
	pk = public_key(n, g)
	sk = secret_key(e, d)
	return pk, sk

def tag_block(m, pk, sk):
	return binpow(pk.g, m*sk.e, pk.n)

def gen_proof(tags, message, q_len, k1, k2, pk):
	t = 1
	p = 1
	seed(k1)
	idx = []
	for i in range(q_len):
		idx.append(randint(0, len(message)-1))
	seed(k2)
	for i in idx:
		a = randint(1, 2**128)
		t*=binpow(tags[i], a, pk.n)
		t%=pk.n
	seed(k2)
	for i in idx:
		a = randint(1, 2**128)
		p*=binpow(pk.g, a*message[i], pk.n)
		p%=pk.n
	return t, p

def check_proof(t, p, pk, sk):
	return binpow(t, sk.d, pk.n), p

def main():
	pk, sk = key_gen()
	print(pk.n, pk.g, sk.e, sk.d)
	message = [randint(0, 2**128) for _ in range(10**3)]
	tags = [tag_block(i, pk, sk) for i in message]
	k1 = 1
	k2 = 2
	q_len = int(sqrt(len(message)))
	t, p = gen_proof(tags, message, q_len, k1, k2, pk)
	print(check_proof(t, p, pk, sk))

def test():
	c = client()
	s = server()
	c.store_index(s.add(c.new_file()))
	print(c.verify(s.proof(c.new_challenge())))

def multi_test():
	c = [client() for _ in range(10)]
	s = server()
	for i in range(len(c)):
		c[i].store_index(s.add(c[i].new_file()))
	for i in range(len(c)):
		print(c[i].verify(s.proof(c[i].new_challenge())))

main()
#test()
#multi_test()
