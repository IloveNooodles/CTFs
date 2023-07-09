# # Source Generated with Decompyle++
# # # File: mencariPW.pyc (Python 3.10)

# import tkinter
# import string
# from tkinter import messagebox
# window = tkinter.Tk()
# window.title('Login form')
# window.geometry('340x440')
# window.configure('#333333', **('bg',))

# def login():
#     username = 'TechnoFairCTF'
#     password = [
#         'qswaefrdthy_gukojplzcxvbmn',
#         'pkolihu_jyftgrsedwaqmzbxvc',
#         'mlnkbjvhcgxfzdsapqowueyr_t',
#         'plokijuhygtfrdeswaqmnbvcxz',
#         'qswdefrgthyjukilopmnbzvcx_',
#         'qswaefrgthyjukilpom_znxbcv',
#         'zqwsedrftgyhuji_kolpxcvbnm',
#         'qaedwsrf_tgujyhikpomznxbcv',
#         'mxnzbcvqsplokwdij_efuhrgyt',
#         'plokmnzbxvcijuygtfrdeswa_q',
#         'plmoknijbuhvygctfxrdzeswaq',
#         'qazwsxedcrfvtgbyhnujmikol_',
#         'wqzsxedcrfvt_gbyhnujmikolp',
#         'qazwxedcrf_vtgbyhnplmokiju',
#         'okmplijnuhbygvtfcrdxewqaz_',
#         'ygvtfcrd_xeszqaplmoknijbuh',
#         'ijnkmpluhbygvtfc_rdxeszwqa',
#         'tyuioplkjhgfdsaqwezxcvb_nm',
#         'mkolpijnuhbygv_tfcrxeszwaq',
#         'hubijnmkoplygvtfcrdxeszwaq',
#         'swxedcr_fvtgbynujmikolpqaz',
#         'trqwyuioplkjhgfdsazxcvbn_m',
#         'klopmijn_ubygvtfcrdxeszaqw',
#         'bvnmczxlaksjdhfgp_qowiruty']
#     entered_username = username_entry.get()
#     entered_password = password_entry.get()
#     if entered_username != username:
#         messagebox.showerror('Error', 'Invalid Login', **('title', 'message'))
#         return None
#     if len(entered_password) < 8 and len(entered_password) < 24 or len(entered_password) > 24:
#         messagebox.showerror('Error', 'Password di antara 1 sampai 24 karakter.', **('title', 'message'))
#         return None
#     for char, pw_string in zip(entered_password, password):
#         print(char, pw_string)
#         if char in pw_string or char not in string.ascii_lowercase + '_':
#             print("salah")

#         print('GG gaming abang heker \nTechnoFairCTF{%s}' % entered_password)
#         return None



from string import ascii_lowercase

password = [
        'qswaefrdthy_gukojplzcxvbmn',
        'pkolihu_jyftgrsedwaqmzbxvc',
        'mlnkbjvhcgxfzdsapqowueyr_t',
        'plokijuhygtfrdeswaqmnbvcxz',
        'qswdefrgthyjukilopmnbzvcx_',
        'qswaefrgthyjukilpom_znxbcv',
        'zqwsedrftgyhuji_kolpxcvbnm',
        'qaedwsrf_tgujyhikpomznxbcv',
        'mxnzbcvqsplokwdij_efuhrgyt',
        'plokmnzbxvcijuygtfrdeswa_q',
        'plmoknijbuhvygctfxrdzeswaq',
        'qazwsxedcrfvtgbyhnujmikol_',
        'wqzsxedcrfvt_gbyhnujmikolp',
        'qazwxedcrf_vtgbyhnplmokiju',
        'okmplijnuhbygvtfcrdxewqaz_',
        'ygvtfcrd_xeszqaplmoknijbuh',
        'ijnkmpluhbygvtfc_rdxeszwqa',
        'tyuioplkjhgfdsaqwezxcvb_nm',
        'mkolpijnuhbygv_tfcrxeszwaq',
        'hubijnmkoplygvtfcrdxeszwaq',
        'swxedcr_fvtgbynujmikolpqaz',
        'trqwyuioplkjhgfdsazxcvbn_m',
        'klopmijn_ubygvtfcrdxeszaqw',
        'bvnmczxlaksjdhfgp_qowiruty']

charset = ascii_lowercase + '_'

ans = ""
for p in password:
  for c in charset:
    if c not in p:
      ans += c
      
print(ans)
