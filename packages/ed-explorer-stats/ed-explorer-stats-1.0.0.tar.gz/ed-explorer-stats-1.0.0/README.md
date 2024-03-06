# ED Explorer Stats

A Python application to parse player journals and display interesting exploring stats for Elite Dangerous.

Only tested on Windows.

Use the `--saves_path` parameter to specify the path to the journal files directory on other platforms.

**Intended for ED Horizons/Odyssey, data from Legacy may or may not work**

## Install

To install use pip: `pip install ed-explorer-stats`.

## Usage

Run `explorer-stats` to list all stat groups that can be executed.

To execute a stat group, pass the name as a subcommand.

For example: `explorer-stats visited_systems` to calculate and display the total visited systems.

## Dependencies

* colorama

## Development

To develop with an editable install, run `pip install --editable .` in the source root.

## Planned Features
* Stat caching to reduce journal reading

## Todo
* Support Linux