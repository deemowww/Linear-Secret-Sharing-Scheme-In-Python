# A construction for Linear Secret Sharing Schemes(LSSS) and its solution in python
Create LSSS matrix from an access policy

Check if an attribute set satisfies an access policy by access tree

Calculate all w_i if the attribute set satisfies this policy

## TEST CASES
```
policy: (a1 and a2) or (a1 and a3 and a4) or (a4 and a5) or (a1 and a5)
attr_set: ['a1', 'a2', 'a3', 'a4', 'a5', 'a6']
matrix: 
[['a1' '1' '1' '0' '0' '0' '0']
 ['a2' '0' '1' '0' '0' '0' '0']
 ['a1' '1' '0' '1' '1' '0' '0']
 ['a3' '0' '0' '0' '1' '0' '0']
 ['a4' '0' '0' '1' '0' '0' '0']
 ['a4' '1' '0' '0' '0' '1' '0']
 ['a5' '0' '0' '0' '0' '1' '0']
 ['a1' '1' '0' '0' '0' '0' '1']
 ['a5' '0' '0' '0' '0' '0' '1']]
attr_path: [0, 1]
w_result: 
[[ 1.]
 [-1.]]

policy: (a1 and a2) or (a1 and a3 and a4) or (a4 and a5) or (a1 and a5)
attr_set: ['a1', 'a3', 'a4', 'a6']
matrix: 
[['a1' '1' '1' '0' '0' '0' '0']
 ['a2' '0' '1' '0' '0' '0' '0']
 ['a1' '1' '0' '1' '1' '0' '0']
 ['a3' '0' '0' '0' '1' '0' '0']
 ['a4' '0' '0' '1' '0' '0' '0']
 ['a4' '1' '0' '0' '0' '1' '0']
 ['a5' '0' '0' '0' '0' '1' '0']
 ['a1' '1' '0' '0' '0' '0' '1']
 ['a5' '0' '0' '0' '0' '0' '1']]
attr_path: [2, 3, 4]
w_result: 
[[ 1.]
 [-1.]
 [-1.]]

policy: a1 or a2 or a3 or a4 or a5
attr_set: ['a1', 'a2', 'a3', 'a4', 'a5', 'a6']
matrix: 
[['a1' '1']
 ['a2' '1']
 ['a3' '1']
 ['a4' '1']
 ['a5' '1']]
attr_path: [0]
w_result: 
[[1.]]

policy: a1 or a2 or a3 or a4 or a5
attr_set: ['a1', 'a3', 'a4', 'a6']
matrix: 
[['a1' '1']
 ['a2' '1']
 ['a3' '1']
 ['a4' '1']
 ['a5' '1']]
attr_path: [0]
w_result: 
[[1.]]

policy: a1 and a2 and a3 and a4 and a5 and a6
attr_set: ['a1', 'a2', 'a3', 'a4', 'a5', 'a6']
matrix: 
[['a1' '1' '1' '1' '1' '1' '1']
 ['a2' '0' '0' '0' '0' '0' '1']
 ['a3' '0' '0' '0' '0' '1' '0']
 ['a4' '0' '0' '0' '1' '0' '0']
 ['a5' '0' '0' '1' '0' '0' '0']
 ['a6' '0' '1' '0' '0' '0' '0']]
attr_path: [0, 1, 2, 3, 4, 5]
w_result: 
[[ 1.]
 [-1.]
 [-1.]
 [-1.]
 [-1.]
 [-1.]]

policy: a1 and a2 and a3 and a4 and a5 and a6
attr_set: ['a1', 'a3', 'a4', 'a6']
matrix: 
[['a1' '1' '1' '1' '1' '1' '1']
 ['a2' '0' '0' '0' '0' '0' '1']
 ['a3' '0' '0' '0' '0' '1' '0']
 ['a4' '0' '0' '0' '1' '0' '0']
 ['a5' '0' '0' '1' '0' '0' '0']
 ['a6' '0' '1' '0' '0' '0' '0']]
not matched

policy: ((a1 and a2) or (a1 and a3 and a4) or (a4 and a5) or (a1 and a5)) and a6
attr_set: ['a1', 'a2', 'a3', 'a4', 'a5', 'a6']
matrix: 
[['a1' '1' '1' '1' '0' '0' '0' '0']
 ['a2' '0' '0' '1' '0' '0' '0' '0']
 ['a1' '1' '1' '0' '1' '1' '0' '0']
 ['a3' '0' '0' '0' '0' '1' '0' '0']
 ['a4' '0' '0' '0' '1' '0' '0' '0']
 ['a4' '1' '1' '0' '0' '0' '1' '0']
 ['a5' '0' '0' '0' '0' '0' '1' '0']
 ['a1' '1' '1' '0' '0' '0' '0' '1']
 ['a5' '0' '0' '0' '0' '0' '0' '1']
 ['a6' '0' '1' '0' '0' '0' '0' '0']]
attr_path: [0, 1, 9]
w_result: 
[[ 1.]
 [-1.]
 [-1.]]

policy: ((a1 and a2) or (a1 and a3 and a4) or (a4 and a5) or (a1 and a5)) and a6
attr_set: ['a1', 'a3', 'a4', 'a6']
matrix: 
[['a1' '1' '1' '1' '0' '0' '0' '0']
 ['a2' '0' '0' '1' '0' '0' '0' '0']
 ['a1' '1' '1' '0' '1' '1' '0' '0']
 ['a3' '0' '0' '0' '0' '1' '0' '0']
 ['a4' '0' '0' '0' '1' '0' '0' '0']
 ['a4' '1' '1' '0' '0' '0' '1' '0']
 ['a5' '0' '0' '0' '0' '0' '1' '0']
 ['a1' '1' '1' '0' '0' '0' '0' '1']
 ['a5' '0' '0' '0' '0' '0' '0' '1']
 ['a6' '0' '1' '0' '0' '0' '0' '0']]
attr_path: [2, 3, 4, 9]
w_result: 
[[ 1.]
 [-1.]
 [-1.]
 [-1.]]
```