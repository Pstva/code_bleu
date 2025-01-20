# CodeBLEU

Just a PyPi package with code taken and adapted from the official implementation from [microsoft/CodeXGLUE](https://github.com/microsoft/CodeXGLUE/blob/main/Code-Code/code-to-code-trans/CodeBLEU.MD).

Install

```sh
git clone git@github.com:Pstva/code_bleu.git
cd code_bleu
poetry build
```


Usage:

```python
from code_bleu import calc_code_bleu

hyps = ["def lala():\n    return 1", "def lulu():\n    return sum(1, 2)"]
refs = [["def lala():\n    return 1"], ["def lala():\n    return 1", "def lulu():\n    return sum(1, 2)"]]

params = (0.25, 0.25, 0.25, 0.25) #alpha, beta, gamma, theta
lang='python'
calc_code_bleu(refs, hyps, lang, params)
```