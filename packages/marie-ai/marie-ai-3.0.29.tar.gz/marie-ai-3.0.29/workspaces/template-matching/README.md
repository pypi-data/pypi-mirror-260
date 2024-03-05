---
title: Template Matching
sdk: gradio
sdk_version: 1.0.0
app_file: app.py
license: apache-2.0
---

# Template Matching

```shell
streamlit run app.py --server.fileWatcherType none --server.enableXsrfProtection=false
```

## Common errors

```text
AxiosError: Request failed with status code 403
```

Disable XSRF protection in the server by adding the following line to the `application.properties` file.

```bash 
--server.enableXsrfProtection=false
```
