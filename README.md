Cross-compiling Rust for the Raspberry Pi
======

This is a template repository to cross-compile Rust applications for a Raspberry Pi target more
easily. I have only found bits and pieces in the Internet on how to properly do this, and
this repository is a result of gathering those and packaging them into a template repository.
I specifically targetted debugging with the command line and with VS Code as those
tools are most commonly used in Rust development. The instrutions provided here have been
tested on Linux (Ubuntu 21.04) and Windows 10, but I really recommend to use a Linux
development hosted when developing anything for an Embedded Linux board.

If you are only interested in remotely running your applications and relying on printouts, LEDs or
other means to debug your software, this repository allows to do this more conveniently as well.

If you have not set up the prerequisites yet, [set them up first](#prerequisites).
This template project can in principle be adapted to other Embedded Linux boards easily.
You can tweak the `DEFAULT_*` parameters in the `bld-deploy-remote.py` script and in the
`def-config.toml` file to do this.

# Build with `cargo`

This is based on [this excellent guide](https://chacin.dev/blog/cross-compiling-rust-for-the-raspberry-pi/).
Make sure you have installed a Raspberry Pi cross-compiler and that you can use the cross-toolchain
linker, for example by running `arm-linux-gnueabihf-gcc -v` or `armv8-rpi4-linux-gnueabihf-gcc -v`.

If this works, you can build the debug image with `cargo`:

```sh
cargo build
```

You can test your application manually by transferring it to the Raspberry Pi and then running it.
You can use the folllowing command sequence, adapting the username and ssh address to your needs:

```sh
scp target/armv7-unknown-linux-gnueabihf/debug/rpi-rs-crosscompile pi@raspberrypi.local:/tmp
ssh pi@raspberrypi.local
/tmp/rpi-rs-crosscompile
```

# Run on Raspberry Pi

This is the automation of the steps specified above.
If you configured the runner correctly, it is sufficient to use `cargo run`.
You can also use the following commands

**Unix**

```sh
python3 bld-deploy-remote.py -d -t -r
```

**Windows**

```sh
py bld-deploy-remote.py -d -t -r
```

# Debug on Raspberry Pi

You can also debug your application in the command line or with VS code. There are different ways
to do this. Make sure you have a GDB application like `gdb-multiarch` or `arm-linux-gnueabihf-gdb`
installed and pass it to the `bld-deploy-remote.py` script with the `--gdb` argument.
You can also do this in the `.cargo/config.toml` file.

## Debug on command line

If you selected the following runners in your `.cargo/config.toml`

**Windows**

```toml
runner = "py bld-deploy-remote.py -t -d -s --gdb arm-linux-gnueabihf-gdb --source"
```

**Unix**

```toml
runner = "python3 bld-deploy-remote.py -t -d -s --source"
```

You can use `cargo run` to debug your application in the command line.
Otherwise, you can call `bld-deploy-remote.py` with the `-b -t -d -s <application> <cargo flags>`
arguments to do this.

## Debug with VS Code, `gdbserver` started by VS Code

Make sure that you can build and run your application remotely first like specified above.
A `launch.json` file was provided to automatically lauch the application with `gdbserver`
remotely.

Make sure you installed the `CodeLLDB` plugin for VS Code first. Then go to the Run & Debug Tab and
use the `Remote Debugging with Server` configuration to debug your application.

## Debug with VS Code, `gdbserver` started externally

This setup is similar to the one above but requires the user to always start a GDB server
in a separate terminal. The good thing about this configuration is that you also get the debug
output of the debugged application.

Make sure to select of the following runners in your `.cargo/config.toml`

**Windows**

```toml
runner = "py bld-deploy-remote.py -t -d --source"
```

**Unix**

```toml
runner = "python3 bld-deploy-remote.py -t -d --source"
```

1. Use `cargo run` in a separate terminal to transfer the application and start the GDB server on
   the Raspberry Pi.
2. Use the `Remote Debugging with Server` configuration in the Run & Debug Tab to debug your
   application

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

   **Unix**: You can download one built with crosstool-ng from
   [here](https://www.dropbox.com/sh/gn9bo472yalknra/AABOghC1ym1CmjL8_XZSzGdma?dl=0).

   **Windows**: It is recommended to install the toolchain from
   [SysProgs](https://gnutoolchains.com/raspberry/)

4. Copy the `.cargo/def-config.toml` file to `.cargo/config.toml` and then adapt it to your needs
   to have a starting configuration for the Raspberry Pi. Set the runners and the linker application
   accordingly depending on whether you want to run or debug the application with `cargo run`
   and which toolchain you installed

5. Linux: Install `sshpass`

   ```sh
   sudo apt-get install sshpass
   ```

   It is recommended to [install the SSH key](https://www.ssh.com/academy/ssh/copy-id) of the local
   development machine on the Raspberry Pi

5. Linux: It is recommended to install `gdb-multiarch`.

   On Ubuntu

   ```sh
   sudo apt-get install gdb-multiarch
   ```

6. It is recommended to install [Python 3.8 or higher](https://www.python.org/downloads/).
   Otherwise, the `bld-deploy-remote.py` script, which automates a lot of manual commands, can not
   be used.

## Using VS Code

For Rust development, it is recommended to install the
[Rust Analyzer](https://marketplace.visualstudio.com/items?itemName=matklad.rust-analyzer)
For debugging, install the
[CodeLLDB extension](https://marketplace.visualstudio.com/items?itemName=vadimcn.vscode-lldb).
