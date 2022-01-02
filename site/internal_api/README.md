# Internal API
App contains API endpoints that are for internal use only.
The webserver should be configured to not allow access to these endpoints.
The only way then to access these endpoints would be by directory accessing
the port exposed internally.

## Setup
As an additional safety measure, the API expects messages to be signed with
a JSON Web Token (JWT).

To facilitate this, the app uses a config defined in the `settings.py`.
Add the following to `settings.py`:

```python
JWT = {
    'JWT_SECRET_KEY': os.getenv('JWT_SECRET_KEY'),
    'JWT_ALGORITHM': 'HS256',
    'JWT_EXPIRATION_SECONDS': 3600,
}
```
The environment variable `JWT_SECRET_KEY` is required to be set.
