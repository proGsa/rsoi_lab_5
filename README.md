# Лабораторная работа #5

![GitHub Classroom Workflow](../../workflows/GitHub%20Classroom%20Workflow/badge.svg?branch=master)

## OAuth2 Authorization

### Формулировка

На базе [Лабораторной работы #4](https://github.com/bmstu-rsoi/lab2-template) реализовать OAuth2 token-based
авторизацию.

* Для авторизации использовать OpenID Connect, в роли Identity Provider использовать стороннее решение.
* На Identity Provider настроить
  использование [Resource Owner Password flow](https://auth0.com/docs/authorization/flows/resource-owner-password-flow)
  (в одном запросе передается `clientId`, `clientSecret`, `username`, `password`).
* Все методы `/api/**` (кроме `/api/v1/authorize` и `/api/v1/callback`) на всех сервисах закрыть token-based
  авторизацией.
* В качестве токена использовать [JWT](https://jwt.io/introduction), для валидации токена
  использовать [JWKs](https://auth0.com/docs/security/tokens/json-web-tokens/json-web-key-sets), _запрос к Identity
  Provider делать не нужно_.
* JWT токен пробрасывать между сервисами, при получении запроса валидацию токена так же реализовать через JWKs.
* Убрать заголовок `X-User-Name` и получать пользователя из JWT-токена.
* Если авторизация некорректная (отсутствие токена, ошибка валидации JWT токена, закончилось время жизни токена
  (поле `exp` в payload)), то отдавать 401 ошибку.
* В `scope` достаточно указывать `openid profile email`.

### Требования

1. Для автоматических прогонов тестов в файле [autograding.json](.github/classroom/autograding.json)
   и [classroom.yml](.github/workflows/classroom.yml) заменить `<variant>` на ваш вариант.
1. Код хранить на Github, для сборки использовать Github Actions.
1. Каждый сервис должен быть завернут в docker.
1. В classroom.yml дописать шаги на сборку, прогон unit-тестов.

### Пояснения

1. В роли Identity Provider можно использовать любое решение, вот несколько рабочих вариантов:
    1. [Okta](https://developer.okta.com/docs/guides/)
    2. [Auth0](https://auth0.com/developers)
2. Для получения metadata для OpenID Connect можно
   использовать [Well-Known URI](https://auth0.com/docs/security/tokens/json-web-tokens/locate-json-web-key-sets):
   `https://[base-server-url]/.well-known/openid-configuration`.
3. Из Well-Known metadata можно получить Issuer URI и JWKs URI.
4. Для реализации OAuth2 можно использовать сторонние библиотеки.

### Прием задания

1. При получении задания у вас создается fork этого репозитория для вашего пользователя.
2. После того как все тесты успешно завершатся, в Github Classroom на Dashboard будет отмечено успешное выполнение
   тестов.

### Варианты заданий

Распределение вариантов заданий аналогично [ЛР #2](https://github.com/bmstu-rsoi/lab2-template).


AUTH0_DOMAIN: library-auth.uk.auth0.com
AUTH0_ISSUER: https://library-auth.uk.auth0.com/
AUTH0_AUDIENCE: https://library-api
JWKS_URL: https://library-auth.uk.auth0.com/.well-known/jwks.json


Domain = library-auth.uk.auth0.com
Client ID = diBoTxvs6RPJjxtew1gnR7KVAKYtxDw5
Client Secret = 6rNF0n18lnIptnLzyJvNIyjeFu5e3-zxIyevJRdDuzecZhCdcVdS1jceuf3b7YIc

test@test.com
pass =qudsu6-qyjcyW-wegzos

Identifier  https://library-api

https://library-auth.uk.auth0.com/.well-known/openid-configuration

"issuer":"https://library-auth.uk.auth0.com/"
"jwks_uri":"https://library-auth.uk.auth0.com/.well-known/jwks.json"
"token_endpoint":"https://library-auth.uk.auth0.com/oauth/token"

"access_token":"eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaXNzIjoiaHR0cHM6Ly9saWJyYXJ5LWF1dGgudWsuYXV0aDAuY29tLyJ9..dGMhWtQt40ZN-EB0.Dk6av2KFsvL7pknDK_giMUp7sh7QzI7Yf830gWD2vKopaZGffFybhvijf1GhOZTWzoNslCQQKMVlZijveu6g7fk7UimvtvmGounVrpzwXJcZIhxuVgpe0hfH99xvuYwFWIAoZ4DfyJV1dAZ7vJBlX9arQC3sASVxq1t57AjTPf0HfPVOsOzLg3Lkk_m7GkoqbMwg22Rzj5Voe9oxY_PnRvIGB0isyv1sopkmWDboQ3JsG_u7lxb0KSrET8iHV3zdSLW41coOYQ0x8wAnORe3b_xdzBk-e1JSi16yhZRvXTimyLqjSr2UT16p7AYbpAouBUQJ2WdopXqNKjl-KCmDPfXO4A.iiFtKyZSJuVaQpErwADigg",
"id_token":"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkJ5VFVpZzNmcjJSQlRMdFBKTHU0cSJ9.eyJuaWNrbmFtZSI6InRlc3QiLCJuYW1lIjoidGVzdEB0ZXN0LmNvbSIsInBpY3R1cmUiOiJodHRwczovL3MuZ3JhdmF0YXIuY29tL2F2YXRhci9iNjQyYjQyMTdiMzRiMWU4ZDNiZDkxNWZjNjVjNDQ1Mj9zPTQ4MCZyPXBnJmQ9aHR0cHMlM0ElMkYlMkZjZG4uYXV0aDAuY29tJTJGYXZhdGFycyUyRnRlLnBuZyIsInVwZGF0ZWRfYXQiOiIyMDI2LTEwLTIzVDIyOjU0OjQxLjgxNFoiLCJlbWFpbCI6InRlc3RAdGVzdC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImlzcyI6Imh0dHBzOi8vbGlicmFyeS1hdXRoLnVrLmF1dGgwLmNvbS8iLCJhdWQiOiJkaUJvVHh2czZSUEpqeHRldzFnblI3S1ZBS1l0eER3NSIsInN1YiI6ImF1dGgwfDZhZGJlM2I3MDNkMTdhNmY5ZjhhOGIyNCIsImlhdCI6MTc5Mjc5NjA4MSwiZXhwIjoxNzkyODMyMDgxfQ.ogTn2ikEk_JcZfRA9htEBuDANPER1U5y2tm2LaOlIDbSR4KRzfPWRaZEga1l9MOY1VVwuSiEFQrfMFhnwBjK_odUmrtWi7OYF11e0pTmljkwCBkGibxv1HewEefvHr3VaNulbdXSTxsiiXv40Us12hPvj3vdFBqdVCWJpt4m9Jd21wbKcmwcTGPffG1EZUSKr6i3lU4Kgj7zqYxTRHnVA3xQb2PpXZXqK1gqaFsEW4IiOSL46g7SckUrFGyKpGLddiepvdLajlPX4EQw819LGytRT-R_XZMQMLB5lfK5lOzYw8-fGGx9blnrZZwMeC_xFwpWA2W1RUB3NDLJPiw1AQ",
"scope":"openid profile email",
"expires_in":86400,
"token_type":"Bearer" 


curl -i \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkJ5VFVpZzNmcjJSQlRMdFBKTHU0cSJ9.eyJpc3MiOiJodHRwczovL2xpYnJhcnktYXV0aC51ay5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NmFkYmUzYjcwM2QxN2E2ZjlmOGE4YjI0IiwiYXVkIjpbImh0dHBzOi8vbGlicmFyeS1hcGkiLCJodHRwczovL2xpYnJhcnktYXV0aC51ay5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNzkyNzk4ODQxLCJleHAiOjE3OTI4ODUyNDEsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJndHkiOiJwYXNzd29yZCIsImF6cCI6ImRpQm9UeHZzNlJQSmp4dGV3MWduUjdLVkFLWXR4RHc1In0.uETuL9_EI93QLokJOWxU5yRA5Eqy2KV28-cC_GUIuyTc7-PFPDHZqsTKp9D9-iagWzGLvHj9WGlQZ5vBuD1NWWzCdsKG2zgNbcEWsJWecD_0O9PDlhIOoG5KWKs7UVjUGjKL_kavS2Unfxr3kCjS0t0Yc4JaNGVIv1IgLeC5doORLmFajBiYDRYk0t7KnegMTEilzeZXFSzxGwy4QaULHuNTHcWojra5x7WZxmENXjY3MIEr0GqGxbkGD5UABvt5VGaYrTZbcVsjjFLStAjJmyHJPd6lEz4Jyma-3R9ZyaS1TWfpNO5aQAT7xoDoyh4rsxpRb6Bw4NBuCR64PH_nTw" \
  "http://localhost:8080/api/v1/libraries?city=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0&page=1&size=10"

curl --request POST \
  --url 'https://library-auth.uk.auth0.com/oauth/token' \
  --header 'content-type: application/json' \
  --data '{
    "grant_type": "password",
    "client_id": "diBoTxvs6RPJjxtew1gnR7KVAKYtxDw5",
    "client_secret": "6rNF0n18lnIptnLzyJvNIyjeFu5e3-zxIyevJRdDuzecZhCdcVdS1jceuf3b7YIc",
    "username": "test@test.com",
    "password": "qudsu6-qyjcyW-wegzos",
    "audience": "https://library-api",
    "scope": "openid profile email"
  }'