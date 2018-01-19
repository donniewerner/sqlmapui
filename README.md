# sqlmapui
GUI for SQLmap written in TKinter python

Full SQLmap functionality
English UI

```
features:
--sql-shell
--forms
--no-cast
-g -q GOOGLEDORK

fixed/added:
--os-cmd=OSCMD      Execute an operating system command
--os-shell          Prompt for an interactive operating system shell
--os-pwn            Prompt for an OOB shell, Meterpreter or VNC
--priv-esc          Database process user privilege escalation
--msf-path=MSFPATH  Local path where Metasploit Framework is installed
--tmp-path=TMPPATH  Remote absolute path of temporary files directory

fixed append the lasturi log and add new line
fixed -v not working

todo:
--update
--identify-waf
--mobile
--skip-urlencode
-s SESSIONFILE      Load session from a stored (.sqlite) file
--file-write=WFILE  Write a local file on the back-end DBMS file system
--file-dest=DFILE   Back-end DBMS absolute filepath to write to

```


note: this was found from an unknown version in Chinese, retranslated to Russian. 
			I am simply building on that work, credits to the
			original authors, and the translated version this
			is built from.
