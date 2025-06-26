# Tests that executables are universal binaries on MacOS
# REQUIRES: platform=Darwin
#
# RUN: file %{wasmkit} | %{FileCheck} --check-prefix CHECK-WASMKIT %s
# CHECK-WASMKIT: {{.*}} Mach-O universal binary {{.*}}
#

