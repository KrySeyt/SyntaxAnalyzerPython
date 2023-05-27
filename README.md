# SyntaxAnalyzerPython
## Setup
1. Just run `main.py` with Python 3.11 or newer. Previous Python versions did not tested
2. Input any sequence that this grammar allows. Maybe `a+b-c*(a*b-c)` or just `a-b+c`

## Task
Create syntax analyzer for this grammar in any programming language. You can convert this grammar to an equivalent one
```console
S -> E_ENDOFSTRING	
E -> E+T | E-T | T		
T -> T*P | P		
P -> (E) | I		
I -> a | b | c

_ENDOFSTRING - end of input sequence
```

## Solution
Equivalent LL(1) grammar
```console
S -> TE_END
E -> +TE|-TE|EPSILON
T -> PD
D -> *T|EPSILON
P -> (TE)|I
I -> a|b|c

_END - end of input sequence
```
