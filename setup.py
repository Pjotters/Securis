from setuptools import setup, find_packages

setup(
    name="securis",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'Flask==2.0.1',
        'Werkzeug==2.0.1',
        'opencv-python-headless==4.5.3.56',
        'numpy>=1.19.3,<1.23.0',
        'protobuf==3.20.3',
        'tensorflow-cpu==2.7.0',
        'gunicorn==20.1.0',
        'flask-swagger-ui==4.11.1',
        'flask-cors==3.0.10',
        'scipy==1.7.3'
    ],
) 