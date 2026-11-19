# Sudoku

Jogo de Sudoku desenvolvido com apoio de IA.

## Executar

O tabuleiro vazio é criado como uma matriz 9x9 e exibido no terminal:

```bash
python sudoku.py
```

As casas vazias são representadas internamente por `0` e exibidas como `.`.

A função `is_valid_move` valida números de `1` a `9` e impede conflitos na
linha, coluna ou quadrante 3x3 da posição escolhida.

Use `load_board("easy")`, `load_board("medium")` ou `load_board("hard")` para
carregar um tabuleiro pré-pronto. Cada chamada retorna uma cópia independente.

## Testes

```bash
python -m unittest
```
