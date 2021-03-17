# Testing

[README.md](README.md)

## Contents

- [Automated Testing](Automated-Testing)
- [Manual Testing](Manual-Testing)
- [Solved Issues](Solved-Issues)
- [Known Issues](Known-Issues)

## Automated Testing

### Validation

Generated **HTML** and **CSS** code were validated with the W3C Markup and CSS validators. Both were found to have no errors or warnings. Reports can be seen below:

Home page

Login page

Recipe page

Add/Edit recipe page

Search page

Profile page

**JavaScript** code was run through [JSHint](https://jshint.com/) to ensure they were syntactically correct. Any errors were corrected and linting re-run until correct.

Pylint was used to verify **Python** code. Any errors were corrected and re-run until correct*. Reports can be seen below:

<details>
<summary><b>app.py</b> report</summary>

```console output
************* Module app
app.py:17:4: W0611: Unused import env (unused-import)

------------------------------------------------------------------

Your code has been rated at 9.95/10 (previous run: 9.95/10, +0.00)
```
</details>

<details>
<summary><b>decorators.py</b> report</summary>

```console output

--------------------------------------------------------------------

Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
```
</details>

<details>
<summary><b>helpers.py</b> report</summary>

```console output

--------------------------------------------------------------------

Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
```

*A warning regarding unused-imports remains as the linter is unable to recognise the use of variables in env.py.
</details>

<lighthouse>

### Python unit tests

## Manual Testing

## Solved Issues

## Known Issues