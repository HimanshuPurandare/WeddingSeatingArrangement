import copy, random, operator, time
from collections import OrderedDict

iparr = []
iparr = [None for x in range(2)]
enem = []
frnd = []
clauses = []
clause_walksat = []
new = []
runPLAlgo = True
stringtobeappendedintothefile = ""

def readInput():
	global iparr
	global enem
	global frnd
	global runPLAlgo
	fname="input.txt"

	with open(fname) as f:
		content=f.readlines()
		
	content=[x.strip() for x in content]
	lineno = 0
	enemlines = 0
	for x in content:
		x = x.rstrip()
		if lineno==0:
			iparr = map(int, x.split())
		elif x.endswith("F"):
			temp = x.split()
			frnd.append([int(temp[0]),int(temp[1])])
		elif x.endswith("E"):
			enemlines += 1
			temp = x.split()
			enem.append([int(temp[0]),int(temp[1])])
		lineno+=1
	enemlines = len(enem)
	for n in range(2,90):
		perm = 0
		perm = (n)*(n-1)
		if enemlines >= 1 and iparr[1] == 1:
			runPLAlgo = False
			break
		else:
			if perm >= (enemlines * 2):
				if perm == (enemlines * 2):
					if n <= iparr[1]:
						runPLAlgo = False
						break
				elif (n-1) <= iparr[1]:
					runPLAlgo = False
					break

def createInitialClauses():
	global iparr
	global enem
	global frnd
	global clauses
	global clause_walksat
	temp = []
	if iparr[0] != None:
		for person in range(1, iparr[0]+1):
			temp = []
			for table in range(1, iparr[1]+1):
				temp.append('x'+str(person)+"-"+str(table))
			clauses.append(temp)
		for person in range(1, iparr[0]+1):
			temp = []
			for i in range(1, iparr[1]+1):
				for j in range(i+1, iparr[1]+1):
					temp.append('~x'+str(person)+"-"+str(i))
					temp.append('~x'+str(person)+"-"+str(j))
					clauses.append(temp)
					temp = []
		for pair in frnd:
			temp = []
			for i in range(1, iparr[1]+1):
				for j in range(1, iparr[1]+1):
					if i != j:
						temp.append('~x'+str(pair[0])+"-"+str(i))
						temp.append('~x'+str(pair[1])+"-"+str(j))
						clauses.append(temp)
						temp=[]
		for pair in enem:
			temp = []
			for i in range(1, iparr[1]+1):
				temp.append('~x'+str(pair[0])+"-"+str(i))
				temp.append('~x'+str(pair[1])+"-"+str(i))
				clauses.append(temp)
				temp=[]
				
		clause_walksat = copy.deepcopy(clauses)

def	resolve(Ci, Cj):
	resolvents = []
	temp = []
	tempCi = []
	tempCj = []
	isTautology = False
	for literal in Ci:
		temp = []
		if literal.startswith("~"):
			lit = literal[1:]
		else:
			lit = "~"+literal
		if lit in Cj:
			tempCi = [x for x in Ci if x != literal]
			tempCj = [x for x in Cj if x != lit]
			temp = tempCi + tempCj
			temp = list(set(temp))
			for l in temp:
				lit = ""
				if l.startswith("~"):
					lit = l[1:]
				else:
					lit = "~"+l
				if lit in temp:
					isTautology = True
					break
			if not isTautology:
				resolvents.append(temp)
		else:
			temp = []

	return resolvents

def pl_resolution():
	tout = time.time() + 36
	global new
	global clauses
	resolvents = []
	while True:
		for i in range(len(clauses)):
			for j in range(i+1, len(clauses)):
				if time.time() > tout:
					return True
				resolvents = []
				resolvents = resolve(clauses[i], clauses[j])
				for newclauses in resolvents:
					if not newclauses:
						return False
				new = [list(x) for x in set(tuple(x) for x in new)]+[list(x) for x in set(tuple(x) for x in resolvents)]
		if set(tuple(x) for x in new).issubset(set(tuple(x) for x in clauses)):
			return True
		clauses = [list(x) for x in set(tuple(x) for x in new)]+[list(x) for x in set(tuple(x) for x in clauses)]
		new = []

