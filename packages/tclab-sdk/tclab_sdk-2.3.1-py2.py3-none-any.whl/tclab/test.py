from blessed import Terminal
term=Terminal()

with term.cbreak():
    val = term.inkey()
    print(val.name=='KEY_ENTER')
    print(type(val))
