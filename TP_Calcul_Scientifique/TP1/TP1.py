from TP_Calcul_Scientifique.TP1.TP1 import Password

niveau = 1
p = Password(niveau)
pw = ['']

################################ NIVEAU 0 ####################################


# for mot in 'abcdefghijklmnopqrstuvwxyz' :
#     pw[0] = mot
#     if p.check(pw) >= 0 :                 # if execute si p.check(pw) diff de
#         print("niveau1 donne =",p.check(pw))
#         break

################################ NIVEAU 1 ####################################

#for i in 'abcdefghijklmnopqrstuvwxyz' :
#    for j in 'abcdefghijklmnopqrstuvwxyz' :
#        for k in 'abcdefghijklmnopqrstuvwxyz' :
#            pw = [i,j,k]
#            if p.check(pw) >= 0 :
#                print("niveau1 donne =",p.check(pw))
#                break

################################ NIVEAU 2 ###################################

# for i in '0123456789' :
#     for j in '0123456789' :
#         for k in '0123456789' :
#             for l in '0123456789' :
#                 for m in '0123456789' :
#                     for n in '0123456789' :
#                         pw = [i,j,k,l,m,n]
#                         if p.check(pw) >= 0 :
#                             print("niveau2 donne =",p.check(pw))
#                             break

# astuce :

#for i in range(1000000):
#    pw = list((6 - len(str(i))) * '0' + (str(i)))
#    resultat_check = p.check(pw)
#    if resultat_check >= 0:
#       print("niveau2 donne =", resultat_check)
#        break

############################### NIVEAU 3 ####################################