import msvcrt, sys
'''
    python 键盘输入密码
'''

def pwd_input():
  chars = []
  while True:
    newChar = msvcrt.getch()
    if newChar in '\r\n':
    # 如果是换行，则输入结束
      print('')
      break
    elif newChar == '\b':
    # 如果是退格，则删除末尾一位
      if chars:
        del chars[-1]
        sys.stdout.write('\b')
        # 删除一个星号，但是不知道为什么不能执行...
    else:
      chars.append(newChar)
      sys.stdout.write('*')
      # 显示为星号
  print(''.join(chars))

def main():
    pwd = pwd_input()
    print(pwd)

if __name__ == '__main__':
    main()