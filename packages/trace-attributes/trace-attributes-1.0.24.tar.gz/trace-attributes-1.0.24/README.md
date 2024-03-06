# LangTrace - Trace Attributes

This repository hosts the JSON schema definitions and the generated model code for both Python and TypeScript. It's designed to streamline the development process across different programming languages, ensuring consistency in data structure and validation logic. The repository includes tools for automatically generating model code from JSON schema definitions, simplifying the task of keeping model implementations synchronized with schema changes.

## Repository Structure

```
/
├── schemas/                      # JSON schema definitions
│   └── openai_span_attributes.json
├── scripts/                      # Shell scripts for model generation
│   └── generate_python.sh
├── generated/                    # Generated model code
│   ├── python/                   # Python models
│   └── typescript/               # TypeScript interfaces
├── package.json
├── requirements.txt
├── README.md
└── .gitignore
```

## Prerequisites

Before you begin, make sure you have the following installed on your system:
- Node.js and npm
- Python and pip
- `ts-node` for running TypeScript scripts directly (install globally via `npm install -g ts-node`)
- `datamodel-code-generator` for Python model generation (install via `pip install datamodel-code-generator`)

## Generating Models

### Python Models

To generate Python models from a JSON schema, use the `generate_python.sh` script located in the `scripts` directory. This script takes the path to a JSON schema file as an argument and generates a Python model in the `generated/python` directory.

```sh
./scripts/generate_python.sh schemas/openai_span_attributes.json
```

### TypeScript Interfaces

To generate TypeScript interfaces from a JSON schema, use the `schema_to_interface.ts` script located in the `src/models` directory. This script also takes the path to a JSON schema file as an argument and generates a TypeScript interface in the `generated/typescript` directory.
t
```sh
ts-node scripts/generate_typescript.ts schemas/langtrace_span_attributes.json
ts-node scripts/generate_typescript.ts schemas/openai_span_attributes.json
```

To include instructions for building and uploading your Python package to PyPI, as well as how to automate this process using GitHub Actions, you can update your `README.md` file with the following sections:

---

## Building and Uploading Your Package to PyPI

This guide provides instructions on how to manually build your Python package and upload it to the Python Package Index (PyPI), as well as how to automate this process using GitHub Actions.

### Manual Upload to PyPI

To manually upload your package to PyPI, follow these steps:

### Prerequisites

Ensure you have the latest versions of `setuptools`, `wheel`, and `twine` installed:

```sh
pip install --upgrade setuptools wheel twine
```

### Building Your Package

Navigate to your project root (where `setup.py` is located) and run:

```sh
python setup.py sdist bdist_wheel
```

This command generates distribution archives in the `dist/` directory.

### Uploading Your Package

To upload your package to PyPI, use `twine`:

```sh
twine upload dist/*
```

You'll be prompted for your PyPI username and password. For token-based authentication, your username is `__token__`, and your password is the PyPI token.

### Generating a PyPI Token

1. Log in to your PyPI account.
2. Navigate to **Account Settings** > **API tokens** > **Add API token**.
3. Follow the prompts to generate a new token.
4. Use this token with `twine` for uploading your package.

To update your `README.md` with instructions for building and publishing your TypeScript library to npm, you can include the following sections:

---

## Building and Publishing to npm

This guide outlines the steps to build your TypeScript library and publish it to the npm registry, making it available for installation and use in other projects.

### Prerequisites

Before you begin, ensure you have:

- Node.js and npm installed. [Download here](https://nodejs.org/en/download/).
- An npm account. [Sign up here](https://www.npmjs.com/signup) if you don't have one.
- Logged into npm in your command line. Run `npm login` and follow the prompts.

### Building Your TypeScript Library

1. **Navigate to Your Project Directory** where your `package.json` is located, typically `src/typescript`.

    ```sh
    cd src/typescript
    ```

2. **Install Dependencies** if you haven't already:

    ```sh
    npm install
    ```

3. **Build Your Project** to compile TypeScript files into JavaScript:

    ```sh
    npm run build
    ```

    This step assumes you have a `"build"` script in your `package.json` that runs the TypeScript compiler, typically `"build": "tsc"`.

### Publishing Your Package to npm

1. **Update the `package.json`** to ensure it has the correct `"name"` (scoped if necessary, e.g., `@langtrase/trace-attributes`), `"version"`, and other relevant information.

2. **Build Your Library** as described in the previous section to ensure you have the latest compiled version.

3. **Publish Your Package**:

    ```sh
    npm publish --access public
    ```

    The `--access public` flag is necessary if you're publishing a scoped package and want it to be publicly available.

4. **Verify** that your package is now available on npm by visiting `https://www.npmjs.com/package/@langtrase/trace-attributes` (adjust the URL to match your package name).

## Updating Your Package

If you make changes and wish to publish an updated version of your package:

1. Make your changes and commit them to your repository.
2. Update the `"version"` in your `package.json` following [Semantic Versioning](https://semver.org/).
3. Repeat the build and publish steps.

## Contributing

Contributions are welcome! If you'd like to add a new schema or improve the existing model generation process, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Make your changes.
4. Test your changes to ensure the generated models are correct.
5. Submit a pull request with a clear description of your changes.

## License

This project is licensed under the [MIT License](LICENSE). See the LICENSE file for more details.

---

This README provides a comprehensive overview of the repository, including its purpose, structure, prerequisites for generating models, and guidelines for contributing. Adjust any paths, installation commands, or other details as necessary to fit your project's specific setup and requirements.