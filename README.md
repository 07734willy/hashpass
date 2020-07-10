# hashpass
Program to hash + salt passwords, purely to uniquify some master password across multiple domains

By hashing the input password against the domain and the username/id, the resulting password becomes unique by domain/site as well as by user (in the event that multiple people use this same program). Additionally, by hashing the input password, we do get some marginal security gains-  if the hashed password were leaked in a breach where passwords were stored in plaintext, the master password is not immediately compromised.

The result is deterministic, so the resulting password will be the same when ran at a future date, even on a different machine. The code is as platform-independent and backwards-compatible as possible, and the only 3rd party dependency (pyperclip) is optional.
