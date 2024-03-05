<div align="center">
    <img src="https://user-images.githubusercontent.com/9326700/282852138-160f32e9-e6cf-495f-b39d-99891602acf9.png" alt="Niquests Logo"/>
</div>

**Niquests** is a simple, yet elegant, HTTP library. It is a drop-in replacement for **Requests**, which is under feature freeze.

Niquests, is the “**Safest**, **Fastest[^10]**, **Easiest**, and **Most advanced**” Python HTTP Client. Production Ready!

✔️ **Try before you switch:** [See Multiplexed in Action](https://replit.com/@ahmedtahri4/Python#main.py)<br>
📖 **See why you should switch:** [Read about 10 reasons why](https://medium.com/dev-genius/10-reasons-you-should-quit-your-http-client-98fd4c94bef3)

<details>
  <summary>👆 <b>Look at the feature table comparison</b> against <i>requests, httpx and aiohttp</i>!</summary>

| Feature                             | niquests | requests  |     httpx     | aiohttp       |
|-------------------------------------|:--------:|:---------:|:-------------:|---------------|
| `HTTP/1.1`                          |    ✅     |     ✅     |       ✅       | ✅             |
| `HTTP/2`                            |    ✅     |     ❌     |     ✅[^7]     | ❌             |
| `HTTP/3 over QUIC`                  |    ✅     |     ❌     |       ❌       | ❌             |
| `Synchronous`                       |    ✅     |     ✅     |       ✅       | ❌             |
| `Asynchronous`                      |    ✅     |     ❌     |       ✅       | ✅             |
| `Thread Safe`                       |    ✅     |     ✅     |     ❌[^5]     | _N/A_[^1]     |
| `Task Safe`                         |    ✅     | _N/A_[^2] |       ✅       | ✅             |
| `OS Trust Store`                    |    ✅     |     ❌     |       ❌       | ❌             |
| `Multiplexing`                      |    ✅     |     ❌     | _Limited_[^3] | ❌             |
| `DNSSEC`                            |  ✅[^11]  |     ❌     |       ❌       | ❌             |
| `Customizable DNS Resolution`       |    ✅     |     ❌     |       ❌       | ✅             |
| `DNS over HTTPS`                    |    ✅     |     ❌     |       ❌       | ❌             |
| `DNS over QUIC`                     |    ✅     |     ❌     |       ❌       | ❌             |
| `DNS over TLS`                      |    ✅     |     ❌     |       ❌       | ❌             |
| `Network Fine Tuning & Inspect`     |    ✅     |     ❌     | _Limited_[^6] | _Limited_[^6] |
| `Certificate Revocation Protection` |    ✅     |     ❌     |       ❌       | ❌             |
| `Session Persistence`               |    ✅     |     ✅     |       ✅       | ✅             |
| `In-memory Certificate CA & mTLS`   |    ✅     |     ❌     | _Limited_[^4] | _Limited_[^4] |
| `SOCKS 4/5 Proxies`                 |    ✅     |     ✅     |       ✅       | ❌             |
| `HTTP/HTTPS Proxies`                |    ✅     |     ✅     |       ✅       | ✅             |
| `TLS-in-TLS Support`                |    ✅     |     ✅     |       ✅       | ✅             |
| `Direct HTTP/3 Negotiation`         |  ✅[^9]   |  N/A[^8]  |    N/A[^8]    | N/A[^8]       |
| `Package / SLSA Signed`             |    ✅     |     ❌     |       ❌       | ✅             |
</details>

[^1]: aiohttp has no support for synchronous request.
[^2]: requests has no support for asynchronous request.
[^3]: while the HTTP/2 connection object can handle concurrent requests, you cannot leverage its true potential.
[^4]: loading client certificate without file can't be done.
[^5]: httpx officially claim to be thread safe but recent tests demonstrate otherwise as of february 2024.
[^6]: they do not expose anything to control network aspects such as IPv4/IPv6 toggles, and timings (e.g. DNS response time, established delay, TLS handshake delay, etc...) and such.
[^7]: while advertised as possible, they refuse to make it the default due to performance issues. as of february 2024 an extra is required to enable it manually.
[^8]: they don't support HTTP/3 at all.
[^9]: you must use a custom DNS resolver so that it can preemptively connect using HTTP/3 over QUIC when remote is compatible.
[^10]: performance measured when leveraging a multiplexed connection with or without uses of any form of concurrency as of november 2023. The research compared `httpx`, `requests`, `aiohttp` against `niquests`.
[^11]: enabled when using a custom DNS resolver.

```python
>>> import niquests
>>> s = niquests.Session(resolver="doh+google://", multiplexed=True)
>>> r = s.get('https://pie.dev/basic-auth/user/pass', auth=('user', 'pass'))
>>> r.status_code
200
>>> r.headers['content-type']
'application/json; charset=utf8'
>>> r.oheaders.content_type.charset
'utf8'
>>> r.encoding
'utf-8'
>>> r.text
'{"authenticated": true, ...'
>>> r.json()
{'authenticated': True, ...}
>>> r
<Response HTTP/3 [200]>
>>> r.ocsp_verified
True
>>> r.conn_info.established_latency
datetime.timedelta(microseconds=38)
```
or using async/await! <small>you'll need to enclose the code within proper async function, see the docs for more.</small>
```python
import niquests
>>> s = niquests.AsyncSession(resolver="doh+google://")
>>> r = await s.get('https://pie.dev/basic-auth/user/pass', auth=('user', 'pass'), stream=True)
>>> r
<Response HTTP/3 [200]>
>>> await r.json()
{'authenticated': True, ...}
```

Niquests allows you to send HTTP requests extremely easily. There’s no need to manually add query strings to your URLs, or to form-encode your `PUT` & `POST` data — just use the `json` method!

[![Downloads](https://static.pepy.tech/badge/niquests/month)](https://pepy.tech/project/niquests)
[![Supported Versions](https://img.shields.io/pypi/pyversions/niquests.svg)](https://pypi.org/project/niquests)

## ✨ Installing Niquests and Supported Versions

Niquests is available on PyPI:

```console
$ python -m pip install niquests
```

Niquests officially supports Python or PyPy 3.7+.

## 🚀 Supported Features & Best–Practices

Niquests is ready for the demands of building scalable, robust and reliable HTTP–speaking applications.

- DNS over HTTPS, DNS over QUIC, DNS over TLS, and DNS over UDP
- Automatic Content Decompression and Decoding
- OS truststore by default, no more certifi!
- OCSP Certificate Revocation Verification
- Advanced connection timings inspection
- In-memory certificates (CAs, and mTLS)
- Browser-style TLS/SSL Verification
- Sessions with Cookie Persistence
- Keep-Alive & Connection Pooling
- International Domains and URLs
- Automatic honoring of `.netrc`
- Basic & Digest Authentication
- Familiar `dict`–like Cookies
- Network settings fine-tuning
- Object-oriented headers
- Multi-part File Uploads
- Chunked HTTP Requests
- Fully type-annotated!
- SOCKS Proxy Support
- Connection Timeouts
- Streaming Downloads
- HTTP/2 by default
- HTTP/3 over QUIC
- Multiplexed!
- Thread-safe!
- DNSSEC!
- Async!

Need something more? Create an issue, we listen.

## 📝 Why did we pursue this?

For many years now, **Requests** has been frozen. Being left in a vegetative state and not evolving, this blocked millions of developers from using more advanced features.

We don't have to reinvent the wheel all over again, HTTP client **Requests** is well established and
really pleasant in its usage. We believe that **Requests** has the most inclusive and developer friendly interfaces.
We intend to keep it that way. As long as we can, long live Niquests!

How about a nice refresher with a mere `CTRL+H` _import requests_ **to** _import niquests as requests_ ?

## 💼 For Enterprise

Professional support for Niquests is available as part of the [Tidelift
Subscription][12]. Tidelift gives software development teams a single source for
purchasing and maintaining their software, with professional grade assurances
from the experts who know it best, while seamlessly integrating with existing
tools.

[12]: https://tidelift.com/subscription/pkg/pypi-niquests?utm_source=pypi-niquests&utm_medium=readme

You may also be interested in unlocking specific advantages by looking at our [GitHub sponsor tiers](https://github.com/sponsors/Ousret).

---

Niquests is a highly improved HTTP client that is based (forked) on Requests. The previous project original author is Kenneth Reitz and actually left the maintenance of Requests years ago.
