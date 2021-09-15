#!/usr/bin/env python3

alphabet = 'abcdefghijklmnopqrstuvwxyz'

list = 'aaaba baabb aabab baaab aaaab babaa ababa aaaaa abbab aaaab aaaaa aabbb aaaaa baaba aaaaa aaaab aaaaa bbaaa abaaa'
encode = list.split(' ')

def tr(list):
	ans = []
	text = ''
	for item in encode:
		temp = ''
		for char in item:
			if char == 'a':
				temp += '0'
			else:
				temp += '1'

		ans.append(alphabet[int(temp, 2)])
	return text.join(ans).upper()

print(tr(list))
