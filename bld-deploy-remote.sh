#!/bin/bash
pi_user="pi"
pi_addr="raspberrypi.local"
scriptname="deploy-rpi.sh"
app_name="rpi-rs-crosscompile"

read -r -d '' cli_help <<EOD
Raspberry Pi Rust Deployment Helper

Builds the image and can optionally transfer and run it on the target system
as well.

Usage:
    ${scriptname} [flags] [options]

Flags:
    -p, --release           Build production image
    -t, --transfer		    Transfer image to Q7S
    -r, --run               Run the image

Options:
    -f, --sshfile FILE      SSH key file. Otherwise, use password from
                            environmental variable SSHPASS
    -e, --sshenv            Take password from environmental variable
EOD

arg_transfer=n
arg_help=n
arg_run=n
arg_ssh_env=n
arg_ssh_file=n
arg_release=n
sshkey_file=""

while (( "${#}" )); do
case "${1}" in
    -t|--transfer)
        arg_transfer=y
        shift
        ;;
    -h|--help)
        arg_help=y
        shift
        ;;
    -r|--run)
        arg_run=y
        shift
        ;;
    -e|--sshenv)
        arg_ssh_env=y
        shift
        ;;
    -p|--release)
        arg_release=y
        shift
        ;;
    -f|--sshfile)
        arg_ssh_file=y
        if [ "${#}" -ge 2 ]; then
            sshkey_file="${2}"
        else
            echo "Error: Missing argument for ${1}"
            exit 1
        fi
        shift
        ;;
    esac
done

# handle help
if [ ${arg_help} = y ]; then
    echo "${cli_help}"
    exit 0
fi

cargo_opts=""
build_folder="debug"
if [ ${arg_release} = y ]; then
    cargo_opts+="--release"
    build_folder="release"
fi

target="armv7-unknown-linux-gnueabihf"
cargo build ${cargo_opts}

sshpass_args=""
if [ ${arg_ssh_file} = y ]; then
    sshpass_args="-f ${sshkey_file}"
elif [ ${arg_ssh_env} = y ]; then
    sshpass_args="-e"
fi
sshpass_cmd="sshpass ${sshpass_args}"
target_cmd="\"/tmp/${app_name}\""
ssh_target="${pi_user}@${pi_addr}"
if [ ${arg_transfer} = y ]; then
    app_loc="./target/${target}/${build_folder}/${app_name}"
    transfer_cmd="${sshpass_cmd} scp ${app_loc} ${ssh_target}:${target_cmd}"
    echo "Running transfer command: ${transfer_cmd}"
    eval ${transfer_cmd}
fi

if [ ${arg_run} = y ]; then
    run_cmd="${sshpass_cmd} ssh ${ssh_target} ${target_cmd}"
    echo "Running target application: ${run_cmd}"
    eval ${run_cmd}
fi
