str = "madam"

i = 0
def palidrome():
	last_index = len(str) - 1
	index = 0
	for i in str:
		if (i == last_index):
			break
		if (i == str[last_index]):
			last_index -= 1
		else:
			return (1)
		
if (palidrome() == 1):
	print("Word is not a Palindrome")
else:
	print("word is a Palindrome")	