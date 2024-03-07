import setuptools

with open("README.md", "r") as f:
	long_description = f.read()

setuptools.setup(
	name = "liboqs", #If you are liboqs creator please contact me via telegram @Fun_Dan3 or email dfr34560@gmail.com if you want to take this name.
	version = "0.9.1",
	author = "Fun_Dan3",
	author_email = "dfr34560@gmail.com",
	description = "Unofficial liboqs-python library with precompiled liboqs libraries",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://github.com/FunDan3/liboqs-python-pip/",
	project_urls = {
		"Bug Tracker": "https://github.com/FunDan3/liboqs-python-pip/issues"
	},
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	packages = setuptools.find_packages(where = "src"),
	package_dir = {"": "src"},
	package_data = {"": ["*.dll", "*.so"]},
	python_requires = ">=3.8",
)
