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

## 📌 Premise Checker Function Algorithm

```latex
\subsection{Premise checker function algorithm}

\begin{algorithm}[H]
\caption{check\_premises}
\begin{algorithmic}[1]
\Require A list of inequalities (string), $premise\_str\_list$
\Ensure Whether system is satisfiable or if a contradiction exists

\State Initialize Z3 Solver $solver$
\State Define Real variables $x, y, z$
\State $safe\_eval\_context \gets \{x: x, y: y, z: z\}$

\For{each $inequality$ in $premise\_str\_list$}
    \State $normalized\_inequality \gets$ Normalize($inequality$)
    \Try
        \State $smt\_inequality \gets$ "(assert " + $normalized\_inequality$ + ")"
        \State $ineq \gets parse\_smt2\_string(smt\_inequality)[0]$
        \State $solver.add(ineq)$
    \Catch
        \Try
            \State $ineq \gets eval(normalized\_inequality, safe\_eval\_context)$
            \State $solver.add(ineq)$
        \Catch
            \State Report error in reading inequality
            \State \Return
        \EndTry
    \EndTry
\EndFor

\If{$solver.check() == sat$}
    \State \Return "The premises has no contradictions"
\Else
    \State \Return "The premises is unsatisfiable and has contradictions"
\EndIf

\end{algorithmic}
\end{algorithm}

\subsection{Proof: correctness of premise checker function}

\theoremstyle{definition}
\newtheorem{definition}{Definition}[section]

\begin{definition}
    Let $S$ be the set of string inequalities that are the input to our \texttt{check\_premises} function.
\end{definition}
\begin{definition}
    Let $P$ be the finite set of inequalities, where each inequality is a first-order logic formula involving real variables $x$, $y$, and $z$. This means that the inequalities do not have free variable occurrences and have well-defined truth values.
\end{definition}
\begin{definition}
    For this function we assume the Z3 module's functionality is correct and we can take the results from \cite{Moura2008ProofsAR}. Let $Z$ be the Z3 solver instance.
\end{definition}
\begin{definition}
    Let $T$ be the transition function which takes each $s \in S$ and converts $s$ into its corresponding logical form $\in P$. This includes the hard-coded string replacements in the function for each $s$ as well as the \texttt{parse\_smt2\_string} and \texttt{eval} steps in \texttt{check\_premises}. We assume $T(s)$ preserves the logic of $s$.
\end{definition}
\begin{definition}
    Z3($\Phi$) returns \texttt{satisfiable} if $\Phi$ is satisfiable and has no contradictions, and returns \texttt{unsatisfiable} if $\exists$ a contradiction.

\begin{proof}
    First we initialize the Z3 solver instance.\\
    \indent For each $s \in S$, we feed $s$ to the transition function $T$, such that $T$ produces a normalized and $SMT-LIB2$-parsed string, where $T(s) \in P$.\\
    \indent $T(s)$ is then added as a constraint to the solver using $solver.add()$.\\

    \textbf{Case 1:} Z3(${T(s) | s \in S}$) returns \texttt{satisfiable}\\

    This means $\exists$ an assignment of values to $x$, $y$, $z$ that makes all formulas $T(s)$ be true simultaneously.\\
    \begin{itemize}
        \item By the definition of the SMT solver, if $Z3$ returns \texttt{satisfiable}, then there exists a model $M$ such that for all $s \in S$, $M \models T(s)$.
        \item Since $T$ is meaning-preserving, if $M \models T(s)$, then $M \models s$, where $s$ is the original inequality.
        \item Therefore, $M$ is a model for $P = \{s \mid s \in S\}$, and $P$ is satisfiable.
        \item The function then outputs "The premises has no contradictions," which is the desired result.
    \end{itemize}\\

    \textbf{Case 2:} Z3(${T(s) | s \in S}$) returns \texttt{unsatisfiable}\\

    This means $\exists$ no assignment of values to $x$, $y$, $z$ that makes all formulas $T(s)$ true simultaneously.\\
    \begin{itemize}
        \item By the definition of the SMT solver, if $Z3$ returns \texttt{unsatisfiable}, then there is no model $M$ such that for all $s \in S$, $M \models T(s)$.
        \item Since $T$ is meaning-preserving, there is no model $M$ such that for all $s \in S$, $M \models s$.
        \item Therefore, $P = \{s \mid s \in S\}$ is unsatisfiable.
        \item The function then prints "The premises is unsatisfiable and has contradictions," which is the desired result.
    \end{itemize}\\

    \textbf{Conclusion:}

The proof demonstrates that the \texttt{check\_premises} function correctly determines the satisfiability of a set of inequalities, assuming the correctness of the Z3 SMT solver and the meaning-preservation of the translation function $T$.
\end{proof}
\end{definition}


