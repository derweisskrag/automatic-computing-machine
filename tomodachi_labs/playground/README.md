# Playground

So far, we got 3 playgrounds environment. I did not yet figure out how to store assets, but I think we would use either 

- `playground/shared`
- `./shared/playground` 

For now, it does not matter, as I intended scripts to run from Git Bash terminal:

I created one script for you: `try_manual_config_import.sh`. As long as you run it from `./`, it will run.

## Importing

In this playground, we talked about how to import packages. This can shed some light on how we are going to
organize the codebase. Right now, we can just reuse our deployed package. 

### How did we import?

There were 4 ways:

- deployed package is easily importable
- configure another config & re-read using load_dotenv, while using `pathlib`
- using `importlib.util`, you can load the module, of course, reusing the path to it (pathlib or os.getcwd and then pathlib)
- using the sys.path.

## using dates

This is empty playground for today. I do not add anything, but I plan on using Python built-in module. So, no imports or file problems.

## dsa library testing

This is not empty. It is not necessary either. It was the first package I deployed. You can install it and try yourself. It is okay. Later on,
we are going to refactor again, which means some junk will be removed.

