# OTP Collection

The collection of OTPs in both Django and Django rest framework.

I will implement the **`Services, Repositories`** design pattern for this project.

## Django

This app contains 2-factor-AUTH for Users, OTP-account-verification and OTP-reset-password.

The token that is created, would be expire in 3 minutes (180 seconds).
You can change this interval in `utils.py`.

You may ask yourself : Where is twilio settings? well ...
The answer is : I'm from Iran :( .... I can't access to these services

BUT

I provide you some resources that could help you in this :

                    https://www.twilio.com/en-us/blog/enable-multiple-otp-methods-django

                    https://www.youtube.com/watch?v=UKTqfhbb9gM

                    https://www.twilio.com/docs/api/rest/sending-messages

                    https://stackoverflow.com/questions/26718151/one-time-user-authentication-with-sms-using-django-and-twilio

                    https://medium.com/@EphraimBuddy/building-a-real-world-phone-verification-api-endpoints-with-django-rest-framework-839c5e8ffb0b

                    https://studygyaan.com/django/login-with-otp-via-email-phone-in-django-rest-framework

I hope these links be useful to you :)

### for Iranians

for add send sms into your Django app see this :

https://github.com/IPeCompany/SmsPanelV2.Python

for more information see :

https://sms.ir

### 2-FACTOR-AUTHENTICATION

If you wanna find 2-factor auth, search in views.py for this comment :

`TODO : Authentication`

### OTP-Account-Verification

If you wanna find the OTP-Registeration, search in views.py for this comment :

`TODO : Registeration`

### OTP-Reset-Password

If you wanna find OTP-Reset-Password, search in views.py for this comment :

`TODO : Reset_Password`

### How to use this project ?

#### first fill up some settings in `settings.py` like SECRET_KEY

#### change the `interval` in the `utils.py` as you please

## DRF

In **`DRF`**, since we will work with **`JWT`** and we don't need `is_active` status,
I will remove needing to password, instead I will use **`get_or_create`** function for it.
