# MDHandler
MDH: A model handler systematically handling your machine learning models in a unified way.

## Features
When building machine learning models with different strategies, tuning large amounts of hyper-parameters, MDH helps you easily organize these models.

MDH provides 2 main features, **model handling**, and **tensorboard binding**.

### Model handler
MDH supports the following operations.

1. Saving models with different configurations.
  Technically, MDH hashes models' configurations, storing the mapping in a hash table, and build a directory for storing those models.

2. Selecting models in an interactive way.
  MDH provides an interface to load / choose / select models. The hashing mechanism implicitly works in the package, and one could easily choosing models according to their configurations.

### Tensorboard Binder

MDH also provides an interactive command line program helping you bind multiple tensorboard processes in one program.

## Installation

