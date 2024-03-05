Log a line in my daily log.

*Latest release 20240305*:
Initial PyPI release.

This is an upgrade from my venerable shell script,
whose logic was becoming unwieldy.

I more or less live in the shell, so I log activity with brief
1-line shell command commands eg:

    dlog HOME: set up the whatchamgig

which I alias as `dl`, with additional aliases like `HOME` for `dl HOME:`
and so forth; as short a throwaway line as I can get away with.
In particular, I use this to make notes about work activity
(none of the several time tracking tools I've tried work for me)
and things like banking and purchases eg:

    dl MYBANK,VENDOR: xfer \$99 to vendor for widget from bank acct rcpt 1234567

I've got scripts to pull out the work ones for making invoices
and an assortment of other scripts (eg my `alert` script) also log via `dlog`.

The current incarnation logs to a flat text file (default `~/var/dlog-quick`)
and to `SQLTags` SQLite database.
It has a little daemon mode to reduce contention for the SQLite database too.

## Class `DLog`

A log entry.

*Method `DLog.daemon(pipepath: str, logpath: Optional[str] = None, sqltags: Optional[cs.sqltags.SQLTags] = None, *, runstate: cs.resources.RunState)`*:
Run a daemon reeading dlog lines from `pipepath`
and logging them to `logpath` and/or `sqltags`.

`pipepath` must not already exist, and will be removed at
the end of this function. This is to avoid dlog clients
trying to use an unattended pipe.

*Property `DLog.dt_s`*:
This log entry's local time as a string.

*Method `DLog.from_str(line, *, categories: Iterable[str] = (), multi_categories: bool = False)`*:
Create a `DLog` instance from a log line.

Parameters:
* `line`: the log line from which to derive the `DLog` object
* `categories`: optional iterable of category names, which will be lowercased
* `multi_categories`: default `False`; if true the look for
  multiple leading *CAT*`,`...`:` preambles on the line to derive
  caetgory names instead of just one

The expected format is:

    YYYY-MM-DD HH:MM:SS [cats,...:] [+tag[=value]]... log text

Example:

    >>> DLog.from_str('2024-02-01 11:12:13 XX: +a +b=1 +c="zot"  +9 zoo=2') # doctest: +ELLIPSIS
    DLog(headline='+9 zoo=2', categories={'xx'}, tags=TagSet:{'a': None, 'b': 1, 'c': 'zot'}, when=...)

*Method `DLog.log(self, logpath: Optional[str] = None, *, pipepath: Optional[str] = None, sqltags: Optional[cs.sqltags.SQLTags] = None)`*:
Log to `pipepath`, falling back to `logpath` and/or `sqltags`.

Parameters:
* `pipepath`: optional filesystem path of a named pipe
   to which to write the log line
* `logpath`: optional filesystem path of a regular file to
  which to append the log line
* `sqltags`: optional `SQLTags` instance or filesystem path
  of an SQLite file to use with `SQLTags`; also log the `DLog`
  entry here

One of `logpath` or `sqltags` must be provided.

If `pipepath` exists and is logged to, `logpath` and `sqltags`
are ignored - the daemon listening to the pipe will do the
logging.

If `pipepath` is not supplied or we fail to log to it, fall
back to logging to `logpath` and/or `sqltags`.

*Method `DLog.quick(self, logf)`*:
Write this log enty to the file `logf`.
If `logf` is a string, treat it as a filename and open it for append.

## Function `dlog(headline: str, *, logpath: Optional[str] = None, sqltags: Optional[cs.sqltags.SQLTags] = '~/var/sqltags.sqlite', tags=None, categories: Optional[Iterable] = None, when: Union[NoneType, int, float, datetime.datetime] = None)`

Log `headline` to the dlog.

Parameters:
* `headline`: the log line message
* `logpath`: optional text log pathname,
  default `~/var/log/dlog-quick` from DEFAULT_LOGPATH
* `sqltags`: optional `SQLTags` instance,
  default uses `~/var/sqltags.sqlite` from DEFAULT_DBPATH
* `tags`: optional iterable of `Tag`s to associate with the log entry
* `categories`: optional iterable of category strings
* `when`: optional UNIX time or `datetime`, default now

## Class `DLogCommand(cs.cmdutils.BaseCommand)`

The `dlog` command line implementation.

Command line usage:

    Usage: dlog subcommand [...]
      Subcommands:
        daemon [pipepath]
          Listen on pipepath for new dlog messages.
          This serialises contention for the database.
        help [-l] [subcommand-names...]
          Print help for subcommands.
          This outputs the full help for the named subcommands,
          or the short help for all subcommands if no names are specified.
          -l  Long help even if no subcommand-names provided.
        log [{CATEGORIES:|tag=value}...] headline
          Log headline to the dlog.
          Options:
          -c categories   Alternate categories specification.
          -d datetime     Timestamp for the log entry instead of "now".
        scan [{-|filename}]...
          Scan log files and report.
        shell
          Run a command prompt via cmd.Cmd using this command's subcommands.

*`DLogCommand.Options`*

*Method `DLogCommand.cats_from_str(cats_s)`*:
Return an iterable of lowercase category names from a comma
or space separated string.

*Method `DLogCommand.cmd_daemon(self, argv)`*:
Usage: {cmd} [pipepath]
Listen on pipepath for new dlog messages.
This serialises contention for the database.

*Method `DLogCommand.cmd_log(self, argv, fstags: cs.fstags.FSTags)`*:
Usage: {cmd} [{{CATEGORIES:|tag=value}}...] headline
Log headline to the dlog.
Options:
-c categories   Alternate categories specification.
-d datetime     Timestamp for the log entry instead of "now".

*Method `DLogCommand.cmd_scan(self, argv)`*:
Usage: {cmd} [{{-|filename}}]...
Scan log files and report.

## Function `main(argv=None)`

Run the `dlog` command line implementation.

# Release Log



*Release 20240305*:
Initial PyPI release.
