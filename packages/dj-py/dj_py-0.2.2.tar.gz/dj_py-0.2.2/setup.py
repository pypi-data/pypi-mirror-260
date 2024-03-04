# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djpay',
 'djpay.api',
 'djpay.api.authorize',
 'djpay.api.authorize.migrations',
 'djpay.api.authorize.tests',
 'djpay.api.authorize.tests.apis',
 'djpay.api.authorize.tests.core',
 'djpay.api.authorize.tests.models',
 'djpay.api.subscriptions',
 'djpay.utils']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.0.0', 'djangorestframework>=3.9,<4.0', 'requests>=2.7,<3.0']

setup_kwargs = {
    'name': 'dj-py',
    'version': '0.2.2',
    'description': 'REST implementation of Django Paypal Authentication System.',
    'long_description': "- **Django PayPal REST API Integration:**\n- *Building a Secure and Reliable Payment Gateway*\n\n## Description\n\nIn this project, we leverage the power of Django to create a robust REST API for integrating PayPal as a secure payment gateway into your web application. With PayPal's wide adoption and reliability, integrating it into your platform will provide seamless and convenient payment options for your users.\n\n## Key Features\n\n- **User Authentication and Authorization:** Implement a secure authentication system using Django's built-in authentication module to ensure that only authorized users can access and make payments through the PayPal API.\n\n- **PayPal API Integration:** Utilize PayPal's REST API to handle payment transactions securely. Implement endpoints for initiating payments, processing transactions, handling refunds, and managing payment status updates.\n\n- **Error Handling and Validation:** Implement robust error handling and data validation mechanisms to ensure smooth and error-free communication with the PayPal API. Handle various scenarios such as validation errors, network failures, and transaction discrepancies gracefully.\n\n- **Webhooks and Notifications:** Set up webhooks to receive real-time notifications from PayPal regarding payment status changes, refunds, and other relevant events. Use Django's webhook handling capabilities to update your application's database and notify users accordingly.\n\n- **Comprehensive Documentation:** Provide clear and concise documentation on how to use the API endpoints, authenticate requests, handle responses, and troubleshoot common issues. Include code samples, usage examples, and best practices to assist developers in integrating the PayPal REST API into their Django applications.\n\n- **Testing and Deployment:** Develop comprehensive test suites to ensure the functionality and reliability of your API. Implement secure deployment practices, including environment configuration and integration with your chosen hosting provider.\n\nBy the end of this project, you will have a powerful REST API integrated with PayPal, providing your users with a seamless and secure payment experience. With Django's robustness and PayPal's reliability, you can confidently handle payment transactions within your application.\n\n**Note:** It is important to familiarize yourself with PayPal's developer documentation and guidelines to ensure compliance with their API usage policies and security practices.\n",
    'author': 'Brahim024',
    'author_email': 'boughanm6@gmail.com',
    'maintainer': 'brahim boughanm',
    'maintainer_email': 'boughanm6@gmail.com',
    'url': 'https://github.com/brahim024/dj-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
