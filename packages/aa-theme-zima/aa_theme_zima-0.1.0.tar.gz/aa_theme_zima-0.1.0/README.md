# Alliance Auth Zima Theme

## Installation

```shell
pip install git+https://gitlab.com/zima-corp/aa-theme-zima.git
```

Now open your `local.py` and add the following right below your `INSTALLED_APPS`:
```python
# Zima Theme - https://gitlab.com/zima-corp/aa-theme-zima
INSTALLED_APPS.insert(0, "aa_theme_zima")
```

After installation, run the command:
```shell
python manage.py collectstatic
```

## Upgrade

```shell
python manage.py collectstatic
```

**Important**

If you are using [aa-gdpr](https://gitlab.com/tactical-supremacy/aa-gdpr), the template stuff needs to be **after** the `aa-gdpr`
entry, like this:

```python
# GDPR Compliance
INSTALLED_APPS.insert(0, "aagdpr")
AVOID_CDN = True


# Zima Theme - https://gitlab.com/zima-corp/aa-theme-zima
INSTALLED_APPS.insert(0, "aa_theme_zima")
```
