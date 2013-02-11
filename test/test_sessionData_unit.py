# own modules
from model import SessionData

import unittest

class UnitTests_SessionData(unittest.TestCase):
    def testSessionData(self):
        good_email = 'good@aisoft.hu'
        bad_email = 'bad@aisoft.hu'
        ip = '127.0.0.1'
        sessionid = SessionData.generateId()
        session = SessionData(key_name=sessionid)
        session.sessionid = sessionid
        session.email = good_email
        session.ip = ip
        otherid = SessionData.generateId()
        self.assertNotEqual(session.sessionid, otherid, 'Two ids generated are the same.')
        self.assertNotEqual('', session.sessionid, 'Empty id generated: ' + str(session.sessionid))
        session.put()
        start_date = session.startdate
        
        valid_session = SessionData.getSession(sessionid)
        self.assertIsNotNone(valid_session, 'Stored session not found')
        self.assertTrue(valid_session.isValid(), 'isValid returned False for a valid session')
        self.assertEqual(good_email, valid_session.email, 'Email field is wrong for returned session')
        self.assertEqual(ip, valid_session.ip, 'IP field is wrong for returned session.')
        self.assertEqual(start_date, valid_session.startdate, 'Startdate field is wrong for returned session.')
        
        valid_session.update_startdate()
        new_start_date = valid_session.startdate
        self.assertNotEqual(start_date, valid_session.startdate, 'Startdate field is wrong after updating')
        
        valid_session = SessionData.getSession(sessionid)
        self.assertNotEqual(start_date, valid_session.startdate, 'Startdate field is wrong after updating')
        self.assertEqual(new_start_date, valid_session.startdate, 'Startdate field is wrong after updating')
        
        invalid_session = SessionData.getSession(otherid)
        self.assertIsNone(invalid_session, 'Valid session found for invalid id')
        
        valid_session.delete()
        valid_session = SessionData.getSession(sessionid)
        self.assertIsNone(valid_session, 'Valid session found for deleted id')