Jira-Commando
=============

A command line utility for Jira.

Installation
=============

```shell
% sudo easy_install https://github.com/joshrl/Jira-Commando/tarball/master
```

Tested on OSX, probably works on UNIX variants, good luck on Windows.

Usage
=============

The first time you run the jira command it will ask for a server, user, and password. The username and server are stored in your home directory in the file ~/.jira.db The password is stored in your keychain associated with the server you set. 

See your cards with a status of "Dev":

```shell
% jira ls Dev
```

Add a comment to a card

```shell
% jira cm JIRA-123 "Hello"
```

Add a git fix version comment to a card

```shell
% jira cm JIRA-123 "Fix version: `git describe`"
```

Move a card to "QA Ready"

```shell
% jira mv JIRA-123 "QA Ready"
```

Move a card to interactively

```shell
% jira mv JIRA-123 "QA Ready"
0) Dev Ready
1) QA Ready
2) QA
3) Deploy Ready
4) Done
5) In Definition
Enter number: 1
```

