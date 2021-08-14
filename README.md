Cross-compiling Rust for the Raspberry PI
======

# Prerequisites

1. Install standard library

	```sh
	rustup target add armv7-unknown-linux-gnueabihf
   ```

2. Install a cross-compile toolchain and add it to your path.
   You can download one built with crosstool-ng from
   [here](https://www.dropbox.com/sh/hkn4lw87zr002fh/AAAO-HxFQzfmmPQQ9KVmoooGa?dl=0).
