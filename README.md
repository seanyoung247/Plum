# ![plum](static/images/plum.png)Plum
Plum is a recipe sharing website designed to help users find recipes and share their own with others.

## UX (User Experience)

### Project Goals

TBC

### User Stories

#### Browsing

- (US001) - As a cook I want the website to be able to make suggestions to me so I can be introduced to new content.

#### Searching

- (US002) - As a cook I want to search recipes by name so that I can find specific dishes that I want to make.
- (US003) - As a cook I want to search recipes on cuisine type so that I can get dishes of a specific type I want to make.
- (US004) - As a cook I want to be able to be able to filter recipes based on cooking time so I can get dishes I have time to prepare.
- (US005) - As a cook I want to save my favourite recipes so that I can quickly find them again in the future.

#### Uploading

- (US006) - As a recipe creator I want to upload my own recipes so that other users can benefit from them.
- (US007) - As a recipe creator I want to gain feedback on my recipes so I can discover improvements.
- (US008) - As a recipe creator I want to be able to edit a recipe I've posted so I can improve it.

## Design

### Database 

#### Schema

##### Recipe collection

Stores individual recipes

| Field name  | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| _id         | Record id                                                    |
| name        | Recipe name                                                  |
| author      | User token for recipe author                                 |
| favourited  | List of user tokens for users who have favourited this recipe |
| description | Short description of the recipe                              |
| cuisine     | Cuisine type                                                 |
| prep_time   | Time in seconds it takes to prepare the recipe               |
| cook_time   | Time in seconds it takes to cook the recipe                  |
| servings    | Integer number of the number of servings this recipe provides |
| rating      | List of values for how many of each star rating the recipe has received. |
| ingredients | List of ingredients                                          |
| steps       | List of strings of preparation steps                         |
| comments    | List of comments                                             |

###### User Token

| Field Name | Description    |
| ---------- | -------------- |
| name       | User name      |
| user_id    | User record id |

###### Ingredients List

| Field Name | Description                                                |
| ---------- | ---------------------------------------------------------- |
| name       | Ingredient name                                            |
| recipe_id  | If this ingredient is also a recipe this is it's record id |
| amount     | How many units to use for this ingredient                  |
| unit       | Name of the unit                                           |
| unit_id    | Id for the unit in the unit collection                     |

###### Comment List

| Field Name | Description                           |
| ---------- | ------------------------------------- |
| user       | Name of the user who left the comment |
| user_id    | User's record id                      |
| comment    | String content of the comment         |

##### User collection

Holds information on each registered user

| Field Name | Description           |
| ---------- | --------------------- |
| _id        | Record id             |
| name       | User Name             |
| password   | User's password hash  |
| recipes    | List of recipe tokens |

###### Recipe Token

| Field Name | Description      |
| ---------- | ---------------- |
| name       | Recipe name      |
| recipe_id  | Recipe record id |

##### Rating collection

Holds individual user-recipe rating interactions. Indexed on user_id and recipe_id.

| Field Name | Description                                 |
| ---------- | ------------------------------------------- |
| _id        | Record id                                   |
| user_id    | Record id of the user making this rating    |
| recipe_id  | Record id of the recipe being rated         |
| rating     | Number 1-5 indicating the star rating given |
| favourited | Did the user favourite the recipe?          |

##### Units collection

Enumerates unit types for use in recipe ingredient lists.

| Field Name | Description           |
| ---------- | --------------------- |
| _id        | Record id             |
| name       | Name of the unit type |

Note: Can be expanded to allow unit conversion later

##### Cuisine collection 

Enumerates cuisine types.

| Field Name | Description              |
| ---------- | ------------------------ |
| _id        | Record id                |
| name       | Name of the cuisine type |

#### Queries

### Fonts

### Colours

### Layout

