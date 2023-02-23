import SwiftCompilerPlugin
import SwiftSyntaxMacros

@main
struct ThePlugin: CompilerPlugin {
  var providingMarcos: [Macro.Type] = [
    EchoExpressionMacro.self,
    MetadataMacro.self
  ]
}
