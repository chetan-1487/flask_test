import re
import os
import uuid

def is_password_valid(password:str)->bool:
  pattern = r"""
    ^
    (?=.*[A-Z])
    (?=.*[a-z])
    (?=.*\d)
    (?=.*[!@#$%^&*()])
    .{8,}
    $

    """
  
  return bool(re.match(pattern, password, re.VERBOSE))


def is_username_valid(username:str)->bool:
  pattern = r"""
      ^(?=.*[A-Z])
      ^(?=.*[a-z])
      ^(?=.*\d)
    """
  
  return bool(re.match(pattern, username, re.VERBOSE))



