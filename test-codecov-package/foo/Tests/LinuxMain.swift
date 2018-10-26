import XCTest

import fooTests

var tests = [XCTestCaseEntry]()
tests += fooTests.allTests()
XCTMain(tests)