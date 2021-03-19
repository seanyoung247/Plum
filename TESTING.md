# Testing

[README.md](README.md)

## Contents

- [Automated Testing](#Automated-Testing)
  - [Validation](#Validation)
  - [Python unit tests](#Python-unit-tests)
- [Manual Testing](#Manual-Testing)
  - [Testing Environments](#Testing-Environments)
  - [Testing Methodology](#Testing-Methodology)
  - [Unit Testing](#Unit-Testing)
  - [Peer Code Review](#Peer-Code-Review)
  - [Student Checklist](#Student-Checklist)
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



To perform automated testing, from the project root directory type:

python test.py

```
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```



## Manual Testing

### Testing Environments

Primary iterative testing was undertaken on a Windows 10 desktop machine with the Google Chrome browser. Once a feature was considered complete it was tested in other environments.

**Desktop testing**

- Platforms:
  - Custom Desktop (Windows 10, Fedora 33)
  - Microsoft SurfaceBook 2 (Windows 10)
  - Apple MacBook Air M1 (macOS Big Sur 11.2.2)
- Browsers:
  - Google Chrome/Chromium
  - Microsoft Edge
  - Firefox
  - Opera
  - Safari

**Tablet testing**

- Platforms:
  - Lenovo Tab M10 (Android 10)
- Browsers:
  - Google Chrome
  - Firefox
  - Opera

**Mobile testing**

- Platforms:
  - OnePlus7 (Android 10)
  - Samsung Galaxy J6 (Android 10)
- Browsers:
  - Chrome
  - FireFox
  - Opera

### Testing Methodology

Code changes were tested prior to committing and pushing to github on the local machine. This was in an attempt to prevent faulty or broken code from being pushed to the repository or deployed to the live site. Further, new features were pushed to a separate branch, which wasn't merged to main and deployed to the live site until tested. On occasions where bugs were missed in testing an issue was opened on github if appropriate. Issues were not raised for bugs arising from known feature incomplete code committed to github, as this information was captured in the coding to-do lists. This approach kept most bugs from being uploaded, with only a few cases of bugs either too complex to be fixed for the current release, or those that introduced regressions in existing code being uploaded.

### Unit Testing

Manual unit testing was conducted iteratively by attempting to "break" new code. In this way most bugs were caught and fixed before committing to the repository and live site.

The python print() and JavaScript console.log functions were used to output variable values and breakpoints during development to give hints to where faults were occurring and why.

Final UI testing was conducted prior to submission to confirm the UI fulfilled the required user stories:

[UI Testing Report](dev/tests/uitesting.pdf)

### Peer Code Review

The project was submitted to peer review on the code institute slack [channel]().

### Student Checklist

A Final sanity check was done with the student check list to ensure the site fits submission guidelines.

## Solved Issues

## Known Issues