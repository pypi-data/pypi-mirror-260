"""Setup module for torus package
"""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(name="mathexp",
      version="0.0.2",
      description="Mathematical Experiments",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/JWKennington/mathexp",
      author="J. W. Kennington",
      author_email="jameswkennington@gmail.com",
      classifiers=[
          "Development Status :: 3 - Alpha",
          # Pick your license as you wish
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          "Programming Language :: Python :: 3.10",
          "Programming Language :: Python :: 3 :: Only",
      ],
      keywords="symbolic math, combinatorics, finite groups",
      packages=['maths'],
      python_requires=">=3.7, <4",
      install_requires=["sympy"],
      extras_require={  # Optional
          "dev": ["check-manifest"],
          "test": ["pytest", "pytest-cov"],
      },
      # entry_points={  # Optional
      #     "console_scripts": [
      #         "torus=scripts.torus:main",
      #     ],
      # },
      project_urls={  # Optional
          "Bug Reports": "https://github.com/JWKennington/mathexp/issues",
          "Funding": "https://www.buymeacoffee.com/locallytrivial",
          "Source": "https://github.com/JWKennington/mathexp",
          "Documentation": "https://mathexp.readthedocs.io/en/latest/"
      },
      )
