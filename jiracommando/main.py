#!/usr/bin/python

from jira.client import JIRA
from optparse import OptionParser
import webbrowser
import keyring
import shelve
import os
import sys
from getpass import getpass

def move_issue(issue_key,to_transition_name=None,interactive=False):

	issue = jira.issue(issue_key)
	transitions = jira.transitions(issue_key)
	to_id = None
	if interactive:
		print "Move %s: %s:" % (issue.key, issue.fields.summary)
		for i,trans in enumerate(transitions):
			print "%i) %s" % (++i,trans['to']['name'])
		input_str = raw_input("Enter number: ")
		try:
			to_id = transitions[int(input_str)]['id']
		except:
			print "Invalid Number!"
			exit(1)
	if not to_id and to_transition_name:
		for trans in transitions:
			if trans['to']['name'] == to_transition_name:
				to_id = trans['id']
				break
	if not to_id:
		print "Transition invalid for issue %s" % issue
	jira.transition_issue(issue=issue_key,transitionId=to_id)

def comment_issue(issue_key,comment):
	issue = jira.issue(issue_key)
	issue.add_comment(comment)

def print_transitions(issue):
	transitions = jira.transitions(issue)
	for trans in transitions:
		print trans['to']['name']

def print_assigned_issues(statuses):
	in_str = ", ".join('"{0}"'.format(i) for i in statuses)
	issues = jira.search_issues('project = PLUS AND status in (%s) AND assignee in (currentUser())' % in_str) 
	for issue in issues:
		print "%s(%s) %s" % (issue.key,issue.fields.status.name,issue.fields.summary)

def action_browse(args):
	if len(args) < 1:
		print 'usage: %s br[owse] JIRA-1234' % os.path.basename(sys.argv[0])
		exit(0)
	url = '%s/browse/%s' % (d['server'],args[1])
	webbrowser.open(url)

def action_list(args):
	if len(args)>1:
		statuses = [args[1]]
	else:
		statuses=['In Definition','Dev Ready','Dev']
	print_assigned_issues(statuses);

def action_move(args):
	if len(args) < 2:
		print 'usage: %s mv JIRA-1234' % os.path.basename(sys.argv[0])
		exit(0)
	if len(args) < 3:
		move_issue(args[1],interactive=True)
	else:
		move_issue(args[1],args[2])

def action_comment(args):
	if len(args) < 2:
		print 'usage: %s cm JIRA-1234 "my comment"' % os.path.basename(sys.argv[0])
		exit(0)
	comment_issue(args[1],args[2])

def setup_jira():
	global jira,d

	if d.has_key('server') and d.has_key('user'):
		password = keyring.get_password(d['server'],d['user'])
		if password:
			jira = JIRA({'server':d['server']},basic_auth=(d['user'], password))

	if not jira:
		if not d.has_key('server'):
			d['server'] = raw_input("Server: ")
		if not d.has_key('user'):
			d['user'] = raw_input("User: ")
		password = getpass()
		d.sync()
		jira = JIRA({'server':d['server']},basic_auth=(d['user'], password))
		if jira:
			keyring.set_password(d['server'],d['user'],password)

actions = {('list','ls'):action_list,('browse','br'):action_browse,('comment','cm'):action_comment,('move','mv'):action_move}

def main():
	global jira,d
	jira = None
	usage = "usage: %prog [options] [list|move|comment|browse] [arguments]"
	parser = OptionParser(usage)
	parser.add_option("-r", "--reset-settings", dest="reset_settings",action="store_true",help="Clear username and server")

	(options, args) = parser.parse_args()

	d = shelve.open(os.path.expanduser("~")+"/.jira")

	if options.reset_settings:
		if d.has_key('server'):
			del d['server']
		if d.has_key('user'):
			del d['user']
		d.sync()

	if len(args) == 0:
		if not d.has_key('server'):
			setup_jira()
		else:
			parser.print_help()
		exit(1)

	action_name = args[0]
	action = None
	for names,value in actions.iteritems():
		if action_name in names:
			action = value
			break

	if not action:
		print "Unknown action: " + action_name
		options.print_help()
		exit(1)

	setup_jira()
	if jira:
		action(args)
	d.close()

if __name__ == "__main__":
	main()

