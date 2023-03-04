# Tests that DT_RPATH is correct for the dummy repl, docc, and sourcekit-lsp executables on Linux.
# REQUIRES: platform=Linux
# RUN: %{readelf} -d %{repl_swift} | %{FileCheck} %s
# CHECK: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}$ORIGIN/../lib/swift/linux
#
# RUN: %{readelf} -d %{docc} | %{FileCheck} --check-prefix CHECK-DOC %s
# CHECK-DOC: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}$ORIGIN/../lib/swift/linux
#
# RUN: %{readelf} -d %{sourcekit-lsp} | %{FileCheck} --check-prefix CHECK-LSP %s
# CHECK-LSP: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}$ORIGIN/../lib/swift/linux
#
# Tests that DT_RUNPATH is correct for the Swift stdlib and other libraries on Linux.
# RUN: %{readelf} -d %{package_path}/usr/lib/swift/linux/libswiftCore.so | %{FileCheck} --check-prefix CHECK-CORE %s
# CHECK-CORE: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}$ORIGIN{{[^/]}}
# CHECK-CORE-NOT: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}:/usr/lib/swift/linux
#
# RUN: %{readelf} -d %{package_path}/usr/lib/libsourcekitdInProc.so | %{FileCheck} --check-prefix CHECK-SK %s
# CHECK-SK: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}$ORIGIN/swift/linux
# CHECK-SK-NOT: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}:/usr/lib/swift/linux
#
# RUN: %{readelf} -d %{package_path}/usr/lib/swift/linux/libswiftRemoteMirror.so | %{FileCheck} --check-prefix CHECK-RM %s
# CHECK-RM: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}$ORIGIN{{[^/]}}
# CHECK-RM-NOT: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}:/usr/lib/swift/linux
#
# RUN: %{readelf} -d %{package_path}/usr/lib/swift/linux/libswift_Differentiation.so | %{FileCheck} --check-prefix CHECK-SD %s
# CHECK-SD: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}$ORIGIN{{[^/]}}
# CHECK-SD-NOT: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}:/usr/lib/swift/linux
#
# RUN: %{readelf} -d %{package_path}/usr/lib/swift/linux/libswiftGlibc.so | %{FileCheck} --check-prefix CHECK-SG %s
# CHECK-SG: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}$ORIGIN{{[^/]}}
# CHECK-SG-NOT: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}:/usr/lib/swift/linux
#
# RUN: %{readelf} -d %{package_path}/usr/lib/swift/linux/libswiftSwiftOnoneSupport.so | %{FileCheck} --check-prefix CHECK-SON %s
# CHECK-SON: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}$ORIGIN{{[^/]}}
# CHECK-SON-NOT: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}:/usr/lib/swift/linux
#
# RUN: %{readelf} -d %{package_path}/usr/lib/libswiftDemangle.so | %{FileCheck} --check-prefix CHECK-SDE %s
# CHECK-SDE-NOT: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}:/usr/lib/swift/linux
#
# RUN: %{readelf} -d %{package_path}/usr/lib/liblldb.so | %{FileCheck} --check-prefix CHECK-LLDB %s
# CHECK-LLDB: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}$ORIGIN/../lib/swift/linux
