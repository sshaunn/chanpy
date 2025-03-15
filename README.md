# chanpy

## add secrets.toml under config
```
secrets.toml

[database]
username = ""
password = ""
host = ""
port = ""

[api_keys]
akshare_token = ""  # 如果akshare需要token
other_data_provider = ""

[jwt]
secret_key = "generate_a_strong_random_key_here"
```