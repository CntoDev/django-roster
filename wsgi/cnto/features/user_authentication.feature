Feature: User authentication
  In order to ensure the safety of community member's privacy
  As a community administrator
  I want users to be authenticated before accessing the roster

  Scenario: Access a restricted page without being authenticated
    When accessing a restricted page
    Then the user is redirected to the login page
