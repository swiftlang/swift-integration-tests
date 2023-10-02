import Foundation
import FoundationNetworking

let url = URL(string: "http://example.com")!
let urlRequest = URLRequest(url: url)
print(urlRequest)

let urlSession = URLSession.shared
let task = urlSession.dataTask(with: urlRequest)
print(task.state)
task.cancel()
