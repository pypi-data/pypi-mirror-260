from setuptools import setup

setup(
    name='enigma_sarti_luigi',
    version='0.1.0',    
    description='Enigma APS2 Sarti e Luigi',
    url='https://github.com/insper-classroom/aps-2-luigi-e-sarti',
    author='Luigi e Sarti',
    author_email='joaopgs4@al.insper.edu.br',
    packages=['enigma_sarti_luigi'],
    install_requires=[
        "blinker==1.7.0",
        "click==8.1.7",
        "Flask==3.0.2",
        "itsdangerous==2.1.2",
        "Jinja2==3.1.3",
        "MarkupSafe==2.1.5",
        "numpy==1.26.4",
        "Werkzeug==3.0.1",
                      ],

    classifiers=[
    ],
)