# Testing

[README.md](README.md)

## Contents

- [Automated Testing](#Automated-Testing)
- [Manual Testing](#Manual-Testing)
- [Solved Issues](#Solved-Issues)
- [Known Issues](#Known-Issues)

## Automated Testing

### Validation

Generated **HTML** and **CSS** code were validated with the W3C Markup and CSS validators. Both were found to have no errors or warnings. Reports can be seen below:

<details>
<summary><b>HTML</b></summary>

- [Home page](dev/tests/html/home_page-validation_report.pdf)
- [Login page](dev/tests/html/login_page-validation_report.pdf)
- [Recipe page](dev/tests/html/recipe_page-validation_report.pdf)
- [Add recipe page](dev/tests/html/add_recipe_page-validation_report.pdf)
- [Edit recipe page](dev/tests/html/edit_recipe_page-validation_report.pdf)
- [Profile page](dev/tests/html/profile_page-validation_report.pdf)
- [Search page](dev/tests/html/search_page-validation_report.pdf)
</details>

<details>
<summary><b>CSS</b></summary>

- [style.css](dev/tests/css/style_css-validation_report.pdf) - Global style sheet
- [login.css](dev/tests/css/login_css-validation_report.pdf) - Login page style sheet
- [recipe.css](dev/tests/css/recipe_css-validation_report.pdf) - Recipe and add/edit recipe pages style sheet
- [search.css](dev/tests/css/search_css-validation_report.pdf) - Search page style sheet
</details>

**JavaScript** code was run through [JSHint](https://jshint.com/) to ensure they were syntactically correct. Any errors were corrected and linting re-run until correct.

Pylint was used to verify **Python** code. Any errors were corrected and re-run until correct. Reports can be seen below:

<details>
<summary><b>app.py</b> report</summary>

```console output
************* Module app
app.py:17:4: W0611: Unused import env (unused-import)

------------------------------------------------------------------

Your code has been rated at 9.95/10 (previous run: 9.95/10, +0.00)
```
[app report](dev/tests/pylint/app_report.txt)

A warning regarding unused-imports remains as the linter is unable to recognise the use of variables in env.py.

</details>

<details>
<summary><b>decorators.py</b> report</summary>

```console output

--------------------------------------------------------------------

Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
```
[decorators report](dev/tests/pylint/decorators_report.txt)

</details>

<details>
<summary><b>helpers.py</b> report</summary>

```console output

--------------------------------------------------------------------

Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
```

[helpers report](dev/tests/pylint/helpers_report.txt)

</details>



<details>

<summary>Google Chrome's <b>lighthouse</b> was also run and provided the following reports:</summary>

Home page

- [Mobile](dev/tests/lighthouse/homepage(mobile).pdf)
- [Desktop](dev/tests/lighthouse/homepage(desktop).pdf)

login page

- [Mobile](dev/tests/lighthouse/loginpage(mobile).pdf)
- [Desktop](dev/tests/lighthouse/loginpage(desktop).pdf)

recipe page

- [Mobile](dev/tests/lighthouse/recipepage(mobile).pdf)
- [Desktop](dev/tests/lighthouse/recipepage(desktop).pdf)

edit recipe page

- [Mobile](dev/tests/lighthouse/editrecipepage(mobile).pdf)
- [Desktop](dev/tests/lighthouse/editrecipepage(desktop).pdf)

profile page

- [Mobile](dev/tests/lighthouse/profilepage(mobile).pdf)
- [Desktop](dev/tests/lighthouse/profilepage(desktop).pdf)

search page

- [Mobile](dev/tests/lighthouse/searchpage(mobile).pdf)
- [Desktop](dev/tests/lighthouse/searchpage(desktop).pdf)

</details>



### Python unit tests

Automated unit testing was performed on functions suitable for it:

- calculate_rating

```
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

Test criteria is in test.py



## Manual Testing



## Solved Issues

## Known Issues