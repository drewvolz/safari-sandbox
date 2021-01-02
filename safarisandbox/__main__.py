#!/usr/bin/env python

from os import path, listdir
from os.path import isdir, join
import argparse
import sqlite3
import Foundation
from typing import TypedDict


class Tab(TypedDict):
	window_id: str
	url: str
	title: str
	last_visit: str
	date_closed: str


def parse_safari() -> [Tab]:
	for User in listdir('/Users'):
		profile_path = join('/Users', User, 'Library/Safari')

		if User[0] != '.' and isdir(profile_path):
			return parse_profile(User, profile_path)


def parse_profile(User, Path) -> [Tab]:
	tabs = []

	last_session_plist_path = join(Path, 'LastSession.plist')
	last_session_plist = read_plist(last_session_plist_path)

	if last_session_plist and 'SessionWindows' in last_session_plist:
		try:
			session_windows = last_session_plist['SessionWindows']

			for window in session_windows:
				for tab in window.get('TabStates', []):
					url = tab.get('TabURL', '')
					title = tab.get('TabTitle', '')
					window_id = tab.get('WindowUUID', '')
					last_visit = tab.get('LastVisitTime', '')
					date_closed = tab.get('DateClosed', '')

					current_tab = Tab(window_id=str(window_id),
					                  url=str(url),
					                  title=str(title),
					                  last_visit=str(last_visit),
					                  date_closed=str(date_closed))

					tabs.append(current_tab)

			return tabs
		except Exception as e:
			print(f'Exception in parse_profile: {e}')


def read_plist(plist_path):
	plist_dict = False

	plist_nsdata, error = Foundation.NSData.dataWithContentsOfFile_options_error_(
	    plist_path, Foundation.NSUncachedRead, None)

	if error is not None or plist_nsdata is None:
		print(f'Unable to read in the data from the plist file: {plist_path}')

	plist_dict, plistFormat, error = Foundation.NSPropertyListSerialization.propertyListFromData_mutabilityOption_format_errorDescription_(
	    plist_nsdata, Foundation.NSPropertyListMutableContainers, None, None)

	if error is not None or plist_dict is None:
		print(f'Unable to read in the data from the plist file: {plist_path}')

	return plist_dict


def init_db(conn: sqlite3.Connection):
	conn.execute('drop table if exists lastsession')
	conn.execute('''
		create table lastsession (
			window_id text,
			url text,
			title text,
			last_visit text,
			date_closed text
		)
	''')


def insert_tabs(conn: sqlite3.Connection, tabs: [Tab]):
	with conn:
		conn.execute('DELETE FROM lastsession')

		for tab in tabs:
			conn.execute(
			    '''
				INSERT INTO lastsession (window_id, url, title, last_visit, date_closed) 
				VALUES (:window_id, :url, :title, :last_visit, :date_closed) 
			''', tab)


def select(conn: sqlite3.Connection, fields: str, order_by: str):
	with conn:
		cursor = conn.cursor()

		sql = '''
		SELECT %s
		FROM lastsession
		ORDER BY %s;
		'''

		query = sql % (fields, order_by)
		print_query = ''.join(query.split('\t'))

		rows = cursor.execute(query).fetchall()
		print(f'Found: {len(rows)}', end='\n\n')
		print(f'Query: {print_query}')

		for row in rows:
			print(row)


def main():
	parser = argparse.ArgumentParser(
	    prog='safarisandbox',
	    description=
	    'Parses Safari\'s LastSession.db and creates a stripped-down sqlite database out of it.'
	)
	args = parser.parse_args()

	conn = sqlite3.connect('session.db')
	init_db(conn)

	tabs = parse_safari()
	insert_tabs(conn, tabs)

	select(conn=conn, fields='url', order_by='url')


if __name__ == "__main__":
	main()
