import setuptools

with open("README.md", "rb") as fh:
    long_description = fh.read().decode("utf-8")

setuptools.setup(
    name='chatgpt-bot-utils',
    version='1.0.0',
    url='https://github.com/duliyouxijuzi/chatgpt-bot-utils',
    license='MIT',
    author='duliyouxijuzi',
    author_email='duliyouxijuzi@gmail.com',
    description='使用chatgpt api的机器人工具',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
    ],
    python_requires='>=3.6',
    install_requires=['openai'],
)
