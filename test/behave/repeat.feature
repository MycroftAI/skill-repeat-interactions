Feature: repeat-interactions

  Scenario: Repeat TTS
    Given an english speaking user
     When the user says "say audacious zebra"
     Then mycroft reply should contain "audacious zebra"
     When the user says "what did you just say"
     Then "repeat-interactions" should reply with "I said, audacious zebra"

  Scenario: Repeat STT
    Given an english speaking user
     When the user says "say audacious zebra"
     Then mycroft reply should contain "audacious zebra"
     When the user says "what did I just say"
     Then "repeat-interactions" should reply with "You said, audacious zebra"
