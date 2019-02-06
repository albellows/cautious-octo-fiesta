#!/usr/bin/env python
# coding: utf-8

# In[18]:


import math


# In[19]:


def ch(x, y, z) :
    return (x & y)^(~x & z)

def parity(x, y, z) :
    return x ^ y ^ z

def maj(x, y, z) :
    return (x & y)^(x & z)^(y & z)


# In[20]:


def f(t, x, y, z) :
    if 0 <= t and t <= 19 :
        return ch(x,y,z)
    elif 20 <= t and t <= 39 :
        return parity(x,y,z)
    elif 40 <= t and t <= 59 :
        return maj(x,y,z)
    elif 60 <= t and t <= 79 :
        return parity(x,y,z)
    else :
        print("Invalid value of t.")
        return -1


# In[21]:


def k(t) :
    if 0 <= t and t <= 19 :
        return 0x5a827999
    elif 20 <= t and t <= 39 :
        return 0x6ed9eba1
    elif 40 <= t and t <= 59 :
        return 0x8f1bbcdc
    elif 60 <= t and t <= 79 :
        return 0xca62c1d6
    else :
        print("Invalid value of t.")
        return -1


# In[5]:


def get_bit_length(s) :
    return 8*len(s.encode("utf-8"))


# In[43]:


# Padded message is parsed into N 512-bit blocks. The 512 bits 
# of the input block
def pad(M) :
    l = get_bit_length(M)
    k = (512 + 448 - (l % 512 + 1)) % 512
    
    s = M.encode("utf-8")
    second_len = math.ceil((k+1)/8)
    s += (1 << k).to_bytes(second_len, byteorder="big")
    third_len = 8
    s += (l).to_bytes(third_len, byteorder="big")
    
    #print(len(s))
    return s
#pad("abc")


# In[38]:





# In[ ]:




