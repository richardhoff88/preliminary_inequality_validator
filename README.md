# 🧮 Mathbeaver Polynomial List Checker

A Python project to automatically validate a list of polynomial inequalities by detecting contradictions using symbolic and SMT-based methods.

---

## 📌 Overview

This project takes a list of inequalities (as strings) and checks if they are consistent (i.e., whether there exists an assignment of real values to variables that makes them all true).  
It uses:
- Symbolic simplification (`Sympy`)
- SMT solvers (`Z3`)

---

## ✏️ Example Input

```python
premises = [
    "(xz−2x−5z) > 0",
    "(4x+y+5) ≥ 0",
    "(3x(yz+5y+1)) ≥ 0",
    "(1) = 0",
    "(yz−4y+5z+3) > 0"
]
