def test_short_phrase():
    phrase = input("Enter a phrase shorter than 15 characters: ")
    assert len(phrase) != 0, "Nothing entered"
    assert len(phrase) < 15, "The phrase is too long"
