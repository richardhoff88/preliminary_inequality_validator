# Mathbeaver Polynomial List Checker

A Python checker to automatically validate a list of polynomial inequalities by detecting contradictions using symbolic and SMT-based methods.

---

## Overview

This project takes a list of inequalities (as strings) and checks if they are consistent (i.e., whether there exists an assignment of real values to variables that makes them all true).  
It uses:
- Symbolic simplification (`Sympy`)
- SMT solvers (`Z3`)

---

## Example Input

```python
premises = [
    "(xz−2x−5z) > 0",
    "(4x+y+5) ≥ 0",
    "(3x(yz+5y+1)) ≥ 0",
    "(1) = 0",
    "(yz−4y+5z+3) > 0"
]
```

# Premise Checker Function and Correctness Proof

## Premise Checker Function Algorithm

Algorithm: check_premises
Input: A list of inequalities (string), $premise_str_list$
Output: Whether system is satisfiable or if a contradiction exists

Initialize Z3 Solver $solver$
Define Real variables $x, y, z$
$safe_eval_context \gets {x: x, y: y, z: z}$
For each $inequality$ in $premise_str_list$:

$normalized_inequality \gets$ Normalize($inequality$)
Try:

$smt_inequality \gets$ "(assert " + $normalized_inequality$ + ")"
$ineq \gets parse_smt2_string(smt_inequality)[0]$
$solver.add(ineq)$


Catch:

Try:

$ineq \gets eval(normalized_inequality, safe_eval_context)$
$solver.add(ineq)$


Catch:

Report error in reading inequality
Return






If $solver.check() == sat$:

Return "The premises has no contradictions"


Else:

Return "The premises is unsatisfiable and has contradictions"



Proof: Correctness of Premise Checker Function
Definitions
Definition 1: Let $S$ be the set of string inequalities that are the input to our check_premises function.
Definition 2: Let $P$ be the finite set of inequalities, where each inequality is a first-order logic formula involving real variables $x$, $y$, and $z$. This means that the inequalities do not have free variable occurrences and have well-defined truth values.
Definition 3: For this function we assume the Z3 module's functionality is correct and we can take the results from [Moura2008ProofsAR]. Let $Z$ be the Z3 solver instance.
Definition 4: Let $T$ be the transition function which takes each $s \in S$ and converts $s$ into its corresponding logical form $\in P$. This includes the hard-coded string replacements in the function for each $s$ as well as the parse_smt2_string and eval steps in check_premises. We assume $T(s)$ preserves the logic of $s$.
Definition 5: Z3($\Phi$) returns satisfiable if $\Phi$ is satisfiable and has no contradictions, and returns unsatisfiable if $\exists$ a contradiction.
Proof
First we initialize the Z3 solver instance.
For each $s \in S$, we feed $s$ to the transition function $T$, such that $T$ produces a normalized and SMT-LIB2-parsed string, where $T(s) \in P$.
$T(s)$ is then added as a constraint to the solver using solver.add().
Case 1: Z3(${T(s) | s \in S}$) returns satisfiable
This means $\exists$ an assignment of values to $x$, $y$, $z$ that makes all formulas $T(s)$ be true simultaneously.

By the definition of the SMT solver, if Z3 returns satisfiable, then there exists a model $M$ such that for all $s \in S$, $M \models T(s)$.
Since $T$ is meaning-preserving, if $M \models T(s)$, then $M \models s$, where $s$ is the original inequality.
Therefore, $M$ is a model for $P = {s \mid s \in S}$, and $P$ is satisfiable.
The function then outputs "The premises has no contradictions," which is the desired result.

Case 2: Z3(${T(s) | s \in S}$) returns unsatisfiable
This means $\exists$ no assignment of values to $x$, $y$, $z$ that makes all formulas $T(s)$ true simultaneously.

By the definition of the SMT solver, if Z3 returns unsatisfiable, then there is no model $M$ such that for all $s \in S$, $M \models T(s)$.
Since $T$ is meaning-preserving, there is no model $M$ such that for all $s \in S$, $M \models s$.
Therefore, $P = {s \mid s \in S}$ is unsatisfiable.
The function then prints "The premises is unsatisfiable and has contradictions," which is the desired result.

Conclusion:
The proof demonstrates that the check_premises function correctly determines the satisfiability of a set of inequalities, assuming the correctness of the Z3 SMT solver and the meaning-preservation of the translation function $T$.


