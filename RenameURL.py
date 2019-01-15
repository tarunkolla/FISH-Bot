import re
with open('train2.from',"r", encoding="utf-8") as oldfile2, open('train.from', 'w',encoding="utf-8") as newfile2:
	for line in oldfile2:
		if "http" in line:
			line=re.sub(r"http\S+", r" newlinechar ", line) #replaces links with "URL"
			newfile2.write(line)
		else:
			newfile2.write(line)
newfile2.close()
print("Done!")