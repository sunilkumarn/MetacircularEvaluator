import ops
from operator import *
dict={}
func_dict={}
local_dict={}

def opdet(dummy):
	"""Determines the operator"""
	if type(ops.last(dummy))==int:return opdet(ops.rest1(dummy))
	else:return ops.last(dummy)
		
def create_env(lists):
	"""Creates the global environement"""
	dict[lists[0]]=lists[1]

def create_localenv(lists):
	"""Creates the environement for the function"""
	func_dict[ops.first(ops.rest(lists))]=ops.rest(ops.rest(ops.rest1(ops.rest1(lists))))

def evaluate(lists,final):
	"""Performs arithmetic and logical operations"""
	if ops.null(lists):return final[0]
	elif ops.first(lists)=='(':return evaluate(ops.rest(lists),final)
	elif ops.first(lists).isdigit():return evaluate(ops.rest(lists),ops.append(final,[int(ops.first(lists))]))
	elif ops.first(lists)==')':
		op=opdet(final)
		if op=='+':f=add
		elif op=='*':f=mul
		elif op=='/':f=div
		elif op=='-':f=sub
		elif op=='%':f=mod
		elif op=='>':f=gt
		elif op=='and':f=and_
		elif op=='<':f=lt
		elif op=='=':f=eq
		result=ops.last(final)
		final=ops.rest1(final)
		while type(ops.last(final))==int:
			result=int(f(ops.last(final),result))
			final=ops.rest1(final)
		final=ops.rest1(final)
		return evaluate(ops.rest(lists),ops.append(final,[result]))
	else:return  evaluate(ops.rest(lists),ops.append(final,[ops.first(lists)]))

def eval_expr(dummy):
	"""Evaluates the expression in recursive functions"""
	reserve=[]
	for i in dummy:
		reserve.append(str(i))
	return evaluate(reserve,[])

def exec_func_body(func_body,passed):
	"""Executes the body of the function"""
	if ops.null(func_body):return str(evaluate(ops.rest(passed),[]))
	if ops.first(func_body).isalpha and ops.first(func_body) in local_dict:

		passed=ops.append(passed,[str(local_dict[ops.first(func_body)])])
		local_dict[ops.first(func_body)]=int(local_dict[ops.first(func_body)])-1
		return exec_func_body(ops.rest(func_body),passed)
	else:return exec_func_body(ops.rest(func_body),ops.append(passed,[ops.first(func_body)]))

def if_cons_alt(dummy,final,count):
	"""evaluates the consequent and alternative of an if condition"""
	if len(dummy)==2 and len(final)==0 and count==0:
		return dummy
	if ops.first(dummy)=='(':
		count+=1
		return if_cons_alt(ops.rest(dummy),ops.append(final,[ops.first(dummy)]),count)
	elif ops.first(dummy).isdigit():
		if len(final)!=0:return if_cons_alt(ops.rest(dummy),ops.append(final,[ops.first(dummy)]),count)
		else:return if_cons_alt(ops.append(ops.rest(dummy),[ops.first(dummy)]),final,count)
	elif ops.first(dummy).isalpha() and ops.first(dummy) in func_dict:
		count_func,func=0,[]
		dummy=ops.rest(dummy)
		for i in dummy: 
			if i=='(':
				func=ops.append(func,['('])
				count_func+=1
			elif i==')':
				count_func-=1
				func=ops.append(func,[')'])
				if count_func==0:
					break
			else:func=ops.append(func,[i])
			dummy=ops.rest(dummy)
		return if_cons_alt(ops.rest(dummy),ops.append(final,[exec_func_body(func,[])]),count)			

	elif ops.first(dummy).isalpha():return if_cons_alt(ops.rest(dummy),ops.append(final,[dict[ops.first(dummy)]]),count)
	elif ops.first(dummy)==')':
		count-=1
		if count >= 0:final=ops.append(final,[ops.first(dummy)])
	 	if count == 0:
			result=str(evaluate(final,[]))
			for i in dict:
				if i in local_dict:
					dict[i]=result
		 	return if_cons_alt(ops.append(ops.rest(dummy),[result]),[],count)

		else:
			if count<0:count=0
			return if_cons_alt(ops.rest(dummy),final,count)
	else:return if_cons_alt(ops.rest(dummy),ops.append(final,[ops.first(dummy)]),count)
	
