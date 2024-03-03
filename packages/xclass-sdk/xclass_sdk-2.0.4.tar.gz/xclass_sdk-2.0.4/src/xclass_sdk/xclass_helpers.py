import pystache

def multipartify(data, parent_key=None, formatter: callable = None) -> dict:
    if formatter is None:
        formatter = lambda v: (None, v)  # Multipart representation of value

    if type(data) is not dict:
        return {parent_key: formatter(data)}

    converted = []

    for key, value in data.items():
        current_key = key if parent_key is None else f"{parent_key}[{key}]"
        if type(value) is dict:
            converted.extend(multipartify(value, current_key, formatter).items())
        elif type(value) is list:
            for ind, list_value in enumerate(value):
                iter_key = f"{current_key}[{ind}]"
                converted.extend(multipartify(list_value, iter_key, formatter).items())
        else:
            converted.append((current_key, formatter(value)))

    return dict(converted)

def render_template(template, data):
    """
    Use pystache to render the Mustache template with input data
    """
    renderer = pystache.Renderer()
    html_output = renderer.render(template, data)
    return html_output

def load_template_from_file(template_file):
    """
    Read the Mustache template from an external file
    """
    with open(template_file, "r", encoding="utf-8") as file:
        template = file.read()
    return template
