#!/usr/bin/env python
# encoding: utf-8
"""
test_session.py

Created by Orestis Markou on 2009-02-17.
Copyright (c) 2009 Orestis Markou. All rights reserved.
"""

from nose.tools import assert_equal
from mock import patch, Mock

from wixed.session import Session
from wixed.utils import EventHook
from wixed.core import BufferManager


class testSession(object):
    def test_constructor(self):
        s = Session()
        assert_equal(s.frames, [])
        assert isinstance(s.buffers, BufferManager)

    @patch('wixed.session.Frame')
    def test_frames(self, mockFrame):
        s = Session()
        frameInstance = mockFrame.return_value
        frameInstance.buffer_changed = EventHook()
        f = s.make_frame()

        assert mockFrame.called
        assert mockFrame.call_args[0][0] == s
        assert s.buffer_changed in frameInstance.buffer_changed.observers

    def test_context(self):
        s = Session()
        assert_equal(s.context,
            dict(buffers=s.buffers, session=s)
        )

    def test_keymap(self):
        s = Session()
        s.keymap['a'] = mockCommand = Mock()
        s.keydown('a')
        assert mockCommand.call_args[0][0] == s


    def test_current_buffer(self):
        s = Session()
        assert s.current_buffer is None
        b = object()
        s.buffer_changed(b)
        assert s.current_buffer == b

        
        
        


