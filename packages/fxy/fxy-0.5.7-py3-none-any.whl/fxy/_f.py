# iSympy+

try:
    import sympy
    isympy = sympy.interactive.session.preexec_source
    extras = ["a, b, c, d = symbols('a b c d')"]
    lines = isympy.split('\n')
    command = '\n'.join(lines[:-2] + extras + lines[-2:])
    exec(command)
    if True:
        print(command)
except:
    pass