def check_for_sol(clause, model):
	for literal in clause:
		if literal[0] == "~":
			if model[literal[1:]] == False:
				return True
		else:
			if model[literal] == True:
				return True
	return False

def ret_symbols(clause):
	literals = []
	for literal in clause:
		literals.append(literal[1:] if literal.startswith('~') else literal)
	return literals

def walksat(wlkcl, p=0.5, max_flips = 40000):
	walksat_model = {}
	if iparr[0] != None:
		for person in range(1,iparr[0]+1):
			for table in range(1,iparr[1]+1):
				walksat_model['x'+str(person)+"-"+str(table)] = bool(random.getrandbits(1))

		for i in range(max_flips):
			satisfied, unsatisfied = [], []
			for clause in wlkcl:
				(satisfied if check_for_sol(clause, walksat_model) else unsatisfied).append(clause)
			if not unsatisfied:
				return walksat_model
			clau = random.choice(unsatisfied)
			if random.uniform(0.0,1.0) < 0.5:
				sym = random.choice(ret_symbols(clau))
			else:
				#flip whichever symbol in clause maximizes the number of satisfied clauses
				maxclausesatisfied = {}
				symlist = []
				symlist = ret_symbols(clau)
				
				for lit in symlist:
					newmod = []
					newmod = copy.deepcopy(walksat_model)
					newmod[lit] = not newmod[lit]
					counter = 0
					for tempclause in wlkcl:
						if check_for_sol(tempclause, newmod) == True:
							counter += 1
					maxclausesatisfied[lit] = counter	
				sym = max(maxclausesatisfied.iteritems(), key=operator.itemgetter(1))[0]
				
			walksat_model[sym] = not walksat_model[sym]
		return None

def main():
	global clause_walksat
	global stringtobeappendedintothefile
	readInput()
	
	if iparr[0] == 0:
		stringtobeappendedintothefile = "yes"
	elif iparr[1] == 0:
		stringtobeappendedintothefile = "no"
	elif iparr[0] == None:
		stringtobeappendedintothefile = ""
	else:
		createInitialClauses()
		dict1 = []
		listtobeprinted = []
		dict2 = {}
		if iparr[1] == 2:
			op = pl_resolution()
			if op:
				stringtobeappendedintothefile = stringtobeappendedintothefile + "yes\n"
				dict1 = walksat(clause_walksat)
				if dict1 == None:
					stringtobeappendedintothefile = "no\n"
			else:
				stringtobeappendedintothefile = stringtobeappendedintothefile + "no\n"
		else:
			if runPLAlgo:
				op = pl_resolution()
				if op:
					stringtobeappendedintothefile = stringtobeappendedintothefile + "yes\n"
					dict1 = walksat(clause_walksat)
					if dict1 == None:
						stringtobeappendedintothefile = "no\n"
				else:
					stringtobeappendedintothefile = stringtobeappendedintothefile + "no\n"
			elif len(enem) == 1 and iparr[1] == 1:
				stringtobeappendedintothefile += "no\n"
			else:
				stringtobeappendedintothefile += "yes\n"
				dict1 = walksat(clause_walksat)
				if dict1 == None:
					stringtobeappendedintothefile = "no\n"

		if dict1 != None:
			for item in dict1:
				if dict1[item] == True:
					listtobeprinted.append(item[1:])
			for it in listtobeprinted:
				dict2[int(it.split("-")[0])] = int(it.split("-")[1])
			#print dict2

			od = OrderedDict(sorted(dict2.items()))
			for i in od:
				stringtobeappendedintothefile += str(i)+" "+str(od[i])+"\n"
		stringtobeappendedintothefile = stringtobeappendedintothefile.rstrip()

	filename = "output.txt"
	with open(filename, "w+") as f:
		f.write(stringtobeappendedintothefile)

main()
