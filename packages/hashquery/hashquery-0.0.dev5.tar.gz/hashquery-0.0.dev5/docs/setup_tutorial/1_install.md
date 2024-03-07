# Installing Hashquery

Hashquery requires Python version 3.6 or above.
We recommend creating a fresh virtual environment for Hashquery, so that it
can't interfere with your other Python projects:

```{code-block} bash
# Creating a virtual env with `conda`
conda create -n hashquery python=3.9.6
conda activate hashquery
```

Hashquery is not currently available on PyPI.
Instead, you’ll link the Hashquery source directory into your Python path
using an [editable pip installation](https://setuptools.pypa.io/en/latest/userguide/development_mode.html).

```bash
pip install -e path/to/hashquery
```

> If you are a Hashboard engineer, this path is inside of the primary repo,
> under `glean/hashquery`.
> If you are not an internal engineer, we will have distributed a zip of
> the source to you directly.
