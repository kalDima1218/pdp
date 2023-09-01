from pow import binpow as binpow

def phi(n):
	i = 2
	mp = {}
	while i*i <= n:
		if n % i == 0:
			mp[i] = 0
		while n % i == 0:
			mp[i]+=1
			n//=i
		i+=1
	if n != 1:
		mp[n] = 1
	res = 1
	for i in mp:
		p = i
		n = mp[i]
		res*=binpow(p, n) - binpow(p, n-1)
	return res
