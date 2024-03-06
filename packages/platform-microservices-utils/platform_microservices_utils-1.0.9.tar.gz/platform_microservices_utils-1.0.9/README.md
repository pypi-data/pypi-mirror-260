```markdown
# Integrating Platform Authentication Module
```
## Step 1: Install the Platform Authentication Module

```bash
pip install platform-microservices-utils
```

## Step 2: Add to Installed Apps

Update your project's  setting in `settings.py`:


## Step 3: Configure Middleware and Create Custom Middleware

```python
MIDDLEWARE = [
    # ...,
    "microservice_utils.middlewares.microservice_token.MicroserviceTokenMiddleware",
    # ...,
]
```


## Step 5: Setting up Environment Variables

To configure your environment for microservice communication, follow these steps:

1. Create a `.env` file in the root directory of your project if it doesn't already exist.

2. Add the following variables to your `.env` file, replacing the placeholder values with your actual configurations:

```dotenv
MICROSERVICE_UAT_HOST=your_uat_host
MICROSERVICE_UAT_PORT=your_uat_port
MICROSERVICE_PROD_HOST=your_prod_host
MICROSERVICE_PROD_PORT=your_prod_port
MICROSERVICE_ENV=UAT
MICROSERVICE_SECRET_KEY="your_secret_key"

```

**Note:** Ensure to replace placeholder values (`<some_secret_key1>`, `<parent_project_secret_key>`) with your actual secret keys.



## .ini file creation

To configure your microservice endpoints, follow these steps:

1. Create a `microservice.ini` file in the root directory of your project.
2. Define your microservice endpoints within the `microservice.ini` file using the following format:

```ini
[Tenant]
tenant_db_config = https://example.com/tenant/config

[Authentication]
auth_pass = https://example.com/authenticate

```
Now, your Django project is integrated with the `platform_microservices_utils` module for additional utilities and functionalities to enhance your project's microservice communication.

