# Alliance Auth XIX Theme

## Installation

```shell
sudo su allianceserver
cd
source /home/allianceserver/venv/auth/bin/activate
git clone https://gitlab.com/legion-of-xxdeathxx/aa-theme-xix.git
pip install -e aa-theme-xix/
```

Now open your `local.py` and add the following right below your `INSTALLED_APPS`:
```shell
nano myauth/myauth/settings/local.py
```
```python
# XIX Theme - https://gitlab.com/legion-of-xxdeathxx/aa-theme-xix
INSTALLED_APPS.insert(0, "aa_theme_xix")
```

After installation, run the command:
```shell
python /home/allianceserver/myauth/manage.py collectstatic --noinput
```

**Important**

If you are using [aa-gdpr](https://gitlab.com/tactical-supremacy/aa-gdpr), the template stuff needs to be **after** the `aa-gdpr`
entry, like this:

```python
# GDPR Compliance
INSTALLED_APPS.insert(0, "aagdpr")
AVOID_CDN = True


# XIX Theme - https://gitlab.com/legion-of-xxdeathxx/aa-theme-xix
INSTALLED_APPS.insert(0, "aa_theme_xix")
```


## Updating
```shell
sudo su allianceserver
cd
source /home/allianceserver/venv/auth/bin/activate
cd aa-theme-xix/
git pull
cd ..
pip install -e aa-theme-xix/
```

After updating, run the command:
```shell
python /home/allianceserver/myauth/manage.py collectstatic --noinput
```
