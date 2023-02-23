@freestanding(expression)
macro echo<T>(_: T) -> T = #externalMacro(module: "ExamplePlugin", type: "EchoExpressionMacro")

@attached(member)
macro Metadata() = #externalMacro(module: "ExamplePlugin", type: "MetadataMacro")

@Metadata
class MyClass {
  var value: Int = #echo(12)
}
