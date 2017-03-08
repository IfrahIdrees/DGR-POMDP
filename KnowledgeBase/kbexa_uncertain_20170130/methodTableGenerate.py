import json
from pprint import pprint
with open('method.json') as method_file:
    method = json.load(method_file)

for x in method:
    pprint(x)
    

'''

with open("methodTable", 'a') as f:
    step_input = open("method.json", "r")
'''    
    
    
    
    
    
'''    


\begin{table}[ht]
\caption{Method \textit{clean-hand}} % title of Table
\centering % used for centering table
\begin{tabular}{c|c |c |c | c | c| c| c} % centered columns (4 columns)
%heading
\hline %inserts double horizontal lines
\multicolumn{4}{c |}{Precondition}&\multicolumn{4}{c}{Subtasks}\\ [0.5ex] % inserts table
\hline
Num. &Object&Attribute&Value&Num.&Name&Precedent&Decedent\\
\hline
1&hand-1&dirty&yes&1&use-soap&None&[rinse-hand]\\
2&hand-1&soapy&no&2&rinse-hand&[use-soap]&None\\
3&faucet-1&state&on&&&&\\
4&person-1&location&kitchen&&&&\\
5&person-1&ability&[$\geq$, 0, 0, 0]&&&&\\
\hline
\end{tabular}
\label{table:MCleanHand} % is used to refer this table in the text
\end{table}



'''
