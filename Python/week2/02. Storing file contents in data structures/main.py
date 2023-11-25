import random

def read_file(f):
	f_content = f.read()
	# print(f_content)
	return f_content.split('\n')

def main():
	f_name = input("Enter a file name: ")
	try:
		f = open(f_name, "r")
	except FileNotFoundError as exp:
		print("No such file or directory")
		return -1
	except Exception as exp:
		print(exp, "Something Went wrong!")
		return -1
	f_content_list = read_file(f)
	f.close()
	print(random.choice(f_content_list))
main()