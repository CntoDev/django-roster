from behave import given, when, then

@when(u'accessing a restricted page')
def step_impl(context):
    context.browser.visit(context.base_url + '/')

@then(u'the user is redirected to the login page')
def step_impl(context):
    assert context.browser.url.endswith('/login/')
