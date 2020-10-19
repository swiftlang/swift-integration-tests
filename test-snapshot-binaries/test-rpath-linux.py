# Tests that DT_RPATH is correct for the dummy repl executable on Linux.
# REQUIRES: platform=Linux
# RUN: %{readelf} -d %{repl_swift} | %{FileCheck} %s
# CHECK: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}$ORIGIN/../lib/swift/linux
#
# Tests that DT_RUNPATH is correct for the Swift stdlib and other libraries on Linux.
# RUN: %{readelf} -d %{package_path}/usr/lib/swift/linux/libswiftCore.so | %{FileCheck} --check-prefix CHECK-CORE %s
# CHECK-CORE-NOT: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}:/usr/lib/swift/linux
#
# RUN: %{readelf} -d %{package_path}/usr/lib/libsourcekitdInProc.so | %{FileCheck} --check-prefix CHECK-SK %s
# CHECK-SK-NOT: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}:/usr/lib/swift/linux
#
# RUN: %{readelf} -d %{package_path}/usr/lib/swift/linux/libswiftRemoteMirror.so | %{FileCheck} --check-prefix CHECK-RM %s
# CHECK-RM-NOT: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}:/usr/lib/swift/linux
#
# RUN: %{readelf} -d %{package_path}/usr/lib/swift/linux/libswift_Differentiation.so | %{FileCheck} --check-prefix CHECK-SD %s
# CHECK-SD-NOT: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}:/usr/lib/swift/linux
#
# RUN: %{readelf} -d %{package_path}/usr/lib/swift/linux/lib_InternalSwiftSyntaxParser.so | %{FileCheck} --check-prefix CHECK-SP %s
# CHECK-SP-NOT: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}:/usr/lib/swift/linux
#
# RUN: %{readelf} -d %{package_path}/usr/lib/swift/linux/libswiftGlibc.so | %{FileCheck} --check-prefix CHECK-SG %s
# CHECK-SG-NOT: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}:/usr/lib/swift/linux
#
# RUN: %{readelf} -d %{package_path}/usr/lib/swift/linux/libswiftSwiftOnoneSupport.so | %{FileCheck} --check-prefix CHECK-SON %s
# CHECK-SON-NOT: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}:/usr/lib/swift/linux
#
# RUN: %{readelf} -d %{package_path}/usr/lib/libswiftDemangle.so | %{FileCheck} --check-prefix CHECK-SDE %s
# CHECK-SDE-NOT: {{.*}} {{\(RPATH\)|\(RUNPATH\)}} {{.*}}:/usr/lib/swift/linux
