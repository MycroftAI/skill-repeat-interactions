
# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from monotonic import monotonic

from mycroft import MycroftSkill, intent_handler


class RepeatRecentSkill(MycroftSkill):
    """Skill to repeat the last Mycroft utterance or percieved user utterance.
    """
    def __init__(self):
        MycroftSkill.__init__(self)
        self.stt_messages = []
        self.last_stt_time = 0

    def initialize(self):
        """Setup handlers for catching user sentences and Mycroft utterances.
        """
        def on_utterance(message):
            self.stt_messages.append(message.data['utterances'][0])
            self.stt_messages = self.stt_messages[-2:]
            self.last_stt_time = monotonic()

        def on_speak(message):
            self.last_tts = message.data['utterance']

        self.add_event('recognizer_loop:utterance', on_utterance)
        self.add_event('speak', on_speak)

        nothing = self.translate('nothing')
        self.last_tts = nothing
        self.stt_messages = [nothing]

    @intent_handler('repeat.tts.intent')
    def handle_repeat_tts(self):
        self.speak_dialog('repeat.tts', dict(tts=self.last_tts))

    @intent_handler('repeat.stt.intent')
    def handle_repeat_stt(self):
        if monotonic() - self.last_stt_time > 120:
            self.speak_dialog('repeat.stt.old', dict(stt=self.stt_messages[0]))
        else:
            self.speak_dialog('repeat.stt', dict(stt=self.stt_messages[0]))

    @intent_handler('did.you.hear.me.intent')
    def handle_did_you_hear_me(self):
        if monotonic() - self.last_stt_time > 60:
            self.speak_dialog('did.not.hear')
            self.speak_dialog('please.repeat', expect_response=True)
        else:
            self.speak_dialog('did.hear')
            self.speak_dialog('repeat.stt', dict(stt=self.stt_messages[0]))


def create_skill():
    return RepeatRecentSkill()
