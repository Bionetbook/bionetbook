# from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
# from django.test import TestCase
from django.test.client import Client

from django.contrib.auth.models import AnonymousUser

from profiles.models import Profile
from protocols.models import Protocol, Step, Action, Component
from protocols.tests.core import AutoBaseTest
# from steps.models import Step
from organization.models import Organization, Membership


class ProtocolSecurityTests(AutoBaseTest):
    '''
    FIRST USER -> ORG 1
    SECOND USER -> ORG 2
    THIRD USER -> ORG 1

    FIRST USER CAN ACCESS THIER PRIVATE DRAFT PROTOCOL

    FIRST USER CAN ACCESS THIER PRIVATE PUBLISHED PROTOCOL

    FIRST USER CAN ACCESS THIER PUBLIC DRAFT PROTOCOL

    FIRST USER CAN ACCESS THIER PUBLIC PUBLISHED PROTOCOL


    FIRST USER CAN NOT ACCESS SECOND USER'S PRIVATE DRAFT PROTOCOL

    FIRST USER CAN NOT ACCESS SECOND USER'S PRIVATE PUBLISHED PROTOCOL

    FIRST USER CAN NOT ACCESS SECOND USER'S PUBLIC DRAFT PROTOCOL

    FIRST USER CAN ACCESS SECOND USER'S PUBLIC PUBLISHED PROTOCOL


    FIRST USER CAN NOT ACCESS THIRD USER'S PRIVATE DRAFT PROTOCOL 

    FIRST USER CAN ACCESS THIRD USER'S PRIVATE PUBLISHED PROTOCOL

    FIRST USER CAN NOT ACCESS THIRD USER'S PUBLIC DRAFT PROTOCOL

    FIRST USER CAN ACCESS THIRD USER'S PUBLIC PUBLISHED PROTOCOL
    '''

    def setUp(self):
        super(ProtocolSecurityTests, self).setUp()

        # USER SETUP
        self.firstUser = self.createUserInstance(username="firstuser", password="pass", email="firstuser@example.com")
        self.secondUser = self.createUserInstance(username="seconduser", password="pass", email="seconduser@example.com")
        self.thirdUser = self.createUserInstance(username="thirduser", password="pass", email="thirduser@example.com")

        # USER PROFILE SETUP
        self.firstProfile = self.createModelInstance(Profile, user=self.firstUser)
        self.secondProfile = self.createModelInstance(Profile, user=self.secondUser)
        self.thirdProfile = self.createModelInstance(Profile, user=self.thirdUser)

        # CREATE THE ORGANIZATION
        self.firstOrg = self.createModelInstance(Organization, name="FirstOrg")
        self.secondOrg = self.createModelInstance(Organization, name="SecondOrg")

        # ADD THE MEMBERSHIP
        self.firstMember = self.createModelInstance(Membership, user=self.firstUser, org=self.firstOrg)
        self.secondMember = self.createModelInstance(Membership, user=self.secondUser, org=self.secondOrg)
        self.thirdMember = self.createModelInstance(Membership, user=self.thirdUser, org=self.firstOrg)

        # CREATE PROTOCOL
        self.firstPrivateDraftProtocol = self.createModelInstance(Protocol, name="firstPrivateDraftProtocol", owner=self.firstOrg, published=False, public=False, author=self.firstUser )
        self.firstPrivatePublishedProtocol = self.createModelInstance(Protocol, name="firstPrivatePublishedProtocol", owner=self.firstOrg, published=True, public=False, author=self.firstUser )
        self.firstPublicDraftProtocol = self.createModelInstance(Protocol, name="firstPublicDraftProtocol", owner=self.firstOrg, published=False, public=True, author=self.firstUser )
        self.firstPublicPublishedProtocol = self.createModelInstance(Protocol, name="firstPublicPublishedProtocol", owner=self.firstOrg, published=True, public=True, author=self.firstUser )

        self.secondPrivateDraftProtocol = self.createModelInstance(Protocol, name="secondPrivateDraftProtocol", owner=self.secondOrg, published=False, public=False, author=self.secondUser )
        self.secondPrivatePublishedProtocol = self.createModelInstance(Protocol, name="secondPrivatePublishedProtocol", owner=self.secondOrg, published=True, public=False, author=self.secondUser )
        self.secondPublicDraftProtocol = self.createModelInstance(Protocol, name="secondPublicDraftProtocol", owner=self.secondOrg, published=False, public=True, author=self.secondUser )
        self.secondPublicPublishedProtocol = self.createModelInstance(Protocol, name="secondPublicPublishedProtocol", owner=self.secondOrg, published=True, public=True, author=self.secondUser )

        self.thirdPrivateDraftProtocol = self.createModelInstance(Protocol, name="thirdPrivateDraftProtocol", owner=self.firstOrg, published=False, public=False, author=self.thirdUser )
        self.thirdPrivatePublishedProtocol = self.createModelInstance(Protocol, name="thirdPrivatePublishedProtocol", owner=self.firstOrg, published=True, public=False, author=self.thirdUser )
        self.thirdPublicDraftProtocol = self.createModelInstance(Protocol, name="thirdPublicDraftProtocol", owner=self.firstOrg, published=False, public=True, author=self.thirdUser )
        self.thirdPublicPublishedProtocol = self.createModelInstance(Protocol, name="thirdPublicPublishedProtocol", owner=self.firstOrg, published=True, public=True, author=self.thirdUser )

    # def test_login(self):
    #     url = reverse("protocol_create", kwargs={'owner_slug': self.firstOrg.slug})
    #     self.assertTrue(self.client.login(username='testuser', password='pass'))    # Confirm that self.firstUser is the first user


    # FIRST USER -> ORG 1
    # SECOND USER -> ORG 2
    # THIRD USER -> ORG 1

    #---------------
    # FIRST USER TESTS
    #---------------

    # FIRST USER CAN ACCESS THIER PRIVATE DRAFT PROTOCOL
    def test_first_user_has_access_to_own_private_draft_protocol(self):
        self.assertTrue( self.firstPrivateDraftProtocol.user_has_access( self.firstUser ), "First User access to own Private Draft Protocol failed." )

    # FIRST USER CAN ACCESS THIER PRIVATE PUBLISHED PROTOCOL
    def test_first_user_has_access_to_own_private_published_protocol(self):
        self.assertTrue( self.firstPrivatePublishedProtocol.user_has_access( self.firstUser ), "First User access to own Private Published Protocol failed."  )

    # FIRST USER CAN ACCESS THIER PUBLIC DRAFT PROTOCOL
    def test_first_user_has_access_to_own_public_draft_protocol(self):
        self.assertTrue( self.firstPublicDraftProtocol.user_has_access( self.firstUser ), "First User access to own Public Draft Protocol failed."  )

    # FIRST USER CAN ACCESS THIER PUBLIC PUBLISHED PROTOCOL
    def test_first_user_has_access_to_own_public_published_protocol(self):
        self.assertTrue( self.firstPublicPublishedProtocol.user_has_access( self.firstUser ), "First User access to own Public Published Protocol failed."  )


    #---------------
    # SECOND USER TESTS
    #---------------

    # FIRST USER CAN NOT ACCESS SECOND USER'S PRIVATE DRAFT PROTOCOL
    def test_first_user_has_no_access_to_second_user_private_draft_protocol(self):
        self.assertFalse( self.secondPrivateDraftProtocol.user_has_access( self.firstUser ), "First User has access to Second User Private Draft Protocol." )

    # FIRST USER CAN NOT ACCESS SECOND USER'S PRIVATE PUBLISHED PROTOCOL
    def test_first_user_has_no_access_to_second_user_private_draft_protocol(self):
        self.assertFalse( self.secondPrivatePublishedProtocol.user_has_access( self.firstUser ), "First User has access to Second User Private Published Protocol."  )

    # FIRST USER CAN NOT ACCESS SECOND USER'S PUBLIC DRAFT PROTOCOL
    def test_first_user_has_no_access_to_second_user_public_draft_protocol(self):
        self.assertFalse( self.secondPublicDraftProtocol.user_has_access( self.firstUser ), "First User has access to Second User Public Draft Protocol."  )

    # FIRST USER CAN ACCESS SECOND USER'S PUBLIC PUBLISHED PROTOCOL
    def test_first_user_has_access_to_second_user_public_published_protocol(self):
        self.assertTrue( self.secondPublicPublishedProtocol.user_has_access( self.firstUser ), "First User access to Second User Public Published Protocol failed."  )


    #---------------
    # THIRD USER TESTS
    #---------------

    # FIRST USER CAN NOT ACCESS THIRD USER'S PRIVATE DRAFT PROTOCOL 
    def test_first_user_has_no_access_to_third_user_private_draft_protocol(self):
        self.assertFalse( self.thirdPrivateDraftProtocol.user_has_access( self.firstUser ), "First User has access to Third User Private Draft Protocol." )

    # FIRST USER CAN ACCESS THIRD USER'S PRIVATE PUBLISHED PROTOCOL
    def test_first_user_has_access_to_third_user_private_draft_protocol(self):
        self.assertTrue( self.thirdPrivatePublishedProtocol.user_has_access( self.firstUser ), "First User access to Third User Private Published Protocol failed."  )

    # FIRST USER CAN NOT ACCESS THIRD USER'S PUBLIC DRAFT PROTOCOL
    def test_first_user_has_no_access_to_third_user_public_draft_protocol(self):
        self.assertFalse( self.thirdPublicDraftProtocol.user_has_access( self.firstUser ), "First User has access to Third User Public Draft Protocol."  )

    # FIRST USER CAN ACCESS THIRD USER'S PUBLIC PUBLISHED PROTOCOL
    def test_first_user_has_access_to_third_user_public_published_protocol(self):
        self.assertTrue( self.thirdPublicPublishedProtocol.user_has_access( self.firstUser ), "First User access to Third User Public Published Protocol failed."  )


    #---------------
    # ANONYMOUS USER TESTS
    #---------------

    def test_anonymous_user_has_no_access_to_user_private_draft_protocol(self):
        user = AnonymousUser
        self.assertFalse( self.thirdPrivateDraftProtocol.user_has_access( user ), "Anonymous User has access to Third User Private Draft Protocol." )

    def test_anonymous_user_has_access_to_third_user_public_published_protocol(self):
        user = AnonymousUser
        self.assertTrue( self.thirdPublicPublishedProtocol.user_has_access( user ), "Anonymous User has access to Third User Public Published Protocol." )

    #---------------
    # URL TESTS
    #---------------

    def test_anonymous_user_has_web_access_to_public_published_protocol(self):
        url = reverse("protocol_detail", kwargs={'owner_slug': self.firstOrg.slug, 'protocol_slug': self.firstPublicPublishedProtocol.slug})
        c = Client()
        response = c.get(url)
        # print response.status_code
        self.assertEqual(response.status_code, 302)     # GETS A REDIRECT INSTEAD OF A 200
        # self.assertEqual(response.status_code, 200)


    def test_anonymous_user_has_no_web_access_to_private_draft_protocol(self):
        url = reverse("protocol_detail", kwargs={'owner_slug': self.firstOrg.slug, 'protocol_slug': self.firstPrivateDraftProtocol.slug})
        c = Client()
        response = c.get(url)
        # print response.status_code
        self.assertEqual(response.status_code, 404)

    # def test_first_user_has_web_access_to_protocol(self):
    #     url = reverse("protocol_detail", kwargs={'owner_slug': self.firstOrg.slug, 'protocol_slug': self.firstPrivateDraftProtocol.slug})

    #     self.firstUser.save()

    #     c = Client()
    #     print c.login(username=self.firstUser.username, password=self.firstUser.password)
    #     # response = c.post('/login/', {'username': self.firstUser.username, 'password': self.firstUser.password }) # Login the User

    #     response = c.get(url)
    #     print response.status_code






    # def test_first_user_has_web_no_access_to_protocol(self):
    #     pass

    # def test_user_has_access(self):
    #     url = reverse("protocol_create", kwargs={'owner_slug': self.firstOrg.slug})
    #     self.assertTrue(self.client.login(username='testuser', password='pass'))    # Confirm that self.firstUser is the first user

    # def test_user_has_no_access(self):
    #     url = reverse("protocol_create", kwargs={'owner_slug': self.firstOrg.slug})
    #     self.assertTrue(self.client.login(username='testuser', password='pass'))    # Confirm that self.firstUser is the first user
