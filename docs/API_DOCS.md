# 📖 API Documentation

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "Legal Assistant Arbitrage API",
    "description": "Legal Assistant Arbitrage API",
    "version": "1.0.0"
  },
  "paths": {
    "/api/health": {
      "get": {
        "tags": [
          "health",
          "system"
        ],
        "summary": "Health",
        "operationId": "health_api_health_get",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {}
              }
            }
          }
        }
      }
    },
    "/api/users/": {
      "get": {
        "tags": [
          "users"
        ],
        "summary": "Read Users",
        "operationId": "read_users_api_users__get",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "items": {
                    "$ref": "#/components/schemas/User"
                  },
                  "type": "array",
                  "title": "Response Read Users Api Users  Get"
                }
              }
            }
          }
        }
      },
      "post": {
        "tags": [
          "users"
        ],
        "summary": "Create User",
        "operationId": "create_user_api_users__post",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/UserCreate"
              }
            }
          },
          "required": true
        },
        "responses": {
          "201": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/User"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/users/{user_id}": {
      "delete": {
        "tags": [
          "users"
        ],
        "summary": "Delete User",
        "operationId": "delete_user_api_users__user_id__delete",
        "parameters": [
          {
            "name": "user_id",
            "in": "path",
            "required": true,
            "schema": {
              "type": "integer",
              "title": "User Id"
            }
          }
        ],
        "responses": {
          "204": {
            "description": "Successful Response"
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/laws/": {
      "get": {
        "tags": [
          "laws"
        ],
        "summary": "Read Laws",
        "operationId": "read_laws_api_laws__get",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "items": {
                    "$ref": "#/components/schemas/Law"
                  },
                  "type": "array",
                  "title": "Response Read Laws Api Laws  Get"
                }
              }
            }
          }
        }
      },
      "post": {
        "tags": [
          "laws"
        ],
        "summary": "Create Law",
        "operationId": "create_law_api_laws__post",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/LawCreate"
              }
            }
          },
          "required": true
        },
        "responses": {
          "201": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Law"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/laws/{law_id}": {
      "delete": {
        "tags": [
          "laws"
        ],
        "summary": "Delete Law",
        "operationId": "delete_law_api_laws__law_id__delete",
        "parameters": [
          {
            "name": "law_id",
            "in": "path",
            "required": true,
            "schema": {
              "type": "integer",
              "title": "Law Id"
            }
          }
        ],
        "responses": {
          "204": {
            "description": "Successful Response"
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/decisions/": {
      "get": {
        "tags": [
          "decisions"
        ],
        "summary": "Read Decisions",
        "operationId": "read_decisions_api_decisions__get",
        "responses": {
          "200": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "items": {
                    "$ref": "#/components/schemas/Decision"
                  },
                  "type": "array",
                  "title": "Response Read Decisions Api Decisions  Get"
                }
              }
            }
          }
        }
      },
      "post": {
        "tags": [
          "decisions"
        ],
        "summary": "Create Decision",
        "operationId": "create_decision_api_decisions__post",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "$ref": "#/components/schemas/DecisionCreate"
              }
            }
          },
          "required": true
        },
        "responses": {
          "201": {
            "description": "Successful Response",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/Decision"
                }
              }
            }
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    },
    "/api/decisions/{decision_id}": {
      "delete": {
        "tags": [
          "decisions"
        ],
        "summary": "Delete Decision",
        "operationId": "delete_decision_api_decisions__decision_id__delete",
        "parameters": [
          {
            "name": "decision_id",
            "in": "path",
            "required": true,
            "schema": {
              "type": "integer",
              "title": "Decision Id"
            }
          }
        ],
        "responses": {
          "204": {
            "description": "Successful Response"
          },
          "422": {
            "description": "Validation Error",
            "content": {
              "application/json": {
                "schema": {
                  "$ref": "#/components/schemas/HTTPValidationError"
                }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "Decision": {
        "properties": {
          "case_number": {
            "type": "string",
            "title": "Case Number"
          },
          "court": {
            "type": "string",
            "title": "Court"
          },
          "summary": {
            "type": "string",
            "title": "Summary"
          },
          "id": {
            "type": "integer",
            "title": "Id"
          }
        },
        "type": "object",
        "required": [
          "case_number",
          "court",
          "summary",
          "id"
        ],
        "title": "Decision"
      },
      "DecisionCreate": {
        "properties": {
          "case_number": {
            "type": "string",
            "title": "Case Number"
          },
          "court": {
            "type": "string",
            "title": "Court"
          },
          "summary": {
            "type": "string",
            "title": "Summary"
          }
        },
        "type": "object",
        "required": [
          "case_number",
          "court",
          "summary"
        ],
        "title": "DecisionCreate"
      },
      "HTTPValidationError": {
        "properties": {
          "detail": {
            "items": {
              "$ref": "#/components/schemas/ValidationError"
            },
            "type": "array",
            "title": "Detail"
          }
        },
        "type": "object",
        "title": "HTTPValidationError"
      },
      "Law": {
        "properties": {
          "code": {
            "type": "string",
            "title": "Code"
          },
          "article": {
            "type": "string",
            "title": "Article"
          },
          "title": {
            "type": "string",
            "title": "Title"
          },
          "id": {
            "type": "integer",
            "title": "Id"
          }
        },
        "type": "object",
        "required": [
          "code",
          "article",
          "title",
          "id"
        ],
        "title": "Law"
      },
      "LawCreate": {
        "properties": {
          "code": {
            "type": "string",
            "title": "Code"
          },
          "article": {
            "type": "string",
            "title": "Article"
          },
          "title": {
            "type": "string",
            "title": "Title"
          }
        },
        "type": "object",
        "required": [
          "code",
          "article",
          "title"
        ],
        "title": "LawCreate"
      },
      "User": {
        "properties": {
          "username": {
            "type": "string",
            "title": "Username"
          },
          "role": {
            "type": "string",
            "title": "Role"
          },
          "id": {
            "type": "integer",
            "title": "Id"
          }
        },
        "type": "object",
        "required": [
          "username",
          "role",
          "id"
        ],
        "title": "User"
      },
      "UserCreate": {
        "properties": {
          "username": {
            "type": "string",
            "title": "Username"
          },
          "role": {
            "type": "string",
            "title": "Role"
          },
          "password": {
            "type": "string",
            "title": "Password"
          }
        },
        "type": "object",
        "required": [
          "username",
          "role",
          "password"
        ],
        "title": "UserCreate"
      },
      "ValidationError": {
        "properties": {
          "loc": {
            "items": {
              "anyOf": [
                {
                  "type": "string"
                },
                {
                  "type": "integer"
                }
              ]
            },
            "type": "array",
            "title": "Location"
          },
          "msg": {
            "type": "string",
            "title": "Message"
          },
          "type": {
            "type": "string",
            "title": "Error Type"
          }
        },
        "type": "object",
        "required": [
          "loc",
          "msg",
          "type"
        ],
        "title": "ValidationError"
      }
    }
  }
}
```
