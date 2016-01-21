# dumbserver 1.0

[![PyPI version](https://badge.fury.io/py/dumbserver.svg)](https://pypi.python.org/pypi/dumbserver/1.0)

dumbserver is specially crafted for mocking responses from multiple systems, extremely useful for functional and integration testing purposes.

dumbserver is built using the  [twisted](https://twistedmatrix.com/trac/) plugin system and can be run as a daemon using `twistd`. 

### Installation

```sh
$ pip install dumbserver
```

### Usage

```sh
$ twistd [options] dumbserver [options]
```

`twistd --help` will list out the options related to `twistd`.

`twistd dumbserver --help` will list out the options related to dumbserver.

##### Options:
  - -e, --expectations=  Comma separated list of expectation files and corresponding port numbers to which it should run. Example: `twistd dumbserver -e /path/to/sample1.yml:8000,/path/to/sample2.yml:8001`
  - -f, --configfile=    The configuration file containing the list of expectation files and corresponding port numbers to which it should run. See -e on how to specify the expectation and port number.
  - --version        Display Twisted version and exit.
  - --help           Display this help and exit.

### Expectation Files

Each file denotes a service that runs on a port and contains a list of requests with corresponding responses. Checkout [examples/sample.yml](https://github.com/varunmulloli/dumbserver/blob/master/examples/sample.yml) to see how to write one.

### License

dumbserver is made available under the MIT license.
The included [LICENSE](https://github.com/varunmulloli/dumbserver/blob/master/LICENSE.txt) file describes this in detail.

### Warranty

  >THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER
  EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
  OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.  THE ENTIRE RISK AS
  TO THE USE OF THIS SOFTWARE IS WITH YOU.

  >IN NO EVENT WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MAY MODIFY
  AND/OR REDISTRIBUTE THE LIBRARY, BE LIABLE TO YOU FOR ANY DAMAGES, EVEN IF
  SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH
  DAMAGES.

Again, see the included [LICENSE](https://github.com/varunmulloli/dumbserver/blob/master/LICENSE.txt) file for specific legal details.
