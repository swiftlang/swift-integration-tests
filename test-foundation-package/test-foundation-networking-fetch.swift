import Foundation
import FoundationNetworking

let url = URL(string: "http://swift.org")!
let data = try! Data(contentsOf: url)
print(data.underestimatedCount)
