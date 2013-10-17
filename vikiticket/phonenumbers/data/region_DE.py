"""Auto-generated file, do not edit by hand. DE metadata"""
from phonenumbers import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_DE = PhoneMetadata(id='DE', country_code=49, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='[1-35-9]\\d{3,13}|4(?:[0-8]\\d{4,12}|9(?:4[1-8]|[0-35-7]\\d)\\d{2,7})', possible_number_pattern='\\d{2,14}'),
    fixed_line=PhoneNumberDesc(national_number_pattern='[246]\\d{5,13}|3(?:[03-9]\\d{4,11}|2\\d{9})|5(?:0[2-8]|[38][0-8]|[124-6]\\d|[79][0-7])\\d{3,10}|7(?:0[2-8]|[1-9]\\d)\\d{3,10}|8(?:0[2-9]|[1-9]\\d)\\d{3,10}|9(?:0[6-9]|[1-9]\\d)\\d{3,10}', possible_number_pattern='\\d{2,14}', example_number='30123456'),
    mobile=PhoneNumberDesc(national_number_pattern='1(?:5\\d{9}|7(?:[0-57-9]|6\\d)\\d{7}|6(?:[02]\\d{7,8}|3\\d{7}))', possible_number_pattern='\\d{10,11}', example_number='15123456789'),
    toll_free=PhoneNumberDesc(national_number_pattern='800\\d{7,9}', possible_number_pattern='\\d{10,12}', example_number='8001234567'),
    premium_rate=PhoneNumberDesc(national_number_pattern='900(?:[135]\\d{6}|9\\d{7})', possible_number_pattern='\\d{10,11}', example_number='9001234567'),
    shared_cost=PhoneNumberDesc(national_number_pattern='180\\d{5,11}', possible_number_pattern='\\d{8,14}', example_number='18012345'),
    personal_number=PhoneNumberDesc(national_number_pattern='700\\d{8}', possible_number_pattern='\\d{11}', example_number='70012345678'),
    voip=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    pager=PhoneNumberDesc(national_number_pattern='16(?:4\\d{1,10}|[89]\\d{1,11})', possible_number_pattern='\\d{4,14}', example_number='16412345'),
    uan=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    no_international_dialling=PhoneNumberDesc(national_number_pattern='NA', possible_number_pattern='NA'),
    national_prefix=u'0',
    national_prefix_for_parsing=u'0',
    number_format=[NumberFormat(pattern='(\\d{2})(\\d{4,11})', format=u'\\1/\\2', leading_digits_pattern=['3[02]|40|[68]9'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='(\\d{3})(\\d{3,10})', format=u'\\1/\\2', leading_digits_pattern=['2(?:\\d1|0[2389]|1[24]|28|34)|3(?:[3-9][15]|40)|[4-8][1-9]1|9(?:06|[1-9]1)'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='(\\d{4})(\\d{2,8})', format=u'\\1/\\2', leading_digits_pattern=['[24-6]|[7-9](?:\\d[1-9]|[1-9]\\d)|3(?:[3569][02-46-9]|4[2-4679]|7[2-467]|8[2-46-8])', '[24-6]|[7-9](?:\\d[1-9]|[1-9]\\d)|3(?:3(?:0[1-467]|2[127-9]|3[124578]|[46][1246]|7[1257-9]|8[1256]|9[145])|4(?:2[135]|3[1357]|4[13578]|6[1246]|7[1356]|9[1346])|5(?:0[14]|2[1-3589]|3[1357]|4[1246]|6[1-4]|7[1346]|8[13568]|9[1246])|6(?:0[356]|2[1-489]|3[124-6]|4[1347]|6[13]|7[12579]|8[1-356]|9[135])|7(?:2[1-7]|3[1357]|4[145]|6[1-5]|7[1-4])|8(?:21|3[1468]|4[1347]|6[0135-9]|7[1467]|8[136])|9(?:0[12479]|2[1358]|3[1357]|4[134679]|6[1-9]|7[136]|8[147]|9[1468]))'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='(\\d{5})(\\d{1,6})', format=u'\\1/\\2', leading_digits_pattern=['3'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='([18]\\d{2})(\\d{7,9})', format=u'\\1 \\2', leading_digits_pattern=['1[5-7]|800'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='(\\d{3})(\\d)(\\d{4,10})', format=u'\\1 \\2 \\3', leading_digits_pattern=['(?:18|90)0', '180|900[1359]'], national_prefix_formatting_rule=u'0\\1'),
        NumberFormat(pattern='(700)(\\d{4})(\\d{4})', format=u'\\1 \\2 \\3', leading_digits_pattern=['700'], national_prefix_formatting_rule=u'0\\1')])
