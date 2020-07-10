# hashpass
Program to hash + salt passwords, purely to uniquify some master password across multiple domains

This application serves as an alternative to classical password managers. Rather than storing + encrypting your passwords, it takes a master password, a domain, and a username as input, and produces a new password on the fly. This means nothing is ever stored, not even locally.

By hashing the input password against the domain and the username/id, the resulting password becomes unique by domain/site as well as by user (in the event that multiple people use this same program). Additionally, by hashing the input password, we do get some marginal security gains-  if the hashed password were leaked in a breach where passwords were stored in plaintext, the master password is not immediately compromised.

The result is deterministic, so the resulting password will be the same when ran at a future date, even on a different machine. The code is as platform-independent and backwards-compatible as possible, and the only 3rd party dependency (pyperclip) is optional, and is used to automatically copy the hashed password to your clipboard.

Passwords are 16 characters in length, consisting of alphanumeric characters and the following symbols: `!@#$%^&*` Passwords will have at least one lowercase letter, uppercase letter, digit, and symbol. Thus, the hashed passwords will meet most password criteria out of the box. Any out-of-the-normal requirements will have to be met by luck or in the worst case, finding a special master password for that specific domain.
