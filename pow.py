def binpow_m(a, n, m):
	res = 1
	while n:
		if n % 2 == 1:
			res*=a
			res%=m
		a*=a
		a%=m
		n//=2
	return res

def binpow(a, n):
	res = 1
	while n:
		if n % 2 == 1:
			res*=a
		a*=a
		n//=2
	return res
