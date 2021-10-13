public struct DocCTest {
    public private(set) var text = "Hello, World!"
    
    public var variable: Int

    public init() {
        variable = 1
    }
    
    /// This is foo
    /// - Returns: foo returns 0
    public func foo() -> Int {
        return 0
    }
}
