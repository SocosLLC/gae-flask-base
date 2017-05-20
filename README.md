# GAE Flask Web Base

## Getting Started

Run `./setup.sh`. It'll install some npm dependencies, create a Python
virtualenv, and compile assets.

Run `./dev_server.sh start` to start the dev server at `localhost:8080`.

`./run_tests.sh` does what it says on the tin.


## Environments

There are three environments: TEST, DEV, and PROD. Since GAE doesn't
support environment variables, you switch between them by symlinking
`src/application/env_conf.py` to the file in `src/application/config/`
that you'd like.


## Assets

Libs are managed with bower. Put your own JS and CSS in
`src/application/assets/`. These files get compiled by executing
`src/assets.py`, putting artifacts in `src/application/static/`.


## Credit

Made with love by the eng team at [Socos LLC](http://www.socoslearning.com)

