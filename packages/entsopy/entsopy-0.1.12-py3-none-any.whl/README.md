# entsopy

  Your cli tool for **download data from the** from ENTSO-E transparency platform.

 **Please note that a security token is mandatory for accessing the ENTSO-E API service.** Follow the official [official instructions](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html#_authentication_and_authorisation) to get one.

## Requirements

- **Python 3.11+** [[How to install Python?]](https://www.python.org/)
- **pip** Python package insaller [[How to install pip?]](https://pip.pypa.io/en/stable/installation/)
- For performing requests to entso-e API service you need a **security token**: you can get one by following the [official instructions](https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html#_authentication_and_authorisation).

## Installation

```  0
pip install entsopy
```

Check out the latest entsopy version on pypi: [pypi.org/project/entsopy](https://pypi.org/project/entsopy/)

:warning: If you use Windows make sure to setup properly the following environment variables in your OS:

``` 0
C:\Users\<username>\AppData\Local\Packages\PythonSoftwareFoundation...\LocalCache\local-packages\Python3...\site-packages
```

``` 0
C:\Users\<username>\AppData\Local\Packages\PythonSoftwareFoundation...\LocalCache\local-packages\Python3...\site-packages
```

## Commands

- `entsopy start` for starting the cli app;
- `entsopy reset` for resetting entsopy configuration data;**
  - `entsopy reset security-token` for resetting securiy token;
  - `entsopy reset download-dir` for resetting the folder in which data are downloaded;
  - `entsopy reset log` for resetting the log file;
  - `entsopy reset all` reset complitely the configuration;
- `entsopy log` for manage entsopy logs;**
- `entsopy --help` for seeing the helper.**

## Useful links

- **Ensto-e official website:** <https://www.entsoe.eu/>
- **Ensto-e transparency platform:** <https://transparency.entsoe.eu/>
- **Ensto-e security token:** <https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html#_authentication_and_authorisation>

## License  

This project is licensed under the terms of the MIT license.

## Founding

> Entsopy was funded by the European Union - _NextGenerationEU_, in the framework of the _GRINS - Growing Resilient, INclusive and Sustainable_ project (GRINS PE00000018 – CUP C93C22005270001)
