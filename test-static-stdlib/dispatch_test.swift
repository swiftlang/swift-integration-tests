import Dispatch

let queue = DispatchQueue(label: "queuename", attributes: .concurrent)
queue.sync {
    print("OK")
}
