# Text v2 plugin HTTP API

The text plugin name is `text_v2`, so all its routes are under
`/data/plugin/text_v2`.

## `/data/plugin/text_v2/tags`

Retrieves an index of tags containint text data.

Returns a dictionary mapping from `runName` (quoted string) to an
array of `tagName`. Here is an example:

  {
    "text_demo_run": [
      "simple_example/greeting",
      "markdown_table/chocolate_study",
      "higher_order_tensors/multiplication_table"
    ]
  }

Runs without any text tags are omitted from the result.

## `/data/plugin/text_v2/text?run=foo&tag=bar`

Returns an array of text events for the given run and tag.  Each event is
a dictionary with members `wall_time`, `step`, `text`, `shape`, and `warning`, 
where `wall_time` is a floating-point number of seconds since epoch, `step` is 
an integer step counter, `text` is an n-dimensional array, `shape` is an array
of the sizes of each dimension, and `warning` is a string relating some warning
in parsing the text summary, or an empty string if there is no warning.

Example:

  {
    shape: [2, 2]
    step: 1
    text: [["×", "**0**"], ["**0**", "0"]]
    wall_time: 1591289315.824522
    warning: ""
  }
