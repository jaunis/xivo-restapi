Feature: REST API Extensions

    Scenario: Extension list with no extensions
        Given I have no extensions
        When I access the list of extensions
        Then I get a list with only the default extensions

    Scenario: Extension list with one extension
        Given I only have the following extensions:
            | exten | context | type | typeval |
            | 1000  | default | user | 1       |
        When I access the list of extensions
        Then I get a list containing the following extensions:
            | exten | context |
            | 1000  | default |

    Scenario: Extension list with one extension
        Given I only have the following extensions:
            | exten | context | type | typeval |
            | 1001  | default | user | 2       |
            | 1000  | default | user | 1       |
        When I access the list of extensions
        Then I get a list containing the following extensions:
            | exten | context |
            | 1000  | default |
            | 1001  | default |

    Scenario: User link list by extension_id with no link
        Given I have no extensions
        When I ask for the list of user_links with extension_id "10"
        Then I get a response with status "200"
        Then I get an empty list

    Scenario: User link list by extension_id with 1 user
        Given I only have the following users:
            | id | firstname | lastname  |
            | 1  | Greg      | Sanderson |
        Given I only have the following lines:
            | id | context | protocol | device_slot |
            | 10 | default | sip      | 1           |
        Given I only have the following extensions:
            | id  | context | exten |
            | 100 | default | 1000  |
        Given the following users, lines, extensions are linked:
            | user_id | line_id | extension_id |
            | 1       | 10      | 100          |
        When I ask for the list of user_links with extension_id "100"
        Then I get a response with status "200"
        Then I get the user_links with the following parameters:
            | user_id | line_id | extension_id |
            | 1       | 10      | 100          |

    Scenario: User link list by extension_id with 2 users
        Given I only have the following users:
            | id | firstname | lastname  |
            | 1  | Greg      | Sanderson |
            | 2  | Cedric    | Abunar    |
        Given I only have the following lines:
            | id | context | protocol | device_slot |
            | 10 | default | sip      | 1           |
        Given I only have the following extensions:
            | id  | context | exten |
            | 100 | default | 1000  |
        Given the following users, lines, extensions are linked:
            | user_id | line_id | extension_id |
            | 1       | 10      | 100          |
            | 2       | 10      | 100          |
        When I ask for the list of user_links with extension_id "100"
        Then I get a response with status "200"
        Then I get the user_links with the following parameters:
            | user_id | line_id | extension_id |
            | 1       | 10      | 100          |
            | 2       | 10      | 100          |

    Scenario: Get an extension that does not exist
        Given I have no extensions
        When I access the extension with id "100"
        Then I get a response with status "404"

    Scenario: Get an extension
        Given I only have the following extensions:
            | id  | exten | context | type | typeval |
            | 100 | 1500  | default | user | 1       |
        When I access the extension with id "100"
        Then I get a response with status "200"
        Then I have an extension with the following parameters:
            | id  | exten | context |
            | 100 | 1500  | default |

    Scenario: Creating an empty extension
        Given I have no extensions
        When I create an empty extension
        Then I get a response with status "400"
        Then I get an error message "Missing parameters: exten,context"

    Scenario: Creating an extension with an empty number
        Given I have no extensions
        When I create an extension with the following parameters:
            | exten | context |
            |       | default |
        Then I get a response with status "400"
        Then I get an error message "Invalid parameters: Exten required"

    Scenario: Creating an extension with an empty context
        Given I have no extensions
        When I create an extension with the following parameters:
            | exten | context |
            | 1000  |         |
        Then I get a response with status "400"
        Then I get an error message "Invalid parameters: Context required"

    Scenario: Creating an extension with only the number
        Given I have no extensions
        When I create an extension with the following parameters:
            | exten |
            | 1000  |
        Then I get a response with status "400"
        Then I get an error message "Missing parameters: context"

    Scenario: Creating an extension with only the context
        Given I have no extensions
        When I create an extension with the following parameters:
            | context |
            | default |
        Then I get a response with status "400"
        Then I get an error message "Missing parameters: exten"

    Scenario: Creating an extension with invalid parameters
        Given I have no extensions
        When I create an extension with the following parameters:
            | toto |
            | tata |
        Then I get a response with status "400"
        Then I get an error message "Invalid parameters: toto"

    Scenario: Creating a commented extension
        Given I have no extensions
        When I create an extension with the following parameters:
            | exten | context | commented |
            | 1000  | default | true      |
        Then I get a response with status "201"
        Then I get a response with an id
        Then I get a header with a location for the "extensions" resource
        Then I get a response with a link to the "extensions" resource

    Scenario: Creating an extension that isn't commented
        Given I have no extensions
        When I create an extension with the following parameters:
            | exten | context | commented |
            | 1000  | default | false     |
        Then I get a response with status "201"
        Then I get a response with an id
        Then I get a header with a location for the "extensions" resource
        Then I get a response with a link to the "extensions" resource

    Scenario: Creating an extension in user range
        Given I have no extensions
        When I create an extension with the following parameters:
            | exten | context |
            | 1000  | default |
        Then I get a response with status "201"
        Then I get a response with an id
        Then I get a header with a location for the "extensions" resource
        Then I get a response with a link to the "extensions" resource

    Scenario: Creating an extension in group range
        Given I have no extensions
        When I create an extension with the following parameters:
            | exten | context |
            | 2000  | default |
        Then I get a response with status "201"
        Then I get a response with an id
        Then I get a header with a location for the "extensions" resource
        Then I get a response with a link to the "extensions" resource

    Scenario: Creating an extension in queue range
        Given I have no extensions
        When I create an extension with the following parameters:
            | exten | context |
            | 3000  | default |
        Then I get a response with status "201"
        Then I get a response with an id
        Then I get a header with a location for the "extensions" resource
        Then I get a response with a link to the "extensions" resource

    Scenario: Creating an extension in conference room range
        Given I have no extensions
        When I create an extension with the following parameters:
            | exten | context |
            | 4000  | default |
        Then I get a response with status "201"
        Then I get a response with an id
        Then I get a header with a location for the "extensions" resource
        Then I get a response with a link to the "extensions" resource

    Scenario: Creating an extension in incall range
        Given I have no extensions
        When I create an extension with the following parameters:
            | exten | context     |
            |  3954 | from-extern |
        Then I get a response with status "201"
        Then I get a response with an id
        Then I get a header with a location for the "extensions" resource
        Then I get a response with a link to the "extensions" resource

    Scenario: Creating an alphanumeric extension
        Given I have no extensions
        When I create an extension with the following parameters:
            | exten  | context |
            | ABC123 | default |
        Then I get a response with status "400"
        Then i get an error message "Invalid parameters: Alphanumeric extensions are not supported"

    Scenario: Creating twice the same extension
        Given I have no extensions
        When I create an extension with the following parameters:
            | exten | context |
            | 1000  | default |
        Then I get a response with status "201"
        When I create an extension with the following parameters:
            | exten | context |
            | 1000  | default |
        Then I get a response with status "400"
        Then I get an error message "Extension 1000@default already exists"

    Scenario: Creating two extensions in different contexts
        Given I have no extensions
        When I create an extension with the following parameters:
            | exten | context |
            | 1000  | default |
        Then I get a response with status "201"
        When I create an extension with the following parameters:
            | exten | context     | type   |
            | 1000  | from-extern | incall |
        Then I get a response with status "201"

    Scenario: Creating an extension with a context that doesn't exist
        Given I have no extensions
        When I create an extension with the following parameters:
            | exten | context             |
            | 1000  | mysuperdupercontext |
        Then I get a response with status "400"
        Then I get an error message "Nonexistent parameters: context mysuperdupercontext does not exist"

    Scenario: Creating an extension outside of context range
        Given I have no extensions
        When I create an extension with the following parameters:
            | exten | context |
            | 99999 | default |
        Then I get a response with status "400"
        Then I get an error message "Invalid parameters: exten 99999 not inside range of context default"

    Scenario: Editing an extension that doesn't exist
        Given I have no extensions
        When I update the extension with id "9999" using the following parameters:
          | exten |
          | 1001  |
        Then I get a response with status "404"

    Scenario: Editing an extension with parameters that don't exist
        Given I only have the following extensions:
          | id  | exten | context | type | typeval |
          | 100 | 1001  | default | user | 1       |
        When I update the extension with id "100" using the following parameters:
          | unexisting_field |
          | unexisting value |
        Then I get a response with status "400"
        Then I get an error message "Invalid parameters: unexisting_field"

    Scenario: Editing the exten of a extension
        Given I only have the following extensions:
          | id  | exten | context | type | typeval |
          | 100 | 1001  | default | user | 1       |
        When I update the extension with id "100" using the following parameters:
          | exten |
          | 1003  |
        Then I get a response with status "204"
        When I ask for the extension with id "100"
        Then I have an extension with the following parameters:
          | id  | exten | context |
          | 100 | 1003  | default |

    Scenario: Editing an extension with an exten outside of context range
        Given I only have the following extensions:
          | id  | exten | context | type | typeval |
          | 100 | 1001  | default | user | 1       |
        When I update the extension with id "100" using the following parameters:
          | exten |
          | 9999  |
      Then I get a response with status "400"
      Then I get an error message "Invalid parameters: exten 9999 not inside range of context default"

    Scenario: Editing the context of a extension
        Given I only have the following extensions:
          | id  | exten | context | type | typeval |
          | 100 | 1001  | default | user | 1       |
        Given I have the following context:
          | name | numberbeg | numberend |
          | toto | 1000      | 1999      |
        When I update the extension with id "100" using the following parameters:
          | context |
          | toto    |
        Then I get a response with status "204"
        When I ask for the extension with id "100"
        Then I have an extension with the following parameters:
          | id  | exten | context |
          | 100 | 1001  | toto    |

    Scenario: Editing the extension with a context that doesn't exist
        Given I only have the following extensions:
          | id  | exten | context | type | typeval |
          | 100 | 1001  | default | user | 1       |
        When I update the extension with id "100" using the following parameters:
          | context             |
          | mysuperdupercontext |
        Then I get a response with status "400"
        Then I get an error message "Nonexistent parameters: context mysuperdupercontext does not exist"

    Scenario: Editing the exten, context of a extension
        Given I only have the following extensions:
          | id  | exten | context | type | typeval |
          | 100 | 1001  | default | user | 1       |
        Given I have the following context:
          | name   | numberbeg | numberend |
          | patate | 1000      | 1999      |
        When I update the extension with id "100" using the following parameters:
          | exten | context |
          | 1006  | patate  |
        Then I get a response with status "204"
        When I ask for the extension with id "100"
        Then I have an extension with the following parameters:
          | id  | exten | context |
          | 100 | 1006  | patate  |

    Scenario: Editing a commented extension
        Given I only have the following extensions:
          | id  | exten | context | type | typeval | commented |
          | 100 | 1007  | default | user | 1       | true      |
        When I update the extension with id "100" using the following parameters:
          | commented |
          | false     |
        Then I get a response with status "204"
        When I ask for the extension with id "100"
        Then I have an extension with the following parameters:
          | id  | exten | context | commented |
          | 100 | 1007  | default | false     |

    Scenario: Delete an extension that doesn't exist
        Given I have no extensions
        When I delete extension "100"
        Then I get a response with status "404"

    Scenario: Delete an extension
        Given I only have the following extensions:
            | id  | exten | context | type | typeval |
            | 100 | 1000  | default | user | 1       |
        When I delete extension "100"
        Then I get a response with status "204"
        Then the extension "100" no longer exists

    Scenario: Delete an extension still has a link
        Given I only have the following users:
            | id | firstname | lastname |
            | 1  | Clémence  | Dupond   |
        Given I only have the following lines:
            | id | context | protocol | device_slot |
            | 10 | default | sip      | 1           |
        Given I only have the following extensions:
            | id  | context | exten | type | typeval |
            | 100 | default | 1000  | user | 1       |
        When I create the following links:
            | user_id | line_id | extension_id | main_line |
            | 1       | 10      | 100          | True      |

        When I delete extension "100"
        Then I get a response with status "400"
        Then I get an error message "Error while deleting Extension: extension still has a link"
