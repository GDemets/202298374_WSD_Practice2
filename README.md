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

