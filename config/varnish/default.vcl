# A heavily customized VCL to support WordPress
# Some items of note:
# Supports https
# Supports admin cookies for wp-admin
# Caches everything
# Support for custom error html page
vcl 4.0;
import directors;
import std;

# Assumed 'wordpress' host, this can be docker servicename
backend default {
    .host = "wordpress";
    .port = "80";
}

acl purge {
    "localhost";
}

sub vcl_recv {
    if (req.url ~ "^/(wp-admin|wp-login)") {
        return (pass);
    }

    set req.http.cookie = regsuball(req.http.cookie, "wp-settings-\d+=[^;]+(; )?", "");
    set req.http.cookie = regsuball(req.http.cookie, "wp-settings-time-\d+=[^;]+(; )?", "");
    set req.http.cookie = regsuball(req.http.cookie, "wordpress_test_cookie=[^;]+(; )?", "");
    if (req.http.cookie == "") {
        unset req.http.cookie;
    }

    if (req.method == "PURGE") {
        if (client.ip !~ purge) {
            return (synth(405));
        } else {
            if (req.http.X-Purge-Method == "regex") {
                ban("req.url ~ " + req.url + " &amp;&amp; req.http.host ~ " + req.http.host);
                return (synth(200, "Banned."));
            } else {
                return (purge);
            }
        }
    }
}

sub vcl_backend_response {
    if (beresp.ttl == 120s) {
        set beresp.ttl = 1h;
    }
}
