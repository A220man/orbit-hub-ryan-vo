import '@testing-library/jest-dom'
import { JSDOM } from 'jsdom'

const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>', {
  url: 'http://localhost',
  pretendToBeVisual: true,
})

global.window = dom.window
global.document = dom.window.document
global.HTMLElement = dom.window.HTMLElement
global.Element = dom.window.Element
global.Node = dom.window.Node
global.requestAnimationFrame = (cb: FrameRequestCallback) => setTimeout(cb, 16)
global.cancelAnimationFrame = (id: number) => clearTimeout(id)