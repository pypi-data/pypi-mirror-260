<a href="https://envialosimple.com/transaccional"><img src="https://envialosimple.com/images/logo_tr.svg" width="200px"/></a>

# EnvíaloSimple Transaccional - Python SDK

## Requirements

- Python 3.8 or higher
- EnvíaloSimple Transaccional API Key ([Create a demo account for free here](https://envialosimple.com/transaccional))

## Installation

```bash
pip install envialosimple-transaccional
```

## Basic Usage

```python
from envialosimple.transaccional import Transaccional
from envialosimple.transaccional.mail import MailParams

estr = Transaccional(your_api_key)

params = MailParams(
        from_email='no-reply@mycompany.com', 
        from_name='MyCompany Notifications',
        to_email='john.doe@example.com', 
        to_name='John Doe',
        subject='This is a test for {{name}}', 
        html='<h1>HTML emails are cool, {{name}}</h1>', 
        text='Text emails are also cool, {{name}}',
        substitutions={'name': 'John'})

estr.mail.send(params)
```
