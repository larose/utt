# Contributing to utt

First off, thanks for taking the time to contribute!

Below are the answers to the most frequently asked questions.


## How can I report an issue?

Open an issue at https://github.com/larose/utt/issues with as much
information as possible.


## How can I request a new feature?

Open an issue at https://github.com/larose/utt/issues and describe the
feature you would like.

Note that we try to keep utt lean and your feature request may be
declined. In this case, you can extend utt with a
[plugin](PLUGINS.md). We will be happy to list it in the plugins
section.


## How can I contribute a bug fix?

See [HACKING.md](HACKING.md) how to set up your environment, fix the
bug and then create a pull request with your bug fix. Your code change
must contain tests to 1) prove that it fixes the bug and 2) prevent
the same regression in the future.


## How can I contribute a new feature?

We try to keep utt as lean as possible. Before developing a new
feature, it's best to first contact Mathieu Larose
<<mathieu@mathieularose.com>> as he will guide you whether to
implement it as a core feature or as a
[plugin](#how-can-i-create-a-plugin).

If you are implementing a new feature within utt, first see
[HACKING.md](HACKING.md) how to set up your environment, then
implement your new feature and finally open a new pull request.

Your code change must contain tests.


## How can I create a plugin?

See [PLUGINS.md](PLUGINS.md) how to create a plugin.

Write to Mathieu Larose <<mathieu@mathieularose.com>> if you would
like your plugin to be listed in the [../README.md](../README.md).


## How can I contribute a non-trivial code change that is not a feature request?

Before doing a refactoring that involves many changes, it's best to
first contact Mathieu Larose <<mathieu@mathieularose.com>> to discuss
the architecture.

Then see [HACKING.md](HACKING.md) how to set up your environment, then
do your refactoring and finally open a new pull request.

Please add tests if this is relevant.
