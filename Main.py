import sys
Horn_Clauses = []
elements = []
true_elements = []
answers = []
KB = []


class Clause:
    def __init__(self, count, head, children):
        self.count = count
        self.head = head
        self.children = children



def tt_entails(knowledge_base, alphaValue):
    symbols_list = []
    #to pass empty model
    model = None

    alpha = alphaValue

    #to create the Knowledge Base Sentence
    KBS = ""
    j = 1
    #The following loop is to create the knowledge base sentence and to create symbols list
    for clause in knowledge_base:
        if "=>" in clause:
            KBS =  KBS + "(not "
            ele = clause.rsplit("=>")
            if ele[1].strip() not in symbols_list:
                symbols_list.append(ele[1].strip())

            if "&" in ele[0]:
                av = ele[0].rsplit("&") 
                i = 1 
                KBS = KBS + '(' 
                for c in av:
                    
                    if c.strip() not in symbols_list:
                        symbols_list.append(c.strip())
                    if(i != len(av)):
                        KBS = KBS + c.strip() +' and '
                    else:
                        KBS = KBS + c.strip() + ') ' + ' or ' + ele[1].strip() + ") "
 
                    i += 1
                
            else:
                if ele[0].strip() not in symbols_list:
                    symbols_list.append(ele[0].strip())
                KBS = KBS + ele[0].strip() + ' or ' + ele[1].strip() + ") "
 
        else:
            if clause.strip() not in symbols_list:
                symbols_list.append(clause.strip())
            KBS = KBS + clause.strip()

        if(j != len(knowledge_base)):
            KBS = KBS + ' and '

        j += 1
    #Call tt_check_all function 
    return tt_check_all(KBS, alpha, symbols_list, model)


def tt_check_all(kb_sentence, query_sentence, symbols_list, model):
    # if length of symbol list is empty check kb_sentence
    if len(symbols_list) == 0:

        # if KB is true and Aplha is true add True to Answers and returns answers
        if eval(kb_sentence) == True:
            if eval(query_sentence) is True: 
                answers.append(True)
            return answers
        # else add False to answers and returns answers
        else:
            answers.append(False)
            return answers
    else:
        copy_list = list(symbols_list)
        symbol = copy_list.pop(0)
        #string is turn to Varible and assign true
        globals()[symbol] = True
        #Pass true value
        true_model = tt_check_all(kb_sentence, query_sentence, copy_list,  globals()[symbol])
      
        #string is turn to variable and assign false
        globals()[symbol] = False
        #Pass false value
        false_model = tt_check_all(kb_sentence, query_sentence, copy_list,  globals()[symbol])

        #return answer
        return answers


def extractClause(Horn_clauses):
    for clause in Horn_Clauses:
        #if => is in the clause it is split has head and children
        if "=>" in clause:
            ele = clause.rsplit("=>")
            #if & in children, the children are split
            if "&" in ele[0]:
                av = ele[0].rsplit("&")
                children = []
                for c in av:
                    #for each child av, add to Children list
                    children.append(c.strip())
                #then create a clause using the extracted information
                cls = Clause(2,ele[1].strip(), children)
                KB.append(cls)                
            else:
                cls = Clause(1,ele[1].strip(),[ele[0].strip()])
                KB.append(cls)
   
    return KB




def foward_chaining(Horn_Clauses, alpha):
    inferred = {} #inferred[s] initially false all s
    Agenda = [] #init with symbols that are true
    answer = [] #Answers are addd to this list
    q = alpha
    for c in Horn_Clauses:
        if "=>" not in c:
            if c.strip() not in Agenda:
                #true values are added to Agenda
                Agenda.append(c.strip())
                #since they haven't been checked yet, False
                inferred[c.strip()] = False

    #Call extract method function extract horn_clauses as Clauses objects
    KB = extractClause(Horn_Clauses)
    for clause in KB:
        #since none of the head or children have been checked initialise them as False
        inferred[clause.head] = False
        for child in clause.children:
            inferred[child] = False

    while len(Agenda) != 0:
        #check true values 
        p =  Agenda.pop(0)
        if p not in answer:
            answer.append(p)
        #if p is alpha end method and returen answer
        if p == q:
            return answer
        #if p has not been checked mark it as checked
        if inferred[p] == False:
            inferred[p] = True

            #Reduce count 
            for clause in KB:
                if p in clause.children:
                    clause.count -= 1   

            #if count is zero, it becomes true and added to agenda
            for clause in KB:
                if clause.count == 0:
                    Agenda.append(clause.head)



def backward_chaining(Horn_Clauses, alpha):
    inferred = {} #inferred[s] initially false all s
    Agenda = [] #init with symbols that are true
    answer = []
    check = []
    q = alpha
    for c in Horn_Clauses:
        if "=>" not in c:
            if c.strip() not in Agenda:
                Agenda.append(c.strip())
                inferred[c.strip()] = False
    #Extract clauses using extract_clause method
    KB = extractClause(Horn_Clauses)
    for clause in KB:
        inferred[clause.head] = False
        for child in clause.children:
            inferred[child] = False
    check.append(q)

    while len(Agenda) != 0:
        #if no children or no answer return none
        if(len(check)== 0):
            return None
        p =  check.pop(0)
    
        if p not in answer:
            answer.append(p)
        #if p true, break loop and return answer
        if p in Agenda:
            answer_inorder = []
            while len(answer) != 0:
                a = answer.pop(-1)
                answer_inorder.append(a)
            return answer_inorder
        #if not checked, mark as check
        if inferred[p] == False:
            inferred[p] = True
            for clause in KB:
                if p in clause.head:
                    for child in clause.children:
                        check.append(child)
        

#Open the file typed in the command line
with open(sys.argv[2]) as f:
    #Read the first line 
    lineTell = f.readline().strip("\n")
    #If Line read is TELL read the next line and split values by ;
    if(str(lineTell) == "TELL"):
        line1 = f.readline().split(';')
        #for each split value add it to Horn_Clause list 
        for l in line1:
            Horn_Clauses.append(l)
        Horn_Clauses.pop()
    #Read the nect line
    lineAsk = f.readline().strip("\n")
    #if the line read is ASK, assign the next line value to alpha
    if(lineAsk == "ASK"):
       alpha = f.readline()


#Method read from the cmd
search  = sys.argv[1]

#if method is Foward chaining run Foward chaining method
if(search == "FC"):
    answer = foward_chaining(Horn_Clauses, alpha)
    if(answer != None):
        print("Yes: " + str(answer))
    else:
        print("No")
#if method is Backward chaining run Backward chaining method
elif(search == "BC"):
    answer = backward_chaining(Horn_Clauses, alpha)
    if(answer != None):
        print("Yes: " + str(answer))
    else:
        print("No")
#if method is Truth Table, run Truth table method
elif(search == "TT"):
    answers = tt_entails(Horn_Clauses, alpha)
    count = 0
    for a in answers:
        #Count the True values in the answer list
        if a == True:
            count += 1

    if(True in answers):
        print("Yes: " + str(count))
    else:
        print("No")
#If method is wrong
else:
    print("Wrong Input")