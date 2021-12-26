#!/usr/bin/env python3
"""Small portable helper script to build, deply and run a Rust application
on a remote machine, e.g. a Raspberry Pi"""
import argparse
import os
import sys
import platform
import time
from typing import Final


# This script can easily be adapted to other remote machines, Linux boards and
# remote configurations by tweaking / hardcoding these parameter, which generally are constant
# for a given board
DEFAULT_USER_NAME: Final = "pi"
DEFAULT_ADDRESS: Final = "raspberrypi.local"
DEFAULT_TOOLCHAIN: Final = "armv7-unknown-linux-gnueabihf"
DEFAULT_APP_NAME: Final = "rpi-rs-crosscompile"
DEFAULT_TARGET_FOLDER: Final = "/tmp"
DEFAULT_DEBUG_PORT: Final = "17777"
if platform.system() == "Windows":
    DEFAULT_GDB_APP = "arm-none-eabi-gdb"
else:
    DEFAULT_GDB_APP = "gdb-multiarch"


def main():
    bld_deploy_run(parse_arguments())


def parse_arguments():
    desc = (
        "Rust Remote Deployment Helper."
        "Builds the image and can optionally transfer and run "
        "it on the target system as well."
    )
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "-u",
        "--user",
        default=f"{DEFAULT_USER_NAME}",
        help=f"Username for ssh access. Default: {DEFAULT_USER_NAME}",
    )
    parser.add_argument(
        "-a",
        "--address",
        default=f"{DEFAULT_ADDRESS}",
        help=f"Remote SSH address. Default: {DEFAULT_ADDRESS}",
    )
    parser.add_argument(
        "--tc",
        default=f"{DEFAULT_TOOLCHAIN}",
        help=f"Target toolchain. Default: {DEFAULT_TOOLCHAIN}",
    )

    parser.add_argument(
        "--app",
        default=f"{DEFAULT_APP_NAME}",
        help=f"Target appname. Default: {DEFAULT_APP_NAME}",
    )
    parser.add_argument(
        "--source",
        help=f"Target destination path. Default: Built from other arguments",
    )
    parser.add_argument(
        "--dest",
        default=f"{DEFAULT_TARGET_FOLDER}",
        help=f"Target destination path. Default: {DEFAULT_TARGET_FOLDER}",
    )
    parser.add_argument(
        "other", nargs=argparse.REMAINDER, help="Argument forwarded to cargo build"
    )

    parser.add_argument(
        "-b",
        "--build",
        action="store_true",
        help="Build application",
    )
    parser.add_argument(
        "-t",
        "--transfer",
        action="store_true",
        help="Transfer application to remote machine",
    )
    parser.add_argument(
        "-r",
        "--run",
        action="store_true",
        help="Run application on remote machine",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Run gdbserver on remote machine for remote debugging"
    )
    parser.add_argument(
        "-s",
        "--start",
        action="store_true",
        help="Start local GDB session, connecting to the remote GDB server"
    )
    parser.add_argument(
        "-p",
        "--port",
        default=f"{DEFAULT_DEBUG_PORT}",
        help="Port to use for remote debugging"
    )
    parser.add_argument(
        "-e",
        "--sshenv",
        action="store_true",
        help="Take password from environmental variable",
    )
    parser.add_argument(
        "--release",
        action="store_true",
        help="Supply --release to build command",
    )
    parser.add_argument(
        "-f",
        "--sshfile",
        help="SSH key file. Otherwise, use password from environmental variable SSHPASS",
    )
    return parser.parse_args()


def bld_deploy_run(args):
    cargo_opts = ""
    build_folder = "debug"
    if args.release:
        cargo_opts += "--release"
        build_folder = "release"
    for other in args.other:
        cargo_opts += f"{other}"
    sshpass_args = ""
    if args.sshfile:
        sshpass_args = f"-f {args.sshfile}"
    elif args.sshenv:
        sshpass_args = "-e"
    ssh_target_ident = f"{args.user}@{args.address}"
    sshpass_cmd = f"sshpass {sshpass_args}"
    dest_path = f"{args.dest}/{args.app}"
    if not args.source:
        source_path = f"{os.getcwd()}/target/{args.tc}/{build_folder}/{args.app}"
    else:
        source_path = args.source
    build_cmd = f"cargo build {cargo_opts}"
    if args.build:
        print(f"Running build command: {build_cmd}")
        os.system(build_cmd)
    if args.transfer:
        if not os.path.exists(source_path):
            print(f"No application found at {source_path}")
            sys.exit(1)
        scp_target_dest = f'{ssh_target_ident}:"{dest_path}"'
        transfer_cmd = f"{sshpass_cmd} scp {source_path} {scp_target_dest}"
        print(f"Running transfer command: {transfer_cmd}")
        os.system(transfer_cmd)
    if args.run:
        run_cmd = f"{sshpass_cmd} ssh {ssh_target_ident} {dest_path}"
        print(f"Running target application: {run_cmd}")
        os.system(run_cmd)
    elif args.debug:
        # Kill all running gdbserver applications  first
        # Then start the GDB server
        debug_shell_cmd = f"sh -c 'killall -q gdbserver; gdbserver *:{args.port} {dest_path}'"
        # Execute the command above and also set up port forwarding. This allows to connect
        # to localhost:17777 on the local development machine
        debug_cmd = f"{sshpass_cmd} ssh -f -L {args.port}:localhost:{args.port} {ssh_target_ident} \"{debug_shell_cmd}\""
        print(f"Running debug command: {debug_cmd}")
        os.system(debug_cmd)
        if args.start:
            start_cmd = f"{DEFAULT_GDB_APP} -q -x gdb.gdb"
            print(f"Running start command: {start_cmd}")
            os.system(start_cmd)


if __name__ == "__main__":
    main()
