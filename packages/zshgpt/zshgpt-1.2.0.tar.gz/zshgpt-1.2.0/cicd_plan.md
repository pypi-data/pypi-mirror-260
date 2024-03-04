## Plan on how to do CI/CD

Lets say current version is 1.2.3

### New features:
1. Make a new branch.
2. Make changes.
3. Push+merge
4. Github actions will:
    0. Do normal testing etc.
    1. Hatch will bump the minor version to 1.3.3
    2. Git tag with current version
    3. Publish to pypi
    4. merge
