import os

check_list = [False for i in range(4460)]
for file_name in os.listdir("Scrape/Youtube/2_round/response"):
	if file_name == "failed_log":
		continue
	index = int(file_name.split(".")[0])
	check_list[index] = True

missing = False
for i in range(len(check_list)):
	if not check_list[i]:
		print("{} missing".format(i))
		missing = True

if not missing:
	print("no missing songs")
	
	
