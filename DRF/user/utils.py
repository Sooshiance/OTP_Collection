import datetime

from django.utils import timezone

import pyotp

from .models import User, OTP

# from sms_ir import SmsIr


def sendToken(user:User):
    try:
        otp = OTP.objects.get(user=user)
        access_time = (datetime.timedelta(minutes=1) + otp.created_at).timestamp()
        delta_time = access_time - timezone.now().timestamp()
        if delta_time > 0:
            return {'error': f"waite : {delta_time} seconds", 'otp': False}
        else:
            otp.delete()
    except OTP.DoesNotExist:
        pass

    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)

    otp = totp.now()

    OTP.objects.create(user=user, otp=otp).save()

    user.otp = otp

    # TODO : send a SMS to User's verified Mobile number

    # sms = SmsIr(api_key="", linenumber=user.username)

    # sms.send_sms(number=user.mobile, message="""
    #             کد تایید شما در سامانه
    #         """, linenumber=user.phone)

    return {'otp': otp, 'error': False}
