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
- encode_time
- calculate_pages



To perform automated testing, from the project root directory type:

`python test.py`

```
>python test.py
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s

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

The project was submitted to peer review on the code institute slack [channel](https://code-institute-room.slack.com/archives/CGWQJQKC5/p1616189018032700).

### Student Checklist

A Final sanity check was done with the student check list to ensure the site fits submission guidelines.

## Solved Issues

#### 404 when opening login page when user logged in

[Link](https://github.com/seanyoung247/Plum/issues/5). If a user is already logged in and tries to open the login page the website raises a 404 error.

**Cause**

Missing url_for in redirect

**Resolution**

[Fix: Fixes 404 error from login page when user already logged in](https://github.com/seanyoung247/Plum/commit/48d99c929fc639fb840b948ceb74c05125b0ff3c)



#### Recipe page layout broken on small screens

[Link](https://github.com/seanyoung247/Plum/issues/6). Page layout breaks when using Google Chrome's responsive layout test.

**Cause**

Fault in either Google Chrome or Materialize.

**Resolution**

Not applicable.



#### Exception on registering new user

[Link](https://github.com/seanyoung247/Plum/issues/7). Exception raised when registering new user.

**Cause**

User not being added properly to session cookie after registration.

**Resolution**

[Fix: Fixes exception on registering new user](https://github.com/seanyoung247/Plum/commit/715e6082fe0249b77427f4768a93af4d3bb59e8d)



#### Admin editing another users recipe changes recipe author

[Link](https://github.com/seanyoung247/Plum/issues/13). Admin user overwrites original author field.

**Cause**

Author field overwritten when updating recipe record

**Resolution**

[Fix: Prevents overwriting author when editing a recipe](https://github.com/seanyoung247/Plum/commit/769cca4aee720263c1868fa3bc02b0d66a1b8226)



#### On refresh horizontal scroller is offset vertically by to bottom of the page

[Link](https://github.com/seanyoung247/Plum/issues/15). Firefox offsets contents.

**Cause**

Scroll-item being set to 100% height.

**Resolution**

[Fix: Fixes firefox layout issue of horizontal scroller](https://github.com/seanyoung247/Plum/commit/00b358e11f80abb1bfb0b158ce4d1775b60360ac)



#### Using the time picker in the search form gives an error message

[Link](https://github.com/seanyoung247/Plum/issues/32). The following error is displayed in the console when using the time-picker component:
`[Intervention] Unable to preventDefault inside passive event listener due to target being treated as passive.`

**Cause**

Appears to be issue within materialize. Possibly using a passive scroll event listener.

**Resolution**

Not Applicable