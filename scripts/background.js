
    var config = {
            mode: "fixed_servers",
            rules: {
                singleProxy: {
                    scheme: "http",
                    host: "us-ca.proxymesh.com",
                    port: parseInt("31280")
                },
                bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    chrome.webRequest.onAuthRequired.addListener(
        function(details, callbackFn) {
            callbackFn({
                authCredentials: {
                    username: "rxtxk_",
                    password: "@Rtk123321"
                }
            });
        },
        {urls: ["<all_urls>"]},
        ["blocking"]
    );
    