import Testing
import XCTest

@Test func example() async throws {
    #expect(Int("42") == 42)
}

final class HelloTests: XCTestCase {
    func testExample() throws {
        XCTAssertEqual(Int("42"), 42)
    }
}
