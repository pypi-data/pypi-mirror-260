from setuptools import setup

with open('cripto_aps2/requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='cripto_aps2',
    version='0.1.0',    
    description='Biblioteca para criptografia e descriptografia de mensagens',
    url='https://github.com/shuds13/pyexample',
    author='Giovanny Russo',
    author_email='giovannyjrusso@gmail.com',
    license='BSD 2-clause',
    packages=['cripto_aps2'],
    install_requires=["numpy>=1.19.5", "flask>=2.0.1"],
                   
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)

