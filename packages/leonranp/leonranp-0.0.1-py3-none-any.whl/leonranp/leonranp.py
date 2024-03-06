'''
This is Leon Random Plus,that add more functions to the random!
To use it,code "import leonranp"

Copyright LeonMMcoset.All rights reserved.
'''
from random import *
#Start Code#
#randstr:just code "randstr()".
def randstr():
    randstrlist = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    randstr = choice(randstrlist)
    print(randstr)
#End Code#
#---------------------------------------
#If your code is commerce,
#you gonna add this in your code!
#"leonranp.info()"
#Thank you!Have a good time.
def info():
    print('This code is use Leon Random Plus!')
#You can use "leonranp.help()" to get help!
def help():
    print('---Leon Random Plus Help Start---')
    print('randstr() -> Random string')
    print('---Leon Random Plus Help End---')