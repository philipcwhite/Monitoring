from web.server import app_vars

def render(file, **kwargs):
    output = ''
    with open(app_vars.app_templates + file, 'r') as f:
        output = f.read()
    for i in kwargs:
        var = '{% ' + i + ' %}'
        if var in output:
            output = output.replace(var, kwargs[i])
    return output
