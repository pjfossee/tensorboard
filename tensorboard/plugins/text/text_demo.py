# Copyright 2020 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from absl import app
from absl import logging
import tensorflow as tf
from tensorboard.plugins.text.summary_v2 import text

tf.compat.v1.enable_v2_behavior()

# Directory into which to write tensorboard data.
LOGDIR = "/tmp/text_demo"

# Number of steps for which to write data.
STEPS = 16


def simple_example(step):
    # Text summaries log arbitrary text. This can be encoded with ASCII or
    # UTF-8. Here's a simple example, wherein we greet the user on each
    # step:
    step_string = tf.as_string(step)
    greeting = tf.constant("hello from step %d! 😊" % step)
    text("greeting", greeting, step)


def simple_example_with_pagination(step):
    # Text summaries can be grouped by Tag (the first argument to the `text`
    # summary's API).  Unique tags will have their own dropdown in the frontend,
    # unless those tags are sub-tags of another tag.  To create a subtag name,
    # one would input MainTagName/SubTagName as the input argument to the `text`
    # summary API.  Subtags will be displayed within the main tag's dropdown,
    # and a pager will appear if there are more than 12 subtags.  This test
    # displays that UI feature by creating 36 subtags within the main tag:
    # "simple_example_with_pagination"
    for i in range(36):
        step_string = tf.as_string(step)
        greeting = tf.constant("hello from step %d! 😊" % step)
        tag = "card%d/greeting" % (i + 1)
        text(tag, greeting, step)


def markdown_table(step):
    # The text summary can also contain Markdown, including Markdown
    # tables. Markdown tables look like this:
    #
    #     | hello | there |
    #     |-------|-------|
    #     | this  | is    |
    #     | a     | table |
    #
    # The leading and trailing pipes in each row are optional, and the text
    # doesn't actually have to be neatly aligned, so we can create these
    # pretty easily. Let's do so.
    header_row = "Pounds of chocolate | Happiness"
    chocolate = tf.range(step)
    happiness = tf.square(chocolate + 1)
    chocolate_column = tf.as_string(chocolate)
    happiness_column = tf.as_string(happiness)
    table_rows = tf.strings.join([chocolate_column, " | ", happiness_column])
    table_body = tf.strings.reduce_join(inputs=table_rows, separator="\n")
    table = tf.strings.join([header_row, "---|---", table_body], separator="\n")
    preamble = "We conducted an experiment and found the following data:\n\n"
    result = tf.strings.join([preamble, table])
    text("chocolate_study", result, step)


def higher_order_tensors(step):
    # We're not limited to passing scalar tensors to the summary
    # operation. If we pass a rank-1 or rank-2 tensor, it'll be visualized
    # as a table in TensorBoard. (For higher-ranked tensors, you'll see
    # just a 2D slice of the data.)
    #
    # To demonstrate this, let's create a multiplication table.

    # First, we'll create the table body, a `step`-by-`step` array of
    # strings.
    numbers = tf.range(step)
    numbers_row = tf.expand_dims(numbers, 0)  # shape: [1, step]
    numbers_column = tf.expand_dims(numbers, 1)  # shape: [step, 1]
    products = tf.matmul(numbers_column, numbers_row)  # shape: [step, step]
    table_body = tf.as_string(products)

    # Next, we'll create a header row and column, and a little
    # multiplication sign to put in the corner.
    bold_numbers = tf.strings.join(["**", tf.as_string(numbers), "**"])
    bold_row = tf.expand_dims(bold_numbers, 0)
    bold_column = tf.expand_dims(bold_numbers, 1)
    corner_cell = tf.constant(u"\u00d7".encode("utf-8"))  # MULTIPLICATION SIGN

    # Now, we have to put the pieces together. Using `axis=0` stacks
    # vertically; using `axis=1` juxtaposes horizontally.
    table_body_and_top_row = tf.concat([bold_row, table_body], axis=0)
    table_left_column = tf.concat([[[corner_cell]], bold_column], axis=0)
    table_full = tf.concat([table_left_column, table_body_and_top_row], axis=1)

    # The result, `table_full`, is a rank-2 string tensor of shape
    # `[step + 1, step + 1]`. We can pass it directly to the summary, and
    # we'll get a nicely formatted table in TensorBoard.
    text("multiplication_table", table_full, step)


def create_run(logdir, run_name):
    # Creates a run specified by `run_name` populated with the text summaries
    # generated by the function above.
    writer = tf.summary.create_file_writer(logdir + "/" + run_name)

    with writer.as_default():
        for step in range(STEPS):
            with tf.name_scope("simple_example"):
                simple_example(step)
            with tf.name_scope("markdown_table"):
                markdown_table(step)
            with tf.name_scope("higher_order_tensors"):
                higher_order_tensors(step)
            with tf.name_scope("simple_example_with_pagination"):
                simple_example_with_pagination(step)

    writer.close()


def run_all(logdir):
    create_run(logdir, "run1")
    create_run(logdir, "run2")


def main(unused_argv):
    logging.set_verbosity(logging.INFO)
    logging.info("Saving output to %s." % LOGDIR)
    run_all(LOGDIR)
    logging.info("Done. Output saved to %s." % LOGDIR)


if __name__ == "__main__":
    app.run(main)
