from setuptools import setup,find_packages

with open("README.md",'r') as f:
	description = f.read()
	
setup(
	name='navdemo',
	version='0.2',
	author='Your Name',
	author_email='your.email@example.com',
	description='A short description of your package',
	packages=find_packages(),
	install_requires=[
	#add dependencies here.
	#eg. 'numpy>=1.11.1'
	],
	entry_points={
		"console_scripts": [
			"demos = navdemo.main:hello",
		],
	}
)
