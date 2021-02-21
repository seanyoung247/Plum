

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

**Administration**

- (US010) - As an admin I want to be able to edit content to ensure it adheres to site rules.
- (US011) - As an admin I want to be able to add cuisine categories so users can search efficiently.

**General**

- (US012) - As a user I want to receive clear feedback for my actions so I know if any further action is required.

##  Design

### Database 

#### Schema

##### Recipe Collection

Stores individual recipes

| Field name  | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| _id         | Record id                                                    |
| name        | Recipe name                                                  |
| author      | User token for recipe author                                 |
| date        | The date this recipe was added                               |
| description | Short description of the recipe                              |
| image       | Recipe Image URL string                                      |
| cuisine     | Cuisine type                                                 |
| time        | Time token                                                   |
| servings    | Integer number of the number of servings this recipe provides |
| rating      | List of values for how many of each star rating the recipe has received. |
| ingredients | List of ingredients                                          |
| steps       | List of strings of preparation steps                         |
| comments    | List of comment objects                                      |

###### User Token

| Field Name | Description    |
| ---------- | -------------- |
| name       | User name      |
| user_id    | User record id |

###### User Token

| Field Name | Description           |
| ---------- | --------------------- |
| total      | Total time in seconds |
| hours      | Number of hours       |
| minutes    | Number of minutes     |

###### Ingredient List

| Field Name | Description                                                |
| ---------- | ---------------------------------------------------------- |
| name       | Ingredient name                                            |
| recipe_id  | If this ingredient is also a recipe this is it's record id |
| amount     | How many units to use for this ingredient                  |
| unit       | Name of the unit                                           |
| unit_id    | Id for the unit in the unit collection                     |

###### Comment List

| Field Name | Description                      |
| ---------- | -------------------------------- |
| user       | User token                       |
| rating     | The rating they gave this recipe |
| comment    | String content of the comment    |

##### User Collection

Holds information on each registered user

| Field Name | Description              |
| ---------- | ------------------------ |
| _id        | Record id                |
| name       | User Name                |
| password   | User's password hash     |
| email      | User's email address     |
| role       | User role, user or admin |
| recipes    | List of recipe tokens    |

###### Recipe Token

| Field Name | Description      |
| ---------- | ---------------- |
| name       | Recipe name      |
| recipe_id  | Recipe record id |

##### Rating Collection

Holds individual user-recipe rating interactions. Indexed on user_id and recipe_id.

| Field Name | Description                                 |
| ---------- | ------------------------------------------- |
| _id        | Record id                                   |
| user_id    | Record id of the user making this rating    |
| recipe_id  | Record id of the recipe being rated         |
| rating     | Number 1-5 indicating the star rating given |
| favourited | Did the user favourite the recipe?          |

##### Units Collection

Enumerates unit types for use in recipe ingredient lists.

| Field Name | Description               |
| ---------- | ------------------------- |
| _id        | Record id                 |
| name       | Name of the unit type     |
| display    | Display name for the unit |

Note: Can be expanded to allow unit conversion later

##### Cuisine Collection 

Enumerates cuisine types.

| Field Name | Description              |
| ---------- | ------------------------ |
| _id        | Record id                |
| name       | Name of the cuisine type |

#### Indexes

**recipes:**

1. pageid_1 - Regular index ensures pageid field is unique
2. -Text indexes for searching-

#### Queries

##### Browsing

**Returns the 8 newest recipes (for US001):**

```mongodb
plumdb.recipes.find().sort("_id", -1).limit(8)
```

##### Users

**Returns a specific user account based on username:**

```mongodb
plumdb.users.find_one({"name": "username"})
```
**Inserts a new user account into the database:**

```mongodb
plumdb.users.insert_one(user-record)
```

##### Searching

**Finds a single recipe from it's pageid (for showing a single recipe page):**

```Mongodb
plumdb.recipes.find_one({"pageid": pageid})
```

##### Uploading

**Adds a rating vote to a recipe (for US002 and US008)**

Updating the recipe record

```mongodb
plumdb.recipes.update_one({"_id" : recipeId}
{
	"$set" : {
		"rating.0" : avg_rating,
		"rating.{vote}" : rating[vote] + 1
	}
})
```

Adding the rating record

```mongodb
plumdb.ratings.insert_one(interaction)
```

**Updates a rating vote on a recipe (for US002 and US008)**

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

**Adds a comment to a recipe (for US002 and US008)**

```mongodb
plumdb.recipes.update_one({"_id" : recipeId}
{
	"$push" : { "comments" : {
		"author" : user_token,
		"text" : comment		
	}}
})
```

##### Administration

TODO: Administration database queries here

### Fonts

Headers are rendered using [Open Sans](https://fonts.google.com/specimen/Open+Sans) with body text in [Roboto](https://fonts.google.com/specimen/Roboto). Open Sans was chosen for headers because it is bold and clear, while Roboto is easy to read and widely used on the web. Both are obtained from Google Fonts.

### Colours

Sap Green was chosen as it is associated with nature, health, and freshness. Plum purple fits the branding of the site well while also being complimentary to Sap Green and evoking feelings of luxury. Honeydew was chosen as a background colour as it is near white, providing plenty of contrast for darker elements and text, while also tying into the main green colour.

![pallet](dev/images/pallet/palette.png)

- Sap Green (#3F7D20) - Main site brand colour
- Plum (#8E4585) - Accent colour
- Honeydew (#F3FCF0) - Background colour
- Rich Black (#0D0A0B) - Main text colour

### Layout

[Wireframes](dev/mockups/wireframes.pdf)



