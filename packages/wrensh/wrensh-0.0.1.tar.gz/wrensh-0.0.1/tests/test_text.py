#!/usr/bin/env python

import tempfile

from wrensh import text

sentence1 = "The quick brown fox jumps over the lazy dog".split(" ")
sentence2 = "Lorem ipsum dolor sit amet".split(" ")

def test_file_io():
    with tempfile.TemporaryDirectory() as tmp:
        text.echo(sentence1).redirect(f"{tmp}/a")
        assert text.cat(f"{tmp}/a").pipe == sentence1, "failed to write sentence to file and read it back again"

        text.echo(sentence2).redirect(f"{tmp}/b")
        text.echo(sentence2).append(f"{tmp}/b")
        assert text.cat(f"{tmp}/b").pipe == (2 * sentence2), "failed to append to file"

        text.cat(f"{tmp}/a", f"{tmp}/b").redirect(f"{tmp}/c")
        assert text.cat(f"{tmp}/c").pipe == (sentence1 + (2 * sentence2)), "failed to cat multiple files"

def test_sort_uniq():
    unsorted = ["3", "1", "4", "1", "5", "9", "2", "7", "1", "8", "2", "8"]
    sorted = ["1", "1", "1", "2", "2", "3", "4", "5", "7", "8", "8", "9"]
    unique = ["1", "2", "3", "4", "5", "7", "8", "9"]
    sh = text.TextWrensh(unsorted)
    assert sh.pipe == unsorted, "failed to initialize unsorted wrensh"
    sh = sh.sort()
    assert sh.pipe == sorted, "failed to sort"
    sh = sh.uniq()
    assert sh.pipe == unique, "failed to deduplicate"

def test_head_tail():
    whole = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    sh = text.TextWrensh(whole)
    sh = sh.head(5)
    assert sh.pipe == ["0", "1", "2", "3", "4"]

    sh = text.TextWrensh(whole)
    sh = sh.tail(5)
    assert sh.pipe == ["5", "6", "7", "8", "9"]

    sh = text.TextWrensh(whole)
    sh = sh.head(15)
    assert sh.pipe == whole

    sh = text.TextWrensh(whole)
    sh = sh.tail(15)
    assert sh.pipe == whole

def test_grep():
    haystack = "Maybe you should use a pitch fork instead of a needle next time".split(" ")
    sh = text.TextWrensh(haystack)
    sh = sh.grep("e{2}")
    assert str(sh) == "needle"

def test_map():
    sh = text.TextWrensh(sentence1)
    sh = sh.map(lambda x: x.upper())
    assert sh.pipe == " ".join(sentence1).upper().split(" "), "map that emitted strings failed"

    sh = text.TextWrensh(sentence1)
    sh = sh.map(lambda x: list(x.upper()))
    assert sh.pipe == list("".join(sentence1).upper()), "map that emitted lists failed"

    sh = text.TextWrensh(sentence1)
    sh = sh.map(lambda x: None if x.lower() == "the" else x)
    assert str(sh) == "quick\nbrown\nfox\njumps\nover\nlazy\ndog", "map that had null values failed"
