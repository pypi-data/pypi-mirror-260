from setuptools import setup, find_packages

setup(
    name='boxpay_checkout_sdk', 
    version='1.0.0',  
    packages=find_packages(),  
    install_requires=[
        'requests', 
        'pydantic'
    ],
    python_requires='>=3.6', 
)