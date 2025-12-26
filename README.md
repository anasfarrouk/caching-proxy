##Caching Proxy Server

This is a caching proxy server made using python.

The server act as a proxy between the client and the host, while also caching responses to decrease latency and reduce traffic cost.

**Usage:**
`python caching-proxy.py --host http://dummyjson.com --port 3000`

If the response is coming from cache, the client receive the following additional header:
`X-Cache:HIT`

If the reponse isn't cached, client receive the following additional header:
`X-Cache:MISS`

Hope you find this program usefull. 🖖

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
