
Given Basic Auth "{username}" "{password}"
=============================================================================================================

Usage example
-------------

```
Feature: zato-apitest docs

Scenario: Given Basic Auth "{username}" "{password}"

    Given address "http://apitest-demo.zato.io"
    Given URL path "/demo/json"
    Given format "JSON"
    Given Basic Auth "MyUser" "MyPassword"

    When the URL is invoked

    Then status is "200"
```

Discussion
----------

(None)