# Contributing

Contributions are welcome! Please ensure that any Rust changes include updated tests and satisfy `cargo fmt`.

- Fork the Project
- Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
- Commit your Changes (`git commit -m 'Add AmazingFeature'`)
- Push to the Branch (`git push origin feature/AmazingFeature`)
- Open a Pull Request

## Get Started

Ready to contribute? Here's how to set up `seedler_repo` for local development.

1. Clone the `seedler_repo` locally.

    ```console
    git clone git+https://github.com/byuirpytooling/seedler.git@main
    cd seedler-repo
    ```

2. Create and activate a uv venv for `seedler_repo`:

    ```console
    uv venv --python 3.14
    source .venv/bin/activate
    ```

3. Install `seedler_repo` python and rust packages locally as editable:

    ```console
    uv pip install -e .
    uv run maturin develop
    ```

4. Use `git` to create a branch for local development and make your changes

5. When you're done making changes, check that your changes conform to any code formatting requirements and pass any tests:

    ```console
    cargo fmt
    ```

6. Commit your changes and open a pull request.

## Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include additional tests if appropriate.
2. If the pull request adds functionality, the docs should be updated.
3. The pull request should work for all currently supported operating systems and versions of Python.

## Code of Conduct

Please note that the `seedler_repo` project is released with a
Code of Conduct [CONDUCT.md](CONDUCT.md). By contributing to this project you agree to abide by its terms.
