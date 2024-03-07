from setuptools import setup, find_packages

setup(
    name="aisak",
    version="1.0.9",
    author="Mandela Logan",
    author_email="mandelakorilogan@gmail.com",
    description="AISAK, short for Artificially Intelligent Swiss Army Knife, is a general-purpose AI system comprising various models designed for different tasks. Developed by the AISAK team, one of the models within AISAK is a state-of-the-art language model designed for text generation tasks. This package leverages usage of the model, named AISAK-Assistant, which is fine-tuned on extensive datasets to excel in understanding and interpreting various queries in natural language text.",
    packages=find_packages(),
    install_requires=[
        "accelerate",
        "torch",
		  "transformers",	
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)