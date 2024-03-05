# RABC Utils
This library provides utility functions for RBAC system.

## APIs

**Utils(token)**

- validate_token() -> boolean
- get_user_roles() -> [user]
- is_user_role_present(role) -> boolean
- get_user_details() -> {}
- validate_with_server(timeout_seconds=20) -> boolean


## EXAMPLE

### Installing the lib
Install the lib with pip install command, supply the flags as below to specify the address of our private ldc_packages index.
`pip install rbac-utils -i http://13.235.135.2:3141/dev/ldc_packages --trusted-host 13.235.135.2`

### Initialise the utils class:
Start by creating an instance of Utils class. Initialise it with a token string.

```python
rbac_utils = Utils(token)
```

### Validating A Token Locally:
Ensures valid 'nbf' claim, 'exp' claim and RBAC signature on the given token.

```python
is_valid = rbac_utils.validate_token() 
```

### Validating A Token From Server:
Ensures valid 'nbf' claim, 'exp' claim and RBAC signature on the given token. Also checks if the token has been invalidated in the RBAC due to other reasons such as change in user's properties that are part of the token payload (Eg: roles, permissions, etc)

```python
is_valid = rbac_utils.validate_with_server()
```

### Getting User Roles From Token:
Get the list of roles defined in the token.

```python
roles = rbac_utils.get_user_roles()
```


### Checking For A Role On The Token:
Check if the given roles is present in the token.

```python
is_role_present = rbac_utils.is_user_role_present('OPS')
```


### Obtaining User Details From A Token:
Obtain user details such (user_id, email and mobile_number) from the token.

```python
user_details = rbac_utils.get_user_details()
```
