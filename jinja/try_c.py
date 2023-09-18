import yaml
from jinja2 import Template

vals = {"var3": "77777", "VERSION": "2.0"}

str1 = '''var1: val1
var2: val2ccc
var3: {{var1}}-{{var2}}-{{var3}}.txt
'''

t = Template(str1)
c = yaml.safe_load(t.render())

print("\nEX A: Use the string embedded values also for the jinja values ")
print(t.render(c))

print("\nEX B: Use the vals string for the jinja values ")
print(t.render(vals))

print("\nEX C: Read a yaml file that has jinja fields")
with open('templates/y_file') as yaml_template:
    contents = yaml.safe_load(yaml_template)
print(f'Before Jinja content: {type(contents)}   {contents}')
template = Template(str(contents))
rendered_yaml_str = template.render(vals)
print(f'AFTER Jinja content: {rendered_yaml_str}')

template2 = Template(contents)


