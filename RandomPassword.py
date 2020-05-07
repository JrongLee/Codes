
import random
import string
a=string.ascii_letters+string.digits
key=[]
def getKey(prefix):
        key=random.sample(a,10)
        keys="".join(key)
        return prefix + keys

pwd = getKey("@Converter")
print(pwd)
