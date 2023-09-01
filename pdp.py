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

def obr(a, m):
	return binpow(a, phi(m)-1, m)

def obr_mods(a, mods):
	phi_m = 1
	m = 1
	for i in mods:
		phi_m*=i-1
		m*=i
	return binpow(a, phi_m-1, m)
	
def key_gen():
	pp = 567930029861#500000003
	qp = 618077191793#500000201
	p = 2 * pp + 1
	q = 2 * qp + 1
	n = p*q
	seed(time())
	a = randint(1, n)
	while gcd(a - 1, n) != 1 or gcd(a + 1, n) != 1:
		a = randint(1, n)
	g = (a ** 2) % n
	e = 65537
	d = obr_mods(e, [pp, qp])
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

main()
