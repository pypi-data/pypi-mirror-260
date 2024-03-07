from pynput import keyboard as kb

'''
target_keys = ['a', 'b', 'c']
key_states = {
    'left': False,
    'right': False,
    'up': False,
    'down': False,
    'space': False
}
'''

class KeyChecker:
    def __init__(self):
        self.key_pressed = None
        self.listener = kb.Listener(on_press=self.on_press,on_release=self.on_release)
        self.listener.start()

    def on_press(self, key):
        try:
            #print(key)
            self.key_pressed = key.char
            #print(key.char)
        except AttributeError:
            # Ignore special keys without char attribute
            #print('pressed')
            if key == kb.Key.up:
                self.key_pressed = 'up'
                #print('---key.up---')
            if key == kb.Key.down:
                #print('---key.down---')
                self.key_pressed = 'down'
            if key == kb.Key.left:
                #print('---key.left---')
                self.key_pressed = 'left'
            if key == kb.Key.right:
                #print('---key.right---')
                self.key_pressed = 'right'
            if key == kb.Key.space:
                #print('---key.space---')
                self.key_pressed = 'space'
    def on_release(self,key):
        try:
            self.key_pressed = ''
            #print('---release---')
        except AttributeError:
            #print('release')
            if key == kb.Key.up:
                #print('---key.up---')
                self.key_pressed = ''
            if key == kb.Key.down:
                #print('---key.down---')
                self.key_pressed = ''
            if key == kb.Key.left:
                #print('---key.left---')
                self.key_pressed = ''
            if key == kb.Key.right:
                #print('---key.right---')
                self.key_pressed = ''
            if key == kb.Key.space:
                #print('---key.space---')
                self.key_pressed = ''

    def is_pressed(self, target_key):
        res = self.key_pressed == target_key
        return res

    def start_listening(self):
        with self.listener as listener:
            listener.join()

def is_pressed(key):
    return keyboard.is_pressed(key)

keyboard = KeyChecker()

'''
# Example usage
if __name__ == "__main__":
    key_checker = KeyChecker()
    try:
        key_checker.start_listening()
        while True:
            target_key = input("Enter the target key: ")
            if key_checker.is_pressed(target_key):
                print(f"Key '{target_key}' is pressed!")
            else:
                print(f"Key '{target_key}' is not pressed!")
    except KeyboardInterrupt:
        pass
'''