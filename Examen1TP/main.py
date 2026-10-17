from checker import (
    build_url,
    is_https,
    show_response,
    check_site,
    scan_sites,
    check_headers,
    retry_check,
)


# Partea 1: build_url și is_https
print("Partea 1, build_url fără slash:",
      build_url("example.com", "login"))
print("Partea 1, build_url cu slash:",
      build_url("example.com", "/login"))

print("Partea 1, is_https cu HTTPS:",
      is_https("https://example.com"))
print("Partea 1, is_https cu HTTP:",
      is_https("http://example.com"))


# Partea 2: show_response
print("\nPartea 2, site disponibil:")
show_response("https://example.com")

print("Partea 2, răspuns 404:")
show_response("https://httpbin.org/status/404")


# Partea 3: check_site
print("\nPartea 3, site disponibil:")
print(check_site("https://example.com"))

print("Partea 3, adresă inexistentă:")
print(check_site("http://this-site-does-not-exist.invalid"))


# Partea 4: scan_sites
print("\nPartea 4, scanarea site-urilor:")
scan_sites()


# Partea 5: check_headers
print("\nPartea 5, antete de securitate:")
print(check_headers(
    "https://httpbin.org/response-headers"
    "?X-Frame-Options=DENY&X-Content-Type-Options=nosniff"
))

print("Partea 5, site fără antete de securitate:")
print(check_headers("https://httpbin.org/status/200"))


# Partea 6: retry_check
print("\nPartea 6, status 200:")
print(retry_check("https://httpbin.org/status/200"))

print("Partea 6, status 404:")
print(retry_check("https://httpbin.org/status/404"))

print("Partea 6, status 500:")
print(retry_check("https://httpbin.org/status/500"))