from setuptools import setup, find_packages

# Lee el contenido del README.md para la descripción larga
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="BKLibOra",  # Nombre del paquete
    version="0.3.2",  # Versión incrementada para reflejar las nuevas funcionalidades
    author="Elieser Castro",
    author_email="bkelidireccion@gmail.com",
    description=(
        "Una librería que utiliza SQLAlchemy y otras dependencias "
        "para generar managers y models que permiten consultar bases de datos Oracle."
    ),
    long_description=long_description,  # Descripción larga desde README.md
    long_description_content_type="text/markdown",
    url="https://github.com/theleerise/BKLibOra.git",
    license="Personal Use Only",
    classifiers=[
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries",
    ],
    packages=find_packages(),  # Encuentra todos los subpaquetes automáticamente
    python_requires=">=3.10",  # Versión mínima de Python
    install_requires=[
        "cffi>=1.17.1",
        "cryptography>=44.0.2",
        "cx_Oracle>=8.3.0",
        "greenlet>=3.1.1",
        "oracledb>=3.1.0",
        "pycparser>=2.22",
        "SQLAlchemy>=2.0.40",
        # "setuptools==78.1.0",
        "typing_extensions>=4.13.2",
    ],
    include_package_data=True,  # Incluye archivos adicionales en MANIFEST.in
    project_urls={
        "Source": "https://github.com/theleerise/BKLibOra.git",
        "Bug Tracker": "https://github.com/theleerise/BKLibOra/issues",
    },
)
