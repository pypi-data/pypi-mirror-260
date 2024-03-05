# akapy

Home to a Python wrapper for the Akamai API.

## How to use?

```python
cloudlet = ak.Cloudlet()
print(cloudlet.get_all())

```

Check out the docs here [remoterabbit.github.io/akapy/](remoterabbit.github.io/akapy/)

<!--TODO: Go through this and add better use cases and how to use-->
Akapy has an authentication class which is passed, when needed, to other classes within Akapy. For most use cases you probably won't need to mess
around with it. The defaults for it are 
