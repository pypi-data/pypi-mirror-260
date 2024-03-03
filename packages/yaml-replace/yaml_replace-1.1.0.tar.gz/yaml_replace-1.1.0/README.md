# yaml-replace

Parse yaml files with variables. 
You can substitute variables in yaml files with values you want to inject.

## Installation

```bash
pip install yaml-replace
```

## Usage & Examples

You can specify a variable in yaml file with `${{ variable_name }}` and then replace it with a value you want to inject.

For example, let's say you have a yaml file `some-yaml-file.yaml` with the following content:

```yaml
# some-yaml-file.yaml
name: GitHub Copilot
description: AI Programming Assistant
version: ${{ version }}
features:
  - name: code generation
    languages_supported: ${{ languages }}
```

In your python code, you can use `yaml-replace` to replace the variables in the yaml file with the values you want to inject:

```python
from yaml_replace import YAMLTemplate

YAMLTemplate.load_from_file('some-yaml-file.yaml').render(
    {
        'version': '1.0.0',
        'languages': ["Python", "JavaScript", "Java", "C++", "C#"],
    }
)
```

The code above will output:

```python
{
  'name': 'GitHub Copilot', 
  'description': 'AI Programming Assistant', 
  'version': '1.0.0', 
  'features': [
    {
      'name': 'code generation', 
      'languages_supported': ['Python', 'JavaScript', 'Java', 'C++', 'C#']
    }
  ]
}
```

You can also use `YAMLTemplate` to load the yaml content from a string:

```python
yaml_content = """
name: GitHub Copilot
description: AI Programming Assistant
version: ${{ version }}
features:
  - name: code generation
    languages_supported: ${{ languages }}
"""

YAMLTemplate(yaml_content).render(
    {
        'version': '1.0.0',
        'languages': ["Python", "JavaScript", "Java", "C++", "C#"],
    }
) # Output is the same as the previous example
```

## Contributing

Any contribution is welcome! Check out [CONTRIBUTING.md](https://github.com/01Joseph-Hwang10/yaml-replace/blob/master/.github/CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](https://github.com/01Joseph-Hwang10/yaml-replace/blob/master/.github/CODE_OF_CONDUCT.md) for more information on how to get started.

## License

`yaml-replace` is licensed under a [MIT License](https://github.com/01Joseph-Hwang10/yaml-replace/blob/master/LICENSE).
