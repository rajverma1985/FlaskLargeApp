Application has a main app package and it has sub packages which constitute of logical
units in the project namely,

app, logicalunit1, logicalunit2, main

main contains all general views
each package has forms and views, main doesn't have any forms (obviously)

IMP: the app __init__ is the place where we initialize all the needed extensions like
flask app, sqlalchemy etc.
