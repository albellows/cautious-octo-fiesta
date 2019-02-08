#!/usr/bin/env python
# coding: utf-8

# In[15]:


import math


# In[135]:


# Bytes bit-wise arithmetic
# Assumes bytes objects are 32-bit words, per SHA-1

def b_xor(x, y) :
    intx = int.from_bytes(x, "big")
    inty = int.from_bytes(y, "big")
    val = intx^inty & 0xffffffff
    return int.to_bytes(val, 4, "big")

def b_and(x, y) :
    intx = int.from_bytes(x, "big")
    inty = int.from_bytes(y, "big")
    val = intx&inty & 0xffffffff
    return int.to_bytes(val, 4, "big")

def b_complement(x) :
    intx = int.from_bytes(x, "big")
    val = ~intx & 0xffffffff
    return int.to_bytes(val, 4, "big")


# In[137]:


# Bytes arithmetic
# Assumes bytes objects are 32-bit words, per SHA-1

# addition is performed modulo 2^32
def b_plus(x, y) :
    intx = int.from_bytes(x, "big")
    inty = int.from_bytes(y, "big")
    val = intx + inty
    val = val % pow(2,32)
    return int.to_bytes(val, 4, "big")

def b_mod(x, y) :
    intx = int.from_bytes(x, "big")
    inty = int.from_bytes(y, "big")
    val = intx % inty
    return int.to_bytes(val, 4, "big")


# In[41]:


def ch(x, y, z) :
    # (x & y)^(~x & z)
    return b_xor(b_and(x,y), b_and(b_complement(x), z))

def parity(x, y, z) :
    # x ^ y ^ z
    return b_xor(b_xor(x,y),z)

def maj(x, y, z) :
    # (x & y)^(x & z)^(y & z)
    return b_xor(b_xor(b_and(x,y),b_and(x,z)),b_and(y,z))


# In[17]:


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


# In[18]:


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


# In[235]:


def rotr(n, x) :
    xint = int.from_bytes(x, "big")
    val = (xint >> n) | (xint << 32 - n)
    # keep in 32-bit space
    val &= 0xffffffff
    return int.to_bytes(val, 4, "big")

def rotl(n, x) :
    xint = int.from_bytes(x, "big")
    val = (xint << n) | (xint >> 32 - n)
    # keep in 32-bit space
    val &= 0xffffffff
    return int.to_bytes(val, 4, "big")


# In[227]:


hex(int.from_bytes(rotl(5, int.to_bytes(0x67452301, 4, "big")),"big"))


# In[20]:


def get_bit_length(s) :
    return 8*len(s.encode("utf-8"))


# In[21]:


def pad(M) :
    l = get_bit_length(M)
    k = (512 + 448 - (l % 512 + 1)) % 512
    
    s = M.encode("utf-8")
    second_len = math.ceil((k+1)/8)
    s += (1 << k).to_bytes(second_len, byteorder="big")
    third_len = 8
    s += (l).to_bytes(third_len, byteorder="big")
    return s

# Padded message is parsed into N 512-bit blocks. The 512 bits 
# of the input block may be expressed as 16 32-bit words
# expects M is a bytes object
def parse_pad(M) :
    blocks = []
    for index in range(0,len(M),65) :
        blocks.append(M[index:index+64])
    return blocks


# In[22]:


def init_hash() :
    return [bytes.fromhex(x) for x in            ("67452301", "efcdab89", "98badcfe",              "10325476", "c3d2e1f0") ]


# In[23]:


s = parse_pad(pad("abcdef"))
s[0][0]


# In[77]:


hex(init_hash()[1][1])


# In[25]:


pad("abc")[2]


# In[256]:


def sha1(m) :
    s = pad(m)
    
    # M and h are both arrays of bytes objects
    M = parse_pad(s)
    h = []
    h.insert(0,init_hash())
    
    N = len(M)
    #n = N+1 if N>1 else N
    
    w = []
    for i in range(1,N+1) :
        for t in range(0,80) :
            if 0 <= t and t <= 15 :
                # M starts at index 1 in the docs!  So indices in
                # M must be subtracted by 1.
                w.insert(t,M[i-1][t*4:(t*4)+4])
            else :
                w.insert(t,                          rotl(1, b_xor(b_xor(b_xor(w[t-3],w[t-8]),                                        w[t-14]), w[t-16])))
                
        a = h[i-1][0]
        b = h[i-1][1]
        c = h[i-1][2]
        d = h[i-1][3]
        e = h[i-1][4]
        
        for t in range(0, 80) :
            kt = int.to_bytes(k(t), 4, "big")           
            T = b_plus(b_plus(b_plus(b_plus(rotl(5,a), f(t,b,c,d)),                        e), kt), w[t])
            
            e = d
            d = c
            c = rotl(30, b)
            b = a
            a = T
  
        new_h = [b_plus(x,h[i-1][y]) for x,y in                             zip([a,b,c,d,e],range(5))]
        
        h.insert(i, new_h)
        
    return h[N]


# In[257]:


sha1("abc")


# In[258]:


hex(int.from_bytes(rotl(5, int.to_bytes(0x67452301, 4, "big")), "big"))


# In[267]:


s = "0x"
for b in sha1("abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq") :
    s += hex(int.from_bytes(b, "big"))[2:]
print(s)


# In[268]:


ex = 0x84983E441C3BD26EBAAE4AA1F95129E5E54670F1
print(hex(ex))
hex(ex) == s


# In[ ]:




