# yes-chef

A command-line tool for managing recipes and making shopping lists.

# Installation

Clone this repository, set up a venv, and run

```shell
./install.sh
```

You may need to give the file run permissions with

```shell
chmod +x install.sh
```

# Usage

Initialise a new recipe library in the current folder:

```shell
chef init .
```

Create a new plan (collection of recipes to turn into a shopping list):

```shell
chef new plan 
```

Add a recipe to the plan:

```shell
chef plan <search term> 
```

View the currently planned recipes:

```shell
chef view plan 
```

View the shopping list for the planned recipes:

```shell
chef view list 
```