#!/usr/bin/env bash
# Build the version-pinned CodeQL image used to analyze Python code.
#
# Provisions a base container with the CodeQL bundle and commits it to a tagged
# image. One-time setup; idempotent. Requires the Docker daemon and network
# access (downloads the CodeQL bundle, ~1.3 GB, producing a ~3.4 GB image).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

CODEQL_VERSION="v2.25.4"
IMAGE="securecontext-codeql-eval:2.25.4"
BUILD_CTR="codeql-eval-build"

if ! docker info >/dev/null 2>&1; then
	echo "Docker daemon is not reachable. Start Docker and re-run." >&2
	exit 1
fi

# Already built? Nothing to do.
if docker image inspect "$IMAGE" >/dev/null 2>&1; then
	echo "Image already built: $IMAGE"
	echo "Run an analysis with:"
	echo "  python3 $SKILL_DIR/scripts/run_eval.py --code <file.py> [--cwe CWE-XX]"
	exit 0
fi

# Remove a leftover build container from an interrupted run.
docker rm -f "$BUILD_CTR" >/dev/null 2>&1 || true

echo "Building $IMAGE (CodeQL $CODEQL_VERSION, linux/amd64)..."
echo "First build downloads the bundle and can take a few minutes."

# Start a long-lived base container to provision in place.
docker run -d --platform=linux/amd64 --name "$BUILD_CTR" ubuntu:22.04 sleep infinity >/dev/null

# Install the CodeQL bundle inside the container. The version is passed as an
# environment variable so the provisioning script body can stay single-quoted.
docker exec -e CODEQL_VERSION="$CODEQL_VERSION" "$BUILD_CTR" sh -c '
	set -e
	export DEBIAN_FRONTEND=noninteractive
	apt-get update
	# python3: required by the CodeQL Python extractor to build the database.
	apt-get install -y --no-install-recommends curl ca-certificates python3
	rm -rf /var/lib/apt/lists/*
	curl -fSL "https://github.com/github/codeql-action/releases/download/codeql-bundle-${CODEQL_VERSION}/codeql-bundle-linux64.tar.gz" -o /tmp/codeql.tar.gz
	mkdir -p /opt
	tar -xzf /tmp/codeql.tar.gz -C /opt
	rm /tmp/codeql.tar.gz
	mkdir -p /work/src
	# Fail early if the python-queries pack is not resolvable.
	/opt/codeql/codeql resolve qlpacks | grep -i python-queries
'

# Commit the provisioned container to the tagged image.
docker commit \
	--change 'ENV PATH=/opt/codeql:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin' \
	--change 'WORKDIR /work' \
	"$BUILD_CTR" "$IMAGE" >/dev/null

docker rm -f "$BUILD_CTR" >/dev/null 2>&1 || true

echo
echo "Done. Built $IMAGE"
echo "Run an analysis with:"
echo "  python3 $SKILL_DIR/scripts/run_eval.py --code <file.py> [--cwe CWE-XX]"
