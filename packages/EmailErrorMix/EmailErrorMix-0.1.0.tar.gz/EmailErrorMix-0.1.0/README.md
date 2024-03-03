EmailErrorMix
==========

A Python package for automated error notification emails, enhancing software debugging and maintenance.

Features
--------
- Automatic error detection and notification
- Support for multiple email recipients
- Error tracking and analytics
- Error notification throttling

Installing
--------
To install the library you can just run the following command:

    # Linux/macOS
    pip3 install EmailErrorMix

    # Windows
    pip install EmailErrorMix


Function Example
--------
```python
from EmailErrorMix import ErrorEmailer 

error_emailer = ErrorEmailer(sender_email='',
                             sender_password='', 
                             smtp_server='smtp.gmail.com', 
                             smtp_port=465)

@error_emailer.notify_on_error()
def example_function(x, y):
    return x / y

if __name__ == '__main__':
    result = example_function(1, 0)
```


ContextManager Example
--------
```python
from EmailErrorMix import ErrorEmailer 

error_emailer = ErrorEmailer(sender_email='',
                             sender_password='', 
                             smtp_server='smtp.gmail.com', 
                             smtp_port=465)

if __name__ == '__main__':
    with error_emailer.context_notify_on_error():
        result = 1/0
```