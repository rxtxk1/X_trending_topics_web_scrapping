from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.proxy import Proxy, ProxyType

# Set up ProxyMesh details
proxy = "us-wa.proxymesh.com:31280"  # Replace with your ProxyMesh proxy URL
proxy_user = "rxtxk_"           # Replace with your ProxyMesh username
proxy_pass = "@Rtk123321"           # Replace with your ProxyMesh password

# Configure the proxy
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"--proxy-server=http://{proxy}")

# Add authentication using an extension
plugin_file = 'proxy_auth_plugin.zip'

with open("manifest.json", "w") as f:
    f.write("""
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Proxy Auth",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """)

with open("background.js", "w") as f:
    f.write(f"""
    var config = {{
            mode: "fixed_servers",
            rules: {{
                singleProxy: {{
                    scheme: "http",
                    host: "{proxy.split(':')[0]}",
                    port: parseInt("{proxy.split(':')[1]}")
                }},
                bypassList: ["localhost"]
            }}
        }};

    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

    chrome.webRequest.onAuthRequired.addListener(
        function(details, callbackFn) {{
            callbackFn({{
                authCredentials: {{
                    username: "{proxy_user}",
                    password: "{proxy_pass}"
                }}
            }});
        }},
        {{urls: ["<all_urls>"]}},
        ["blocking"]
    );
    """)

from zipfile import ZipFile

with ZipFile(plugin_file, 'w') as zp:
    zp.write("manifest.json")
    zp.write("background.js")

chrome_options.add_extension(plugin_file)

# Start the browser with the proxy
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.google.com")
print("Proxy setup successful!")
driver.quit()
