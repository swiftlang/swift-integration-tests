# Tests that DT_RPATH is correct for the dummy repl executable on Linux.
# REQUIRES: platform=Linux
# RUN: %{readelf} -d %{repl_swift} | %{FileCheck} %s
# CHECK: {{.*}} RPATH {{.*}}$ORIGIN/../lib/swift/linux
