Cross-compiling Rust for the Raspberry Pi
======

# Build with `cargo`

Build debug image:

```sh
cargo build --target armv7-unknown-linux-gnueabihf
```

# Prerequisites

1. Install rust on your development machine using `rustup`

   ```sh
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   ```

2. Install standard library

	```sh
	rustup target add armv7-unknown-linux-gnueabihf
   ```

3. Install a cross-compile toolchain and add it to your path.
   You can download one built with crosstool-ng from
   [here](https://www.dropbox.com/sh/hkn4lw87zr002fh/AAAO-HxFQzfmmPQQ9KVmoooGa?dl=0).

4. Install `sshpass`

   ```sh
   sudo apt-get install sshpass
   ```
