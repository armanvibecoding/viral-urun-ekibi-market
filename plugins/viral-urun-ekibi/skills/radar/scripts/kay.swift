// kay X Y TIK [piksel_tik=10] [ms=8] — hidSystemState kaynaklı piksel tekerlek (pozitif TIK = aşağı, negatif = yukarı)
import Foundation
import CoreGraphics
let a = CommandLine.arguments
let p = CGPoint(x: Double(a[1])!, y: Double(a[2])!)
let n = Int(a[3])!, px = a.count > 4 ? Int32(a[4])! : 10, ms = a.count > 5 ? UInt32(a[5])! : 8
let s = CGEventSource(stateID: .hidSystemState)
CGEvent(mouseEventSource: s, mouseType: .mouseMoved, mouseCursorPosition: p, mouseButton: .left)?.post(tap: .cghidEventTap)
usleep(60000)
let dir: Int32 = n > 0 ? -1 : 1
for _ in 0..<abs(n) {
  let e = CGEvent(scrollWheelEvent2Source: s, units: .pixel, wheelCount: 1, wheel1: dir*px, wheel2: 0, wheel3: 0)!
  e.location = p; e.post(tap: .cghidEventTap); usleep(ms*1000)
}
