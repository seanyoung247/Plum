# Plum
Plum is a recipe sharing website designed to help users find recipes and share their own with others.



## UX (User Experience)

### Project Goals

TBC

### User Stories

#### Searching

- (US00x) - As a cook I want to search recipes by name so that I can find specific dishes that I want to make
- (US00x) - As a cook I want to search recipes on cuisine type so that I can get dishes of a specific type I want to make
- (US00x) - As a cook I want to be able to be able to filter recipes based on cooking time so I can get dishes I have time to prepare
- (US00x) - As a cook I want to save my favourite recipes so that I can quickly find them again in the future

#### Uploading

- (US00x) - As a recipe creator I want to upload my own recipes so that other users can benefit from them
- (US00x) - As a user I want to 

## Design

### Database 

#### Schema

##### Recipe collection

Stores individual recipes

| Field name  | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| _id         | Record id                                                    |
| name        | Recipe name                                                  |
| author      | User token                                                   |
| description | Short description of the recipe                              |
| cuisine     | Cuisine type                                                 |
| prep_time   | Time in seconds it takes to prepare the recipe               |
| cook_time   | Time in seconds it takes to cook the recipe                  |
| servings    | Integer number of the number of servings this recipe provides |
| rating      | List of values for how many of each star rating the recipe has received. |
| ingredients | List of ingredients                                          |
| steps       | List of strings of preparation steps                         |
| comments    | List of comments                                             |

###### User token

| Field name | Description                                  |
| ---------- | -------------------------------------------- |
| name       | User name                                    |
| user_id    | Record id of the user in the user collection |

###### Ingredients List

| Field name | Description                               |
| ---------- | ----------------------------------------- |
| name       | Ingredient name                           |
| amount     | How many units to use for this ingredient |
| unit       | Name of the unit                          |
| unit_id    | Id for the unit in the unit collection    |

###### Comment List

##### User collection

##### Rating collection

##### Units collection

##### Cuisine collection 

#### Queries

### Fonts

### Colours

### Layout

