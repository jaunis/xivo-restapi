Feature: REST API Devices

    Scenario: Create a device with no parameters
        When I create an empty device
        Then I get a response with status "201"
        Then I get a response with a device id
        Then I get a header with a location for the "devices" resource
        Then I get a response with a link to the "devices" resource

    Scenario: Create a device with one parameter
        When I create the following devices:
            | ip       |
            | 10.0.0.1 |
        Then I get a response with status "201"
        Then I get a response with a device id
        Then I get a header with a location for the "devices" resource
        Then I get a response with a link to the "devices" resource
        Then the device has the following parameters:
            | ip       |
            | 10.0.0.1 |

    Scenario: Create a device with an invalid ip address
        When I create the following devices:
            | ip           | mac               |
            | 10.389.34.21 | 00:11:22:33:44:50 |
        Then I get a response with status "400"
        Then I get an error message "Invalid parameters: ip"
        When I create the following devices:
            | ip            | mac               |
            | 1024.34.34.21 | 00:11:22:33:44:50 |
        Then I get a response with status "400"
        Then I get an error message "Invalid parameters: ip"

    Scenario: Create a device with an invalid mac address
        When I create the following devices:
            | ip       | mac               |
            | 10.0.0.1 | ZZ:11:22:33:44:50 |
        Then I get a response with status "400"
        Then I get an error message "Invalid parameters: mac"
        When I create the following devices:
            | ip       | mac                |
            | 10.0.0.1 | 00:11:22:DF5:44:50 |
        Then I get a response with status "400"
        Then I get an error message "Invalid parameters: mac"
        When I create the following devices:
            | ip       | mac            |
            | 10.0.0.1 | 11:22:33:44:50 |
        Then I get a response with status "400"
        Then I get an error message "Invalid parameters: mac"

    Scenario: Create a device with ip and mac
        Given there are no devices with mac "00:11:22:33:44:51"
        When I create the following devices:
            | ip       | mac               |
            | 10.0.0.1 | 00:11:22:33:44:51 |
        Then I get a response with status "201"
        Then I get a response with a device id
        Then I get a header with a location for the "devices" resource
        Then I get a response with a link to the "devices" resource
        Then the device has the following parameters:
            | ip       | mac               |
            | 10.0.0.1 | 00:11:22:33:44:51 |

    Scenario: Create 2 devices with same mac
        Given there are no devices with mac "00:11:22:33:44:52"
        When I create the following devices:
            | ip       | mac               |
            | 10.0.0.2 | 00:11:22:33:44:52 |
        Then I get a response with status "201"
        When I create the following devices:
            | ip       | mac               |
            | 10.0.0.3 | 00:11:22:33:44:52 |
        Then I get a response with status "400"
        Then I get an error message "device 00:11:22:33:44:52 already exists"

    Scenario: Create 2 devices with the same ip address
        Given there are no devices with mac "00:11:22:33:44:53"
        Given there are no devices with mac "00:11:22:33:44:54"
        When I create the following devices:
            | ip       | mac               |
            | 10.0.0.4 | 00:11:22:33:44:53 |
        Then I get a response with status "201"
        When I create the following devices:
            | ip       | mac               |
            | 10.0.0.4 | 00:11:22:33:44:54 |
        Then I get a response with status "201"

    Scenario: Create a device with a plugin that doesn't exist
        Given there are no devices with mac "00:11:22:33:44:55"
        When I create the following devices:
            | ip       | mac               | plugin                   |
            | 10.0.0.5 | 00:11:22:33:44:55 | mysuperduperplugin-1.2.3 |
        Then I get a response with status "400"
        Then I get an error message "Nonexistent parameters: plugin mysuperduperplugin-1.2.3 does not exist"

    Scenario: Create a device with a plugin
        Given there are no devices with mac "00:11:22:33:44:56"
        Given the plugin "null" is installed
        When I create the following devices:
            | ip       | mac               | plugin |
            | 10.0.0.6 | 00:11:22:33:44:56 | null   |
        Then I get a response with status "201"
        Then I get a response with a device id
        Then I get a header with a location for the "devices" resource
        Then I get a response with a link to the "devices" resource
        Then the device has the following parameters:
            | ip       | mac               | plugin |
            | 10.0.0.6 | 00:11:22:33:44:56 | null   |

    Scenario: Create a device with a config template that doesn't exist
        When I create a device using the device template id "mysuperduperdevicetemplate"
        Then I get a response with status "400"
        Then I get an error message "Nonexistent parameters: template_id mysuperduperdevicetemplate does not exist"

    Scenario: Create a device with a config template
        Given there exists the following device templates:
            | id       | label        |
            | abcd1234 | testtemplate |
        When I create a device using the device template id "abcd1234"
        Then I get a response with status "201"
        Then I get a response with a device id
        Then I get a header with a location for the "devices" resource
        Then I get a response with a link to the "devices" resource
        Then the device has the following parameters:
            | template_id |
            | abcd1234    |

    Scenario: Create a device with all parameters
        Given there are no devices with mac "00:11:22:33:44:55"
        Given the plugin "null" is installed
        Given there exists the following device templates:
            | id         | label        |
            | mytemplate | testtemplate |
        When I create the following devices:
            | ip       | mac               | sn | plugin | model     | vendor     | version | description | options               | template_id |
            | 10.0.0.1 | 00:11:22:33:44:55 | XX | null   | nullmodel | nullvendor | 1.0     | example     | {"switchboard": True} | mytemplate  |
        Then I get a response with status "201"
        Then I get a response with a device id
        Then I get a header with a location for the "devices" resource
        Then I get a response with a link to the "devices" resource
        Then the device has the following parameters:
            | ip       | mac               | sn | plugin | model     | vendor     | version | description | options               | template_id |
            | 10.0.0.1 | 00:11:22:33:44:55 | XX | null   | nullmodel | nullvendor | 1.0     | example     | {"switchboard": True} | mytemplate  |
            
        Given there are users with infos:
            | firstname | lastname | number | context | protocol |            device |
            | Aayla     | Secura   |   1234 | default | sip      | 00:11:22:33:44:55 |
        Then I get a response with a link to the "devices" resource
        Then the device has the following parameters:
            | ip       | mac               | sn | plugin | model     | vendor     | version | description | options               | template_id |
            | 10.0.0.1 | 00:11:22:33:44:55 | XX | null   | nullmodel | nullvendor | 1.0     | example     | {"switchboard": True} | mytemplate  |

    Scenario: Synchronize a device
        Given there are no devices with id "123"
        Given there are no devices with mac "00:00:00:00:aa:01"
        Given I have the following devices:
          | id  | ip             | mac               |
          | 123 | 192.168.32.197 | 00:00:00:00:aa:01 |
        When I synchronize the device "123" from restapi
        Then I see in the log file device "123" synchronized

    Scenario: Edit a device with no parameters
        Given I have the following devices:
            | ip       | mac               |
            | 10.0.0.1 | 00:11:22:33:44:55 |
        When I edit the device with mac "00:11:22:33:44:55" using no parameters
        Then I get a response with status "204"
        When I go get the device with mac "00:11:22:33:44:55" using its id
        Then I get a response with status "200"
        Then the device has the following parameters:
            | ip       | mac               |
            | 10.0.0.1 | 00:11:22:33:44:55 |

    Scenario: Edit a device with ip and mac
        Given I have the following devices:
            | ip       | mac               |
            | 10.0.0.1 | 00:11:22:33:44:55 |
        When I edit the device with mac "00:11:22:33:44:55" using the following parameters:
            | ip       | mac               |
            | 10.0.0.2 | 00:11:22:33:44:55 |
        Then I get a response with status "204"
        When I go get the device with mac "00:11:22:33:44:55" using its id
        Then I get a response with status "200"
        Then the device has the following parameters:
            | ip | mac               |
            | 10.0.0.2 | 00:11:22:33:44:55 |

    Scenario: Edit a device by adding new parameters
        Given the plugin "null" is installed
        Given there exists the following device templates:
            | id         | label        |
            | mytemplate | testtemplate |
        Given there are no devices with mac "aa:11:22:33:44:55"
        Given I have the following devices:
            | mac               |
            | 00:11:22:33:44:55 |
        When I edit the device with mac "00:11:22:33:44:55" using the following parameters:
            | ip       | mac               | plugin | model     | vendor     | version | template_id |
            | 10.1.0.1 | aa:11:22:33:44:55 | null   | nullmodel | nullvendor | 1.0     | mytemplate  |
        Then I get a response with status "204"
        When I go get the device with mac "aa:11:22:33:44:55" using its id
        Then I get a response with status "200"
        Then the device has the following parameters:
            | ip       | mac               | plugin | model     | vendor     | version | template_id |
            | 10.1.0.1 | aa:11:22:33:44:55 | null   | nullmodel | nullvendor | 1.0     | None        |

    Scenario: Edit a device with an invalid mac
        Given I have the following devices:
            | mac               |
            | 00:11:22:33:44:55 |
        When I edit the device with mac "00:11:22:33:44:55" using the following parameters:
            | mac               |
            | ZZ:11:22:33:44:56 |
        Then I get a response with status "400"
        Then I get an error message "Invalid parameters: mac"
        When I edit the device with mac "00:11:22:33:44:55" using the following parameters:
            | mac                |
            | aa:110:22:33:44:56 |
        Then I get a response with status "400"
        Then I get an error message "Invalid parameters: mac"

    Scenario: Edit a device with a mac that already exists
        Given I have the following devices:
            | mac               |
            | 00:11:22:33:44:55 |
            | 00:11:22:33:44:56 |
        When I edit the device with mac "00:11:22:33:44:55" using the following parameters:
            | mac               |
            | 00:11:22:33:44:56 |
        Then I get a response with status "400"
        Then I get an error message "device 00:11:22:33:44:56 already exists"

    Scenario: Edit a device with an invalid ip
        Given I have the following devices:
            | mac               | ip       |
            | 00:11:22:33:44:55 | 10.0.0.1 |
        When I edit the device with mac "00:11:22:33:44:55" using the following parameters:
            | ip        |
            | 399.0.0.1 |
        Then I get a response with status "400"
        Then I get an error message "Invalid parameters: ip"
        When I edit the device with mac "00:11:22:33:44:55" using the following parameters:
            | ip          |
            | 10.9999.0.1 |
        Then I get a response with status "400"
        Then I get an error message "Invalid parameters: ip"

    Scenario: Edit a device with a template that does not exist
        Given I have the following devices:
            | mac               |
            | 00:11:22:33:44:55 |
        When I edit the device with mac "00:11:22:33:44:55" using the following parameters:
            | template_id          |
            | mysuperdupertemplate |
        Then I get a response with status "400"
        Then I get an error message "Nonexistent parameters: template_id mysuperdupertemplate does not exist"

    Scenario: Edit a device with a custom template
        Given there exists the following device templates:
            | id            | label          |
            | testtemplate  | Test Template  |
            | supertemplate | Super Template |
        Given I have the following devices:
            | mac               | template_id  |
            | 00:11:22:33:44:55 | testtemplate |
        When I edit the device with mac "00:11:22:33:44:55" using the following parameters:
            | template_id   |
            | supertemplate |
        Then I get a response with status "204"
        When I go get the device with mac "00:11:22:33:44:55" using its id
        Then I get a response with status "200"
        Then the device has the following parameters:
            | mac               | template_id |
            | 00:11:22:33:44:55 | None        |

    Scenario: Edit a device with a plugin that does not exist
        Given I have the following devices:
            | mac               |
            | 00:11:22:33:44:55 |
        When I edit the device with mac "00:11:22:33:44:55" using the following parameters:
            | plugin          |
            | mysuperplugin   |
        Then I get a response with status "400"
        Then I get an error message "Nonexistent parameters: plugin mysuperplugin does not exist"

    Scenario: Edit a device with a plugin
        Given the plugin "null" is installed
        Given the plugin "zero" is installed
        Given I have the following devices:
            | mac               | plugin |
            | 00:11:22:33:44:55 | null   |
        When I edit the device with mac "00:11:22:33:44:55" using the following parameters:
            | plugin |
            | zero   |
        Then I get a response with status "204"
        When I go get the device with mac "00:11:22:33:44:55" using its id
        Then I get a response with status "200"
        Then the device has the following parameters:
            | mac               | plugin |
            | 00:11:22:33:44:55 | zero   |

    Scenario: Get a device that doesn't exist
        Given there are no devices with id "1234567890abcdefghij1234567890ab"
        When I go get the device with id "1234567890abcdefghij1234567890ab"
        Then I get a response with status "404"

    Scenario: Get a device that exists
        Given there exists the following device templates:
            | id         | label       |
            | mytemplate | My Template |
        Given the plugin "null" is installed
        Given I have the following devices:
            | ip       | mac               | plugin | model     | vendor     | version | template_id |
            | 10.0.0.1 | 00:11:22:33:44:55 | null   | nullmodel | nullvendor | 1.0     | mytemplate  |
        When I go get the device with mac "00:11:22:33:44:55" using its id
        Then I get a response with status "200"
        Then I get a response with a link to the "devices" resource
        Then the device has the following parameters:
            | ip       | mac               | plugin | model     | vendor     | version | template_id |
            | 10.0.0.1 | 00:11:22:33:44:55 | null   | nullmodel | nullvendor | 1.0     | None        |

    Scenario: Device list with minimum 2 devices
        Given there exists the following device templates:
            | id         | label       |
            | mytemplate | My Template |
        Given the plugin "null" is installed
        Given I have the following devices:
            | ip       | mac               | plugin | model     | vendor     | version | template_id         |
            | 10.0.0.1 | 00:11:22:33:44:55 | null   | nullmodel | nullvendor | 1.0     | mytemplate          |
            | 10.0.0.2 | 00:11:22:33:44:56 | null   | nullmodel | nullvendor | 1.0     | defaultconfigdevice |
        When I request the list of devices
        Then I get a response with status "200"
        Then I get a list containing the following devices:
            | ip       | mac               | plugin | model     | vendor     | version | template_id |
            | 10.0.0.1 | 00:11:22:33:44:55 | null   | nullmodel | nullvendor | 1.0     | None        |
            | 10.0.0.2 | 00:11:22:33:44:56 | null   | nullmodel | nullvendor | 1.0     | None        |
        Then the list contains the same number of devices as on the provisioning server


    Scenario: Search for devices with HTTP_PROXY set
        Given I set the HTTP_PROXY environment variables to "10.99.99.99"
        When I request the list of devices
        Then I get a response with status "200"

    Scenario: Reset to autoprov a device
        Given there are no devices with id "123"
        Given there are no devices with mac "00:00:00:00:aa:01"
        Given I have the following devices:
          | id  | ip             | mac               |
          | 123 | 192.168.32.197 | 00:00:00:00:aa:01 |
        When I reset the device "123" to autoprov from restapi
        Then I see in the log file device "123" autoprovisioned

    Scenario: Associate line to a device
        Given I have the following lines:
            |     id | context | protocol | username | secret | device_slot |
            | 523478 | default | sip      | toto     | tata   |           1 |
        Given I have the following devices:
            |              id |       ip |               mac |
            | 658743288432479 | 10.0.0.1 | 00:00:00:00:00:12 |
        When I associate my line_id "523478" to the device "658743288432479"
        Then I get a response with status "403"

    Scenario: Remove line to a device
        Given I have the following lines:
            |     id | context | protocol | username | secret | device_slot |
            | 955473 | default | sip      | toto     | tata   |           1 |

        When I remove line_id "955473" from device "954743217965"
        Then I get a response with status "403"

    Scenario: Delete a device
        Given I have the following devices:
            |            id |       ip |               mac |
            | 1346771446546 | 10.0.0.1 | 00:00:00:00:00:12 |
        When I delete the device "1346771446546" from restapi
        Then I get a response with status "204"
        Then I see in the log file device "1346771446546" deleted
        Then the device "1346771446546" is no longer exists in provd

    Scenario: Delete a device that doesn't exist
        Given there are no devices with id "abcd"
        When I delete the device "abcd" from restapi
        Then I get a response with status "404"

    Scenario: Delete a device associated to a line
        Given I have the following devices:
            |            id |       ip |               mac |
            | 6521879216879 | 10.0.0.1 | 00:00:00:00:00:12 |
        Given there are users with infos:
            | firstname | lastname | number | context | protocol |            device |
            | Aayla     | Secura   |   1234 | default | sip      | 00:00:00:00:00:12 |
        When I delete the device "6521879216879" from restapi
        Then I get a response with status "400"
        Then I get an error message "Error while deleting device: device is still linked to a line"
