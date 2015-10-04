Command-Line Utility
--------------------
For syntax help::

	python cli.py -h 

You will need to supply your Twitter application OAuth credentials.  The easiest option is to save them in TwitterAPI/credentials.txt.  It is the default place where cli.py will look for them.  You also may supply an alternative credentials file as a command-line argument.

Call any REST API endpoint::

	python cli.py -endpoint statuses/update -parameters status='my tweet'

Another example (here using abbreviated option names) that parses selected output fields::

	python cli.py -e search/tweets -p q=zzz count=10 -field screen_name text 

Calling any Streaming API endpoint works too::

	python cli.py -e statuses/filter -p track=zzz -f screen_name text

After the ``-field`` option you must supply one or more key names from the raw JSON response object.  This will print values only for these keys.  When the ``-field`` option is omitted cli.py prints the entire JSON response object.  
