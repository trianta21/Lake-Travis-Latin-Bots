dat = [[["F","a","S","NOM"],["F","ae","P","NOM"],["F","ae","S","GEN"], ["F","ārum","P","GEN"],["F","ae","S","DAT"],["F","īs","P","DAT"],["F","am","S","ACC"],["F","ās","P","ACC"],["F","ā","S","ABL"],["F","īs","P","ABL"]],[["M","us","S","NOM"],["M","ī","P","NOM"],["M","ī","S","GEN"], ["M","ōrum","P","GEN"],["M","ō","S","DAT"],["M","īs","P","DAT"],["M","um","S","ACC"],["M","ōs","P","ACC"],["M","ō","S","ABL"],["M","īs","P","ABL"]],[["N","um","S","NOM"],["N","a","P","NOM"],["N","ī","S","GEN"], ["N","ōrum","P","GEN"],["N","ō","S","DAT"],["N","īs","P","DAT"],["N","um","S","ACC"],["N","a","P","ACC"],["N","ō","S","ABL"],["N","īs","P","ABL"]],[["M","","S","NOM"],["M","ēs","P","NOM"],["M","is","S","GEN"], ["M","um","P","GEN"],["M","ī","S","DAT"],["M","ibus","P","DAT"],["M","em","S","ACC"],["M","ēs","P","ACC"],["M","e","S","ABL"],["M","ibus","P","ABL"]],[["N","","S","NOM"],["N","a","P","NOM"],["N","is","S","GEN"], ["N","um","P","GEN"],["N","ī","S","DAT"],["N","ibus","P","DAT"],["N","","S","ACC"],["N","a","P","ACC"],["N","e","S","ABL"],["N","ibus","P","ABL"]],[["M","is","S","NOM"],["M","ēs","P","NOM"],["M","is","S","GEN"], ["M","ium","P","GEN"],["M","ī","S","DAT"],["M","ibus","P","DAT"],["M","em","S","ACC"],["M","ēs","P","ACC"],["M","e","S","ABL"],["M","ibus","P","ABL"]],[["N","e","S","NOM"],["N","ia","P","NOM"],["N","is","S","GEN"], ["N","ium","P","GEN"],["N","ī","S","DAT"],["N","ibus","P","DAT"],["N","e","S","ACC"],["N","ia","P","ACC"],["N","ī","S","ABL"],["N","ibus","P","ABL"]],[["M","us","S","NOM"],["M","ūs","P","NOM"],["M","ūs","S","GEN"], ["M","uum","P","GEN"],["M","uī","S","DAT"],["M","ibus","P","DAT"],["M","um","S","ACC"],["M","ūs","P","ACC"],["M","ū","S","ABL"],["M","ibus","P","ABL"]],[["N","ū","S","NOM"],["N","ua","P","NOM"],["N","ūs","S","GEN"], ["N","uum","P","GEN"],["N","ū","S","DAT"],["N","ibus","P","DAT"],["N","N","ū","S","ACC"],["N","ua","P","ACC"],["N","ū","S","ABL"],["N","ibus","P","ABL"]],[["F","ēs","S","NOM"],["F","ēs","P","NOM"],["F","eī","S","GEN"], ["F","ērum","P","GEN"],["F","eī","S","DAT"],["F","ēbus","P","DAT"],["F","em","S","ACC"],["F","ēs","P","ACC"],["F","ē","S","ABL"],["F","ēbus","P","ABL"]],[["M","ēs","S","NOM"],["M","ēs","P","NOM"],["M","ēī","S","GEN"], ["M","ērum","P","GEN"],["M","ēī","S","DAT"],["M","ēbus","P","DAT"],["M","em","S","ACC"],["M","ēs","P","ACC"],["M","ē","S","ABL"],["M","ēbus","P","ABL"]]]
print("NOUN ADJECTIVE 'BETTER THAN KATE' BOT V3\n\nSimply copy and paste the words in!\n")
def ranFunc (e):
	return len(e)
def endSor(word):
	dig4 = word[len(word)-4:]
	endlis = []
	for x in range(len(dat)):
   		for y in range(len(dat[x])):
   			if dat[x][y][1] in dig4:
   				endlis.append(dat[x][y][1])
	endlis.sort(reverse=True, key=ranFunc)
	return endlis[0]

def core(words):
	f = words[0:words.find(" ")]
	s = words[words.find(" ")+1:]
	fend = endSor(f)
	send = endSor(s)
	print("\n")
	fprop = []
	sprop = []
	for x in range(len(dat)):
		for y in range(len(dat[x])):
			if dat[x][y][1] == fend:
				fprop.append(dat[x][y])
			if dat[x][y][1] == send:
				sprop.append(dat[x][y])
	for x in range(len(fprop)):
		for y in range(len(sprop)):
			if (fprop[x][0]==sprop[y][0])&(fprop[x][2]==sprop[y][2])&(fprop[x][3]==sprop[y][3]):
				return("Yes")
	return("No")
while True:
	rawLis = input("Copy and paste words with a comma imbetween: ")
	fullLis = rawLis.split(",")
	for x in range(1,11):
		print("{0}. {1}".format(x, core(fullLis[x-1])))
	dec = input("\n\nWould you like to use again?(y/n) ")
	if dec == "y":
		print("\n")
	else:
		exit()