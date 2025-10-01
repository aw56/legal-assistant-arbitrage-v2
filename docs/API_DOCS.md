# 📖 API Docs — Legal Assistant Arbitrage v2

Сгенерировано автоматически из `http://localhost:8000/openapi.json`


## `/`

### GET

- **Описание:** Root

#### Ответы:

- `200`: Successful Response


## `/api/health`

### GET

- **Описание:** Health Check

#### Ответы:

- `200`: Successful Response


## `/api/users/`

### GET

- **Описание:** Read Users

#### Ответы:

- `200`: Successful Response


### POST

- **Описание:** Create User

#### Тело запроса:

```json
пример данных...
```

#### Ответы:

- `201`: Successful Response
- `422`: Validation Error


## `/api/users/{user_id}`

### GET

- **Описание:** Read User

#### Параметры:

- `user_id` (path):
#### Ответы:

- `200`: Successful Response
- `422`: Validation Error


### PUT

- **Описание:** Update User

#### Параметры:

- `user_id` (path):
#### Тело запроса:

```json
пример данных...
```

#### Ответы:

- `200`: Successful Response
- `422`: Validation Error


### DELETE

- **Описание:** Delete User

#### Параметры:

- `user_id` (path):
#### Ответы:

- `204`: Successful Response
- `422`: Validation Error


## `/api/laws/`

### GET

- **Описание:** Read Laws

#### Ответы:

- `200`: Successful Response


### POST

- **Описание:** Create Law

#### Тело запроса:

```json
пример данных...
```

#### Ответы:

- `201`: Successful Response
- `422`: Validation Error


## `/api/laws/{law_id}`

### GET

- **Описание:** Read Law

#### Параметры:

- `law_id` (path):
#### Ответы:

- `200`: Successful Response
- `422`: Validation Error


### PUT

- **Описание:** Update Law

#### Параметры:

- `law_id` (path):
#### Тело запроса:

```json
пример данных...
```

#### Ответы:

- `200`: Successful Response
- `422`: Validation Error


### DELETE

- **Описание:** Delete Law

#### Параметры:

- `law_id` (path):
#### Ответы:

- `204`: Successful Response
- `422`: Validation Error


## `/api/decisions/`

### GET

- **Описание:** Read Decisions

#### Ответы:

- `200`: Successful Response


### POST

- **Описание:** Create Decision

#### Тело запроса:

```json
пример данных...
```

#### Ответы:

- `201`: Successful Response
- `422`: Validation Error


## `/api/decisions/{decision_id}`

### GET

- **Описание:** Read Decision

#### Параметры:

- `decision_id` (path):
#### Ответы:

- `200`: Successful Response
- `422`: Validation Error


### PUT

- **Описание:** Update Decision

#### Параметры:

- `decision_id` (path):
#### Тело запроса:

```json
пример данных...
```

#### Ответы:

- `200`: Successful Response
- `422`: Validation Error


### DELETE

- **Описание:** Delete Decision

#### Параметры:

- `decision_id` (path):
#### Ответы:

- `204`: Successful Response
- `422`: Validation Error
