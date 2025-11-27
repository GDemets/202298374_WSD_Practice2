# 202298374_WSD_Practice2

## Context
This application is a RESTful API built with Flask and SQLAlchemy, allowing the management of users (User) and their posts (Post).
It implements all CRUD operations: Create, Read, Update, Delete, with full error handling and a standardized JSON response format.

## User Model
| Champ    | Type        | Contraintes      |
| -------- | ----------- | ---------------- |
| id       | Integer     | Primary Key      |
| pseudo   | String(30)  | Unique, Not Null |
| mail     | String(30)  | Unique, Not Null |
| password | String(100) | Not Null         |
| role     | String(20)  | Not Null         |

## Post model
| Champ   | Type        | Contraintes           |
| ------- | ----------- | --------------------- |
| id      | Integer     | Primary Key           |
| user_id | Integer     | Foreign Key → User.id |
| score   | Integer     | Not Null              |
| message | String(100) | Not Null              |

## Endpoints
### GET
| Endpoint           | Description                    | Success | Error |
| ------------------ | ------------------------------ | ------- | ----- |
| `/users`           | Get all the users              | 200     | -     |
| `/users/<user_id>` | Get an user by his id          | 200     | 404   |

### POST
| Endpoint                 | Description                      | Success | Error     |
| ------------------------ | -------------------------------- | ------- | ----------|
| `/users`                 | Create a new user                | 201     | 400, 409  |
| `/users/<user_id>/posts` | Create a new post                | 201     | 400, 404  |

### PUT
| Endpoint                  | Description        | Success | Error         |
| ------------------------- | ------------------ | ------- | --------------|
| `/users/mail/<user_id>`   | Update mail user   | 200     | 400, 404      |
| `/users/pseudo/<user_id>` | Update pseudo user | 200     | 400, 404, 409 |

### DELETE
| Endpoint           | Description          | Success | Error    |
| ------------------ | -------------------- | ------- | ---------|
| `/users/<user_id>` | Delets a user        | 200     | 404      |
| `/users`           | Delete all the users | 200     | 404, 500 |


