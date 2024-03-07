# KeyPaths

```{include} /_fragments/alpha_notice.md

```

For more information on KeyPaths, see
[KeyPaths and the `_` variable](/concept_explanations/keypaths.md).

---

:::{admonition} Advanced API
:class: tip

While we expect most consumers to use
[the magic `_` variable](/concept_explanations/keypaths.md), we don't
expect many users to need to deal with the `KeyPath` type directly,
unless they are building their own packages on top of the
Hashquery framework.
:::

```{eval-rst}
.. currentmodule:: hashquery

.. autoclass:: hashquery.utils.keypath.keypath.KeyPath
    :members:

.. automodule:: hashquery.utils.keypath.keypath
    :members:
    :exclude-members: KeyPath
```

## Resolving Keypaths

```{eval-rst}
.. currentmodule:: hashquery
.. automodule:: hashquery.utils.keypath.resolve
    :members:

```
