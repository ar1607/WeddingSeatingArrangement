import copy, random

def readFromFile(fname):
	inputArray=[]
	with open(fname) as f:
		inputArray = f.readlines()
	return inputArray

def outputToFile(fname, outputArray):
	with open(fname, 'w+') as file:
		file.write("yes\n")
		for i in range(1,people):
			file.write(str(i)+' '+str(outputArray[i])+'\n')
		file.write(str(people)+' '+str(outputArray[people]))

def outputNullToFile(fname):
	with open(fname, 'w+') as file:
		file.write("no")

def isNegation(literal):
	if literal[0]=='~':
		return True
	else:
		return False

def isUnitLiteral(literal):
	if len(literal)==1:
		return True
	return False

def isSentenceTrueInModel(model, sentence):
	for i in sentence:
		if isNegation(i):
			s = i[1:]
			if s in model:
				if model[s]==False:
					return True
			else:
				return None
		else:
			if i in model:
				if model[i]==True:
					return True
			else:
				return None
	return False

def isTrueInModel(clause, model):
	for i in clause:
		if isSentenceTrueInModel(model, i)==False:
			return False
		elif isSentenceTrueInModel(model, i)==None:
			return None
	return True

def updateModel(model, p, value):
	model[p]=value
	return model

def simplify(clause, p):
	if not isNegation(p):
		notP = '~'+p
	else:
		notP = p[1:]

	rem = []
	for i in clause:
		if i==p:
			rem.append(i)

	for i in clause:
		for j in i:
			if j==notP:
				i.remove(j)
			elif j==p:
				rem.append(i)

	while rem:
		xx = rem.pop(0)
		clause.remove(xx)
	return clause

def findPureSymbol(clause, symbols, model):
	posSymbols = set()
	negSymbols = set()

	for i in clause:
		if isSentenceTrueInModel(model, i):
			continue
		for j in i:
			if j[0]=='~':
				ss = j[1:]
				negSymbols.add(ss)
			else:
				posSymbols.add(j)

	for s in symbols:
		if s in posSymbols:
			posSymbols.remove(s)
		if s in negSymbols:
			negSymbols.remove(s)

	if len(posSymbols)==0 and len(negSymbols)==0:
		return None, None

	else:
		if len(posSymbols)>0:
			return posSymbols.pop(), True
		else:
			return negSymbols.pop(), False

def findUnitLiteral(clause, symbols, model):
	for i in clause:
		if isSentenceTrueInModel(model, i)==None:
		#if i not in model:
			a = None

			if isUnitLiteral(i):
				a = i[0]
			else:
				for j in i:
					if j not in model:
						if a==None:
							a = j
						else:
							a = None
							break
			if a!=None:
				if isNegation(a):
					return a, False
				else:
					return a, True
	return None, None
		

def dpll(clause, symbols, model):
	
	#STEP 1 : If all clauses are true for model, return True
	res = isTrueInModel(clause, model)
	if res == True:
		return True
	#STEP 2 : If some clause are false for model, return False
	elif res==False:
		return False
	
	#STEP 3 : Find pure symbols
	p,val = findPureSymbol(clause, symbols, model)
	#STEP 4 : if we get a pure symbol, then call dpll with update symbols and model
	if p:
		symbols.remove(p)
		model[p]=val
		return dpll(simplify(clause, p), symbols, model)

	#STEP 5 : Find unit literal
	p,val = findUnitLiteral(clause, symbols, model)
	#STEP 6 : If we get a unit literal, then call dpll with update symbols and model
	if p:
		ps = p
		if isNegation(p):
			ps = p[1:]
		symbols.remove(ps)
		model[ps]=val
		return dpll(simplify(clause, p), symbols, model)
	
	#STEP 7 : Pop from symbols
	p = symbols.pop(0)
	#STEP 8 : Return dpll with updates symbol and model
	if dpll(simplify(clause, p), symbols, updateModel(model, p, True)):
		return True
	else:
		return dpll(simplify(clause, p), symbols, updateModel(model, p, False))

def allPeopleAreFriends(inputArray):
	for i in inputArray:
		y = i.split()
		if y[2]!='F':
			return False
	return True

def main():
	global people, tableSize
	inputArray = readFromFile('input.txt') #CHANGES - change to Intput.txt
	x = inputArray[0].split()
	people = int(x[0])
	tableSize = int(x[1])
	inputArray.pop(0)
	
	if people==0 or tableSize==0:
		outputNullToFile('output.txt')
		return
	
	elif len(inputArray)==0 or ( tableSize>=1 and allPeopleAreFriends(inputArray)):
		res = {}
		for i in range(1,people+1):
			res[i]=1
		outputToFile('output.txt', res)
		return

	clause=[]
	symbols = []
	model={}

	#adding unary clauses for case A in assignment
	for i in range(1,people+1):
		sentence = []
		for j in range(1, tableSize+1):
			sentence.append('X'+str(i)+'_'+str(j))
			symbols.append('X'+str(i)+'_'+str(j))
			#model['X'+str(i)+str(j)] = None
		clause.append(sentence)

	#adding binary clauses for case A in assignment
	for i in range(1,people+1):
		for j in range(1, tableSize+1):
			for k in range(j+1,tableSize+1):
					sentence = ['~X'+str(i)+'_'+str(j),'~X'+str(i)+'_'+str(k)]
					clause.append(sentence)

	#adding clauses for cases B & C in the assignment
	for i in inputArray:
		y = i.split()
		if y[2]=='F':
			#adding clauses for case B in the assingment
			for a in range(1, tableSize+1):
				sentence = ['X'+str(y[0])+'_'+str(a),'~X'+str(y[1])+'_'+str(a)]
				clause.append(sentence)
				sentence = ['~X'+str(y[0])+'_'+str(a),'X'+str(y[1])+'_'+str(a)]
				clause.append(sentence)
		else:
			#adding clauses for case C in the assingment
			for a in range(1, tableSize+1):
				sentence = ['~X'+str(y[0])+'_'+str(a),'~X'+str(y[1])+'_'+str(a)]
				clause.append(sentence)

	pl = dpll(clause, symbols, model)

	if pl==False:
		outputNullToFile('output.txt')
	else:
		result = {}
		for key, value in model.iteritems():
			if value == True:
				counter = 1
				a = ''
				for j in range(1, len(key)):
					if key[j]=='_':
						counter+=1
						break
					else:
						a+=key[j]
						counter+=1
				a = int(a)		
				b = ''
				for x in range(counter,len(key)):
					b+=key[x]
				b = int(b)
				result[a]=b
		outputToFile('output.txt', result)
		return

main()