# Safari Sandbox

A python program that parses Safari's `LastSession.plist` and creates a stripped-down sqlite database out of it for querying.
 

## Hacking

```sh
$ python3 -m venv ./venv
$ source ./venv/bin/activate # or activate.csh or activate.fish
$ pip install -r requirements.txt
$ python -m safarisandbox
```

- The database name is set to `session.db` and the table is named `lastsession`.
- Then modify the query at the bottom of `main`.

### Properties to choose from
name | type
--|--
`window_id` | text
`url` | text
`title` | text
[last-visit] | text
`date_closed` | text

### Current query that will run on your Safari windows and tabs:

```sql
SELECT url
FROM lastsession
ORDER BY url;
```


## Credits

PropertyList parsing help came from the [OSXAuditor](https://github.com/jipegit/OSXAuditor) source.


[last-visit]: https://web.archive.org/web/20200406074029/http://2016.padjo.org/tutorials/sqlite-your-browser-history/#whats-with-the-visittime "last visit"
