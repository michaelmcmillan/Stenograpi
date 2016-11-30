# Server API

This document describes all the available HTTP endpoints the server exposes.

## POST /api/v1/user/login

### Should return a token if correct credentials are given

**Parameters:**

Key        | Value
---------- | ----------------
`username` | bob@gmail.com
`password` | correct-password


**Headers:**

Key            | Value
-------------- | -------------
`Content-Type` | application/json

#### Response (HTTP status 200)
````javascript
{
  success: true,
  token: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9 [...]'
}
````

### Should return an error if incorrect credentials are given

**Parameters:**

Key        | Value
---------- | -------------
`username` | bob@gmail.com
`password` | wrong-password


**Headers:**

Key            | Value
-------------- | -------------
`Content-Type` | application/json

#### Response (HTTP status 401)
````javascript
{
  success: false,
  error: 'Wrong username or password.'
}
````