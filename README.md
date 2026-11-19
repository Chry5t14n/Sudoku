# Sudoku

Jogo de Sudoku desenvolvido com apoio de IA.

## Executar

O jogo carrega um tabuleiro fácil e permite inserir jogadas pelo terminal:

```bash
python sudoku.py
```

As casas vazias são representadas internamente por `0` e exibidas como `.`.
Informe `linha coluna número` usando valores de `1` a `9`. Digite `sair` para
encerrar. Os números do tabuleiro inicial não podem ser alterados.
Após cada jogada, o programa verifica se o tabuleiro foi completado
corretamente e exibe uma mensagem de parabéns ao vencer.

A função `is_valid_move` valida números de `1` a `9` e impede conflitos na
linha, coluna ou quadrante 3x3 da posição escolhida.

Use `load_board("easy")`, `load_board("medium")` ou `load_board("hard")` para
carregar um tabuleiro pré-pronto. Cada chamada retorna uma cópia independente.

## Interface no navegador

Inicie um servidor local na raiz do projeto:

```bash
python3 -m http.server 8000
```

Depois abra `http://localhost:8000` no navegador.

Clique em uma casa vazia e use as teclas `1` a `9` para preencher. Use
`Backspace` ou `Delete` para limpar a casa e `Escape` para remover a seleção.

## Testes

```bash
python -m unittest
```
