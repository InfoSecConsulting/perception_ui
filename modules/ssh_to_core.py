__author__ = 'arozar'

import pexpect
from modules.cisco_cmds import *
from modules.pormpts import *

def cisco_enable_mode(user, host, passwd, en_passwd):
  ssh_newkey = 'Are you sure you want to continue connecting (yes/no)?'
  constr = 'ssh %s@%s' % (user, host)
  child = pexpect.spawnu(constr)

  ret = child.expect([pexpect.TIMEOUT, ssh_newkey, '[P|p]assword:'])
  if ret == 0:
    print('[-] Error Connecting to %s' % host)
    return
  if ret == 1:
    child.sendline('yes')
    new_ret = child.expect([pexpect.TIMEOUT, '[P|p]assword:'])
    if new_ret == 0:
      print('[-] Could not accept new key from %s' % host)
      return
    if new_ret == 1:
      child.sendline(passwd)

      auth = child.expect([pexpect.TIMEOUT, '[P|p]assword:', '.>', '.#'])
      if auth == 0:
        print('Timed out sending user auth password to host %s' % host)
        return
      if auth == 1:
        print('User password is incorrect')
        return
      if auth == 2:
        child.sendline(SHOWVER)
        # find out what Cisco OS we are working with
        what_os = child.expect([pexpect.TIMEOUT, '.IOS.', '.Adaptive.'])
        if what_os == 0:
          print('show version timed out for %s' % host)
          return

        if what_os == 1:  # if it's an IOS device
          child.sendcontrol('c')
          child.expect(PRIV_EXEC_MODE)
          child.sendline('enable')
          child.sendline(en_passwd)
          enable = child.expect([pexpect.TIMEOUT, '[P|p]assword:', '.#'])
          if enable == 0:
            print('Timed out sending enable password to host %s' % host)
          if enable == 1:
            print('enable password for %s is incorrect' % host)
            return
          if enable == 2:
            child.sendline(IOSTERMLEN0)
            return child

        if what_os == 2:  # if it's an ASAOS device
          child.sendline(QOUTMORE)
          child.expect(PRIV_EXEC_MODE)
          enable = child.expect([pexpect.TIMEOUT, 'Invalid password', '.#'])
          if enable == 0:
            print('Timed out sending enable password to host %s' % host)
            return
          if enable == 1:
            print('enable password for %s is incorrect' % host)
            return
          if enable == 3:
            child.sendline(ASATERMPAGER0)
            return child
      if auth == 3:
        child.sendline(SHOWVER)
        # find out what Cisco OS we are working with
        what_os = child.expect([pexpect.TIMEOUT, '.IOS.', '.Adaptive.'])
        if what_os == 0:
          print('show version timed out for %s' % host)
          return

        if what_os == 1:  # if it's an IOS device
          child.sendcontrol('c')
          child.sendline(IOSTERMLEN0)
          return child

        if what_os == 2:  # if it's an ASAOS device
          child.sendline(QOUTMORE)
          child.sendline(ASATERMPAGER0)
          return child

  child.sendline(passwd)
  auth = child.expect([pexpect.TIMEOUT, '[P|p]assword:', '.>', '.#'])

  if auth == 0:
    print('Timed out sending user auth password to host %s' % host)
    return
  if auth == 1:
    print('User password is incorrect')
    return
  if auth == 2:
    child.sendline('enable')
    child.sendline(en_passwd)
    enable = child.expect([pexpect.TIMEOUT, '.#'])
    if enable == 0:
      print('enable password for %s is incorrect' % host)
    if enable == 1:
      child.sendline(SHOWVER)
      # find out what Cisco OS we are working with
      what_os = child.expect([pexpect.TIMEOUT, '.IOS.', '.Adaptive.'])
      if what_os == 0:
        print('show version timed out for %s' % host)
        return

      if what_os == 1:  # if it's an IOS device
        child.sendcontrol('c')
        child.sendline(IOSTERMLEN0)
        return child

      if what_os == 2:  # if it's an ASAOS device
        child.sendline(QOUTMORE)
        child.sendline(ASATERMPAGER0)
        return child

  if auth == 3:
    child.sendline(SHOWVER)
    # find out what Cisco OS we are working with
    what_os = child.expect([pexpect.TIMEOUT, '.IOS.', '.Adaptive.'])
    if what_os == 0:
      print('show version timed out for %s' % host)
      return

    if what_os == 1:  # if it's an IOS device
      child.sendcontrol('c')
      #child.sendline(IOSTERMLEN0)
      ready = child.expect([pexpect.TIMEOUT, '.#'])
      if ready == 0:
        print('timed out for host: %s' % host)
      if ready == 1:
        return child

    if what_os == 2:  # if it's an ASAOS device
      child.sendline(QOUTMORE)
      child.sendline(ASATERMPAGER0)
      ready = child.expect([pexpect.TIMEOUT, '.#'])
      if ready == 0:
        print('timed out for host: %s' % host)
      if ready == 1:
        return child

  else:
    print('Failed to login to %s' % host)