def eval_if(lists,final,count):
	"""Evaluates the predicate of the 'if' condition"""
	if count==0 and len(final) != 0:
		expr,move=eval_expr(final),0
		for i in func_dict:
			if i in func_dict[i]:
				move=1
		if move==1:
			if expr==0:
				lists=if_cons_alt(ops.rest1(lists),[],0)
		else:lists=if_cons_alt(ops.rest1(lists),[],0)
		if expr==1:return lists[0],1
		else:return lists[1],0
	if ops.first(lists).isalpha():
		final=ops.append(final,[local_dict[ops.first(lists)]])
		return eval_if(ops.rest(lists),final,count)

	if ops.first(lists)=='(':
		count+=1
		return eval_if(ops.rest(lists),ops.append(final,[ops.first(lists)]),count)
	
	elif ops.first(lists)==')':
		    count=count-1
		    return eval_if(ops.rest(lists),ops.append(final,[ops.first(lists)]),count)
	else:return eval_if(ops.rest(lists),ops.append(final,[ops.first(lists)]),count)
def eval_define(lists):
	create_localenv(lists)
	
def evaluate_funcbody(dummy,lists):
	"""Evaluates the function body"""
	if ops.null(dummy):return lists
	if ops.first(dummy).isalpha():return evaluate_funcbody(ops.rest(dummy),ops.append(lists,[local_dict[ops.first(dummy)]]))
	else:return evaluate_funcbody(ops.rest(dummy),ops.append(lists,[ops.first(dummy)]))
	
def extract_funcbody(lists,finalbody,count):
	"""Extracts the body of the function"""
	if ops.first(lists)=='(':
		if ops.first(ops.rest(lists))=='if':
			count+=1
			return extract_funcbody(ops.rest(lists),ops.append(finalbody,[ops.first(lists)]),count)
		elif ops.first(ops.rest(lists)).isalpha():return extract_funcbody(ops.rest(lists),finalbody,count)
		else:
			count+=1
			return extract_funcbody(ops.rest(lists),ops.append(finalbody,[ops.first(lists)]),count)

	elif ops.first(lists).isalpha():
		if '(' not in finalbody:return extract_funcbody(ops.rest(lists),finalbody,count)
		else:return extract_funcbody(ops.rest(lists),ops.append(finalbody,[ops.first(lists)]),count)
	elif ops.first(lists)==')':
		if count>0:
		  count-=1
		  return extract_funcbody(ops.rest(lists),ops.append(finalbody,[ops.first(lists)]),count)
		if len(finalbody)!=0 and count==0:
			return finalbody
		else:return extract_funcbody(ops.rest(lists),finalbody,count)
	if ops.first(lists)=='if':return extract_funcbody(ops.rest(lists),ops.append(finalbody,[ops.first(lists)]),count)
	else:return extract_funcbody(ops.rest(lists),ops.append(finalbody,[ops.first(lists)]),count)

def exec_call(name,body):
	"""Starts the processing of the function """
	j=1
	for i in ops.rest(ops.rest(func_dict[name])):
		if i==')':
			break
		if i.isalpha():
			local_dict[i]=body[j]
			dict[i]=body[j]
			j+=1
	if '-' in body:	return evaluate(body,[])
	lists = extract_funcbody(func_dict[name],[],0)
	if 'if' in lists and name in func_dict[name]:
		check=0
		while check==0:retr,check=eval_if(ops.rest(ops.rest(lists)),[],0)
		else:
			for i in local_dict:
				if i in dict:
					return int(dict[i])
	elif 'if' in lists:
		retr,check=eval_if(ops.rest(ops.rest(lists)),[],0)
		return retr
	else:return evaluate(evaluate_funcbody(lists,[]),[])

def if_begin_eval(lists):
	"""Begins the execution of the if condition"""
	dup_list=ops.rest(ops.rest(lists))
	lists=[]
	for each in dup_list:
		if each.isalpha():
			lists.append(dict[each])
		else:
			lists.append(each)
	a,b=eval_if(lists,[],0)
	return int(a)

def from_env(lists):
	"""Retrieves value from the environement"""
	dup_list=lists
	lists=[]
	for each in dup_list:
		if each.isalpha():
			lists.append(dict[each])
		else:
			lists.append(each)
	return lists

def gravity(lists):
	"""Initial function for checking the current input"""
	if lists[1]=='if':return if_begin_eval(lists)
	elif lists[1]=='define' and lists[2]=='(':
			eval_define(ops.rest(ops.rest(lists)))
			return 'Environement created'
	elif lists[1]=='define':
			create_env(ops.rest(ops.rest(lists)))
			return 'Environement created '
	elif lists[1].isalpha() and lists[1] in func_dict:return exec_call(lists[1],ops.rest(ops.rest1(lists)))
	else:
			lists=from_env(lists)
			return evaluate(lists,[])

def main():
	try:
		while 1:
			print 'scheme>>>'
			i=raw_input()
			lists=i.split()
			print gravity(lists)
	except: 
		print 'END OF SESSION!!!'
if __name__ == '__main__':
	main()
