# Plum
Plum is a recipe sharing website designed to help users find recipes and share their own with others.



## UX (User Experience)

### Project Goals

TBC

### User Stories

#### Browsing

- (US00x) - As a cook I want the website to be able to make suggestions to me so I can be introduced to new content.

#### Searching

- (US00x) - As a cook I want to search recipes by name so that I can find specific dishes that I want to make.
- (US00x) - As a cook I want to search recipes on cuisine type so that I can get dishes of a specific type I want to make.
- (US00x) - As a cook I want to be able to be able to filter recipes based on cooking time so I can get dishes I have time to prepare.
- (US00x) - As a cook I want to save my favourite recipes so that I can quickly find them again in the future.

#### Uploading

- (US00x) - As a recipe creator I want to upload my own recipes so that other users can benefit from them.
- (US00x) - As a user I want to gain feedback on my recipes so I can improve them.

## Design

### Database 

#### Schema

##### Recipe collection

Stores individual recipes

| Field name  | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| _id         | Record id                                                    |
| name        | Recipe name                                                  |
| author      | Name of the user who posted the recipe                       |
| author_id   | Record id of the user in the user collection                 |
| description | Short description of the recipe                              |
| cuisine     | Cuisine type                                                 |
| prep_time   | Time in seconds it takes to prepare the recipe               |
| cook_time   | Time in seconds it takes to cook the recipe                  |
| servings    | Integer number of the number of servings this recipe provides |
| rating      | List of values for how many of each star rating the recipe has received. |
| ingredients | List of ingredients                                          |
| steps       | List of strings of preparation steps                         |
| comments    | List of comments                                             |

###### Ingredients List

| Field name | Description                               |
| ---------- | ----------------------------------------- |
| name       | Ingredient name                           |
| amount     | How many units to use for this ingredient |
| unit       | Name of the unit                          |
| unit_id    | Id for the unit in the unit collection    |

###### Comment List

| Field Name | Description                           |
| ---------- | ------------------------------------- |
| user       | Name of the user who left the comment |
| user_id    | User's record id                      |
| comment    | String content of the comment         |

##### User collection

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

##### Units collection

##### Cuisine collection 

#### Queries

### Fonts

### Colours

### Layout

