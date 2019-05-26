# Tests that RUNPATH is correct for the plutil binary on Linux
# REQUIRES: platform=Linux
# RUN: %{readelf} -d %{swift_bin_dir}/plutil | %{FileCheck} %s
# CHECK: {{.*}} RUNPATH {{.*}}:$ORIGIN/../lib/swift/linux
