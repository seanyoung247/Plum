

# ![plum](static/images/plum.png)Plum

Plum is a recipe sharing website designed to help users find recipes and share their own with others.

[See live site.](https://plum-recipes.herokuapp.com/)

## Table of Contents

- **[User Experience](#User-Experience)**
  - [Project Goals](#Project-Goals)
    - [User Stories](#User-Stories)
- **[Design](#Design)**
  - [Database](#Database)
    - [Schema](#Schema)
      - [Recipe Collection](#Recipe-Collection)
        - [User Token](#User-Token)
        - [Ingredient List](#Ingredient-List)
        - [Comment List](#Comment-List)
      - [User Collection](#User-Collection)
        - [Recipe Token](#Recipe-Token)
      - [Rating Collection](#Rating-Collection)
      - [Units Collection](#Units-Collection)
      - [Cuisine Collection](#Cuisine-Collection)
    - [Relationships](#Relationships)
    - [Indexes](#Indexes)
    - [Queries](#Queries)
      - [Browsing](#Browsing)
      - [Users](#Users)
      - [Searching](#Searching)
      - [Uploading](#Uploading)
      - [Administration](#Administration)
  - [Fonts](#Fonts)
  - [Colours](#Colours)
  - [Layout](#Layout)
- [Features](#Features)
- [Technologies](#Technologies)
- [Testing](#Testing)
- [Source Control](#Source-Control)
  - [Branches](#Branches)
  - [Github Desktop](#Github-Desktop)
- [Deployment](#Deployment)
- [Credits](#Credits)
  - [Media](#Media)
  - [Acknowledgements](#Acknowledgements)

## User Experience

### Project Goals

TBC

### User Stories

**Browsing**

- (US001) - As a cook I want the website to make suggestions to me so I can be introduced to new content.
- (US002) - As a cook I want to see reviews and ratings from other users so I can select the best content.

**Searching**

- (US003) - As a cook I want to search recipes by name so that I can find specific dishes that I want to make.
- (US004) - As a cook I want to search recipes on cuisine type so that I can get dishes of a specific type I want to make.
- (US005) - As a cook I want to be able to be able to filter recipes based on cooking time so I can get dishes I have time to prepare.
- (US006) - As a cook I want to save my favourite recipes so that I can quickly find them again in the future.

**Uploading**

- (US007) - As a recipe creator I want to upload my own recipes so that other users can benefit from them.
- (US008) - As a recipe creator I want to gain feedback on my recipes so I can discover improvements.
- (US009) - As a recipe creator I want to be able to edit a recipe I've posted so I can improve it.

**Users**

- (US010) - As a new user I want to be able to register with the site so that I can upload new recipes and track my favourites.
- (US011) - As a registered user I want to be able to log into my account so that I can access my recipes and favourites.

**Administration**

- (US012) - As an admin I want to be able to edit content to ensure it adheres to site rules.
- (US013) - As an admin I want to be able to add cuisine categories so users can search efficiently.

**General**

- (US014) - As a user I want to receive clear feedback for my actions so I know if any further action is required.

##  Design

### Database 

#### Schema

##### Recipe Collection

Stores individual recipes

| Field name  | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| _id         | Record id                                                    |
| pageid      | Unique string url path for this recipe                       |
| title       | Recipe name                                                  |
| author      | Username of the user who uploaded this recipe                |
| date        | The date this recipe was added                               |
| description | Short description of the recipe                              |
| image       | Recipe Image URL string                                      |
| cuisine     | Cuisine type                                                 |
| time        | time this recipe takes to prepare in minutes                 |
| servings    | Integer number of the number of servings this recipe provides |
| rating      | List of values for how many of each star rating the recipe has received. |
| ingredients | List of ingredients                                          |
| steps       | List of strings of preparation steps                         |
| comments    | List of comment objects                                      |

###### Comment List

| Field Name | Description                   |
| ---------- | ----------------------------- |
| user       | Username                      |
| comment    | String content of the comment |

##### User Collection

Holds information on each registered user

| Field Name | Description              |
| ---------- | ------------------------ |
| _id        | Record id                |
| name       | User Name                |
| password   | User's password hash     |
| email      | User's email address     |
| role       | User role, user or admin |

##### Rating Collection

Holds individual user-recipe rating interactions. Indexed on user_id and recipe_id.

| Field Name | Description                                 |
| ---------- | ------------------------------------------- |
| _id        | Record id                                   |
| user_id    | Record id of the user making this rating    |
| recipe_id  | Record id of the recipe being rated         |
| rating     | Number 1-5 indicating the star rating given |
| favourited | Did the user favourite the recipe?          |

##### Cuisine Collection 

Enumerates cuisine types.

| Field Name | Description              |
| ---------- | ------------------------ |
| _id        | Record id                |
| name       | Name of the cuisine type |

#### Relationships

#### Indexes

**recipes:**

1. Unique index on page_id - Ensures pageid field is unique.
2. Text index on title and description for text searches.

**users:**

1. Unique index on name - Ensures two users can't share a username.

**ratings:**

1. Unique compound index on user_id and recipe_id - Ensures only one interaction record between one recipe and user.

**cuisines:**

1. Unique index on name - Ensures each cuisine type only appears once.

#### Queries

<Rationale/explanation goes here>

##### Browsing

**Returns the 8 newest recipes (for US001):**

```mongodb
plumdb.recipes.find().sort("_id", -1).limit(8)
```

**Returns a specific Recipe/User interaction (for US002, US008):**

```Mongodb
plumdb.ratings.find_one({"user_id" : user['userid'], "recipe_id" : recipe['_id']})
```

##### Users

**Returns a specific user account based on username (US011):**

```mongodb
plumdb.users.find_one({"name": "username"})
```
**Inserts a new user account into the database (US010):**

```mongodb
plumdb.users.insert_one(user-record)
```

**Returns all the recipes a user has uploaded:**

```mongodb
plumdb.recipes.find({"author" : username})
```

**Returns all the recipes a user has favourited (for US006):**

```mongodb
plumdb.ratings.aggregate([
	{ "$match" : {"user_id" : userid, "favorited" : True} },
	{
		"$lookup" : {
			"from" : "recipes",
			"localField" : "recipe_id",
			"foreignField" : "_id",
			"as": "favorites"
		}
	},
	{"$unwind" : "$favorites"},
	{"$replaceRoot" : {"newRoot" : "$favorites"}}
])
```

##### Searching

**Finds a single recipe from it's pageid (for showing a single recipe page):**

```Mongodb
plumdb.recipes.find_one({"pageid": pageid})
```

**Finds recipes conforming to a user's search (for US003, US004, and US005):**

Any individual field can be omitted as long as at least one field is passed.

```Mongodb
plumdb.recipes.find({
	
})
```

##### Uploading

**Adds a rating vote to a recipe (for US002 and US008)**:

Updating the recipe record

```mongodb
plumdb.recipes.update_one({"_id" : recipeId}
{
	"$set" : {
		"rating.0" : avg_rating,
		"rating.<vote>" : rating[vote] + 1
	}
})
```

Adding the rating record

```mongodb
plumdb.ratings.insert_one(interaction-record)
```

**Updates a rating vote on a recipe (for US002 and US008)**:

Updating the recipe record

```mongodb
plumdb.recipes.update_one({"_id" : recipeId}
{
	"$set" : {
		"rating.0" : avg_rating,
		"rating.{vote}" : rating[vote] + 1
		"rating.{old_vote}" : rating[old_vote] - 1
	}
})
```

Updating the rating record

```mongodb
plumdb.ratings.update_one({"_id" : interaction._id}, 
{
	"$set" : {"rating" : new_rating}
})
```

**Favouriting a recipe (for US006):**

```mongodb
plumdb.ratings.update_one({"_id" : existing_interaction['_id']},
	{"$set" : {"favorited" : favorite}})
```

**Adds a comment to a recipe (for US002 and US008)**:

```mongodb
plumdb.recipes.update_one({"_id" : recipeId}
{
	"$push" : { "comments" : {
		"author" : username,
		"text" : comment		
	}}
})
```

**Adds a new recipe (for US007):**

Adds the recipe to the database

```mongodb
plumdb.recipes.insert_one(recipe-record)
```

Adds the recipe to the users list

```mongodb
plumdb.users.update_one({"_uid" : userid},
	{"$push" : {"recipes" : recipe_token}})
```

**Edits an existing recipe (for US009):**

```Mongodb
mongo.db.recipes.replace_one({"pageid" : pageid}, recipe-record)
```

##### Administration

TODO: Administration database queries here

### Fonts

Headers are rendered using [Open Sans](https://fonts.google.com/specimen/Open+Sans) with body text in [Roboto](https://fonts.google.com/specimen/Roboto). Open Sans was chosen for headers because it is bold and clear, while Roboto is easy to read and widely used on the web. Both are obtained from Google Fonts.

### Colours

Sap Green was chosen as it is associated with nature, health, and freshness. Plum purple fits the branding of the site well while also being complimentary to Sap Green and evoking feelings of luxury. Honeydew was chosen as a background colour as it is near white, providing plenty of contrast for darker elements and text, while also tying into the main green colour.

### ![pallet](dev/images/pallet/palette.png)

- Sap Green (#3F7D20) - Main site brand colour
- Plum (#8E4585) - Accent colour
- Honeydew (#F3FCF0) - Background colour
- Rich Black (#0D0A0B) - Main text colour
- White - As a background to bring out some sections

### Layout

[Wireframes](dev/mockups/wireframes.pdf)

## Features

## Technologies

### Languages

- [HTML5](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
  - Used as the markup language for the site layout.
- [CSS3](https://developer.mozilla.org/en-US/docs/Web/CSS)
  - Used to style and colour HTML and dynamic elements.
- [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
  - Used to create and manipulate the site's client-side dynamic elements. Also performs AJAX requests for client/server communication.
- [Python](https://www.python.org/)
  - Used for the backend server and running queries to the database.
- [Jinja](https://jinja.palletsprojects.com/en/2.11.x/)
  - Used to generate HTML from site templates
- [SVG](https://developer.mozilla.org/en-US/docs/Glossary/SVG)
  - Used to define a number of the sites icons and graphical elements.

### Libraries

- [JQuery](https://jquery.com)
    - The project uses JQuery to simplify DOM manipulation.
- [Bootstrap](https://getbootstrap.com/)
    - The project uses bootstrap to aid in responsive design.
- [Popper](https://popper.js.org/)
    - Included as a requirement of bootstrap. Used in dropdown splash screen menu.
- [Virtual Joystick](https://github.com/jeromeetienne/virtualjoystick.js)
    - A relatively lightweight touch joystick used for user interaction on touch screens. Licenced under the [MIT Licence](assets/scripts/MIT-LICENSE.txt).

### Editors:

- [Typora](https://typora.io/)
  - Typora was used to simplify creation of the README.md file.
- [Atom](https://atom.io/)
  - Atom was used to write HTML and Javascript code.
- [dbdiagram](https://dbdiagram.io/home)
  - Used to create Entity Relationship Diagrams of the database.
- [Balsamic](https://balsamiq.com/)
  - Used to create the website's wireframes.

### Tools:

- [Git](https://git-scm.com/)
  - Used for version control (via github desktop).
- [Github desktop](https://desktop.github.com/)
  - Used to push updates and synchronise local code with the remote repository.
- [Github](https://github.com/)
  - Used to store the project repository and deploy the site via github pages.
- [MongoDB](https://www.mongodb.com/3)
  - Used for the backend database.
- [Adobe Photoshop](https://www.adobe.com/products/photoshop.html)
  - Used to create some of the image files used on the site.
- [Adobe Illustrator](https://www.adobe.com/products/illustrator.html)
  - Used to create some of the sprite images and icons used on the site.

## Testing

## Source Control

The website was developed using the Atom editor with github for version control. Github Desktop was used to simplify the process of compiling pushing commits to the remote repository.

### Branches

Branches were used to add new features for testing without affecting the main branch and deployed application. 

#### Creating a branch

#### Selecting a branch

#### Merging a branch

#### Deleting a branch

### Github Desktop

#### Github Accounts

Once installed Github Desktop can be linked to an existing user account by:

1. Selecting File->Options from the Github Desktop menu.
2. Selecting sign in in the Accounts section of the dialog.
3. Enter github user account and password.

#### Cloning Repositories

Adding an existing github repository to the local machine and Github Desktop can be achieved by:

1. Selecting File->Clone repository... from the Github Desktop menu.
2. Selecting the repository from the list in the dialog.
3. Selecting where the repository should be cloned to on the local machine
4. Clicking the clone button
5. Github Desktop will automatically clone the repository.

#### Selecting current Repository

Github Desktop will automatically track any changes to the current local repository from the github repository.

1. Click the "current repository" button
2. Select the required repository from the menu

#### Updating Github

Github desktop will automatically flag unmerged changes in the current repository. These can be merged by:

1. Deselect any changes to be excluded from the next commit in the changes list. (Github desktop automatically selects all available commits.)
2. Add commit summary.
3. Add commit description (if any).
4. Click "commit to master".
5. Select Push Origin from the pane on the right.

## Deployment

## Credits

### Media
<details>
  <summary>Click to expand!</summary>

  ## Heading
  1. A numbered
  2. list
     * With some
     * Sub bullets
</details>




Recipes:

- Parmesan Crusted Chicken image and recipe from [gimmedelicious](https://gimmedelicious.com/crispy-parmesan-crusted-chicken/).

General:

- [New Recipe image](https://unsplash.com/photos/x5SRhkFajrA) - photograph by [Todd Quackenbush](https://unsplash.com/@toddquackenbush)

### Acknowledgements