#!/bin/bash
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
DEFAULT_TMP_DIR="${SCRIPT_DIR}/qdrant"
QDRANT_TMP_DIR_PREFIX="QDRANT_tmp_"

QDRANT_IMG="docker.io/qdrant/qdrant:latest"
QDRANT_CONTAINER_NAME="qdrantdb"

echo "===== Script to run the QDRANT Vector DB ====="
echo "===== Canceling the script will remove all persistent DB files ====="

function error_exit() {
    echo "Error: $1" >&2
    exit "${2:-1}"
}

function cleanup_and_exit() {
    echo "===== Cleaning up QDRANT files and exiting ====="
    local exit_val=$1
    if [ -z "${QDRANT_DATA_DIR}" ]; then
        echo "cleanup_and_exit(): Temp dir not provided !" >&2
    else
      # Ensure dir exists and starts with prefix
      if [ -d "${QDRANT_DATA_DIR}" ]; then
          QDRANT_TMP_DIR=$(basename "${QDRANT_DATA_DIR}")
          if [[ "${QDRANT_TMP_DIR}" =~ "${QDRANT_TMP_DIR_PREFIX}"* ]]; then
              echo "Cleaning up temporary QDRANT files"
              rm -rf "${QDRANT_DATA_DIR}"
              rmdir "${DEFAULT_TMP_DIR}"
          fi
      fi
    fi

    if [ -n "$CONTAINER_TOOL" ]; then
        # Stop and remove the Qdrant container
        $CONTAINER_TOOL stop "$QDRANT_CONTAINER_NAME"
        $CONTAINER_TOOL rm "$QDRANT_CONTAINER_NAME"
        echo "Qdrant container removed."
    else
        echo "Skipping container cleanup"
    fi
    # Propagate exit value if was provided
    [ -n "${exit_val}" ] && echo "Exit code: ${exit_val}" && exit "$exit_val"
    exit 0
}

check_container_tool() {
    if command -v podman &> /dev/null; then
        command -v podman
    elif command -v docker &> /dev/null; then
        command -v docker
    fi
}


CONTAINER_TOOL=$(check_container_tool)
if [ -n "$CONTAINER_TOOL" ]; then
    echo "Container tool path: $CONTAINER_TOOL"
else
    echo "Neither Podman nor Docker is available on this system."
    exit 1
fi

if [ ! -d "${DEFAULT_TMP_DIR}" ]; then
    mkdir -p "${DEFAULT_TMP_DIR}" || error_exit "Failed to create temporary directory ${DEFAULT_TMP_DIR}"
fi

QDRANT_DATA_DIR=$(TMPDIR="${DEFAULT_TMP_DIR}" mktemp -d -t "${QDRANT_TMP_DIR_PREFIX}XXXXX") || exit 2

echo "Temporary directory created: ${QDRANT_DATA_DIR}"

# Cleanup on exit
trap 'cleanup_and_exit $?' TERM EXIT

$CONTAINER_TOOL run --name "$QDRANT_CONTAINER_NAME" -p 6333:6333 -v "${QDRANT_DATA_DIR}":/qdrant/storage:z "${QDRANT_IMG}"


