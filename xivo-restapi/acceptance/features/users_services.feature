Feature: Users services

	Scenario: enable DND for a user
	  Given there is a user "John MacNey"
	  Then I can enable DND for this user

	Scenario: disable DND for a user
	  Given there is a user "Hanna Milonne"
	  Then I can disable DND for this user