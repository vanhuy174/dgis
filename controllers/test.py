ones = ["", "một", "hai ", "ba ", "bốn ", "năm ", "sáu ", "bảy ", "tám ", "chín ", "mười ", "mười một ",
            "mười hai ", "mười ba ", "mười bốn ", "mười lăm ", "mười sáu ", "mười bảy ", "mười tám ", "mười chín "]

twenties = ["", "", "hai mươi ", "ba mươi ", "bốn mươi ", "năm mươi ", "sáu mươi ", "bảy mươi ", "tám mươi ", "chín mươi "]

thousands = ["", "nghìn ", "triệu ", "tỉ ", "nghìn tỉ ", "quadrillion ", "quintillion ", "sextillion ",
                 "septillion ", "octillion ", "nonillion ", "decillion ", "undecillion ", "duodecillion ",
                 "tredecillion ", "quattuordecillion ", "quindecillion", "sexdecillion ", "septendecillion ",
                 "octodecillion ", "novemdecillion ", "vigintillion "]

def num999(n):
    c = n % 10  # singles digit
    b = ((n % 100) - c) / 10  # tens digit
    a = ((n % 1000) - (b * 10) - c) / 100  # hundreds digit
    t = ""
    h = ""
    if a != 0 and b == 0 and c == 0:
        t = ones[a] + "hundred "
    elif a != 0:
        t = ones[a] + "hundred and "
    if b <= 1:
        h = ones[n % 100]
    elif b > 1:
        h = twenties[b] + ones[c]
    st = t + h
    return st

# def num2word(num):
#     if num == 0: return 'zero'
#     i = 3
#     n = str(num)
#     word = ""
#     k = 0
#     while (i == 3):
#         nw = n[-i:]
#         n = n[:-i]
#         if int(nw) == 0:
#             word = num999(int(nw)) + thousands[int(nw)] + word
#         else:
#             word = num999(int(nw)) + thousands[k] + word
#         if n == '':
#             i = i + 1
#         k += 1
#     return word[:-1]


def num2words(num):
    under_20 = ['không', "một", "hai ", "ba ", "bốn ", "năm ", "sáu ", "bảy ", "tám ", "chín ", "mười ", "mười một ",
            "mười hai ", "mười ba ", "mười bốn ", "mười lăm ", "mười sáu ", "mười bảy ", "mười tám ", "mười chín "]
    tens = ["hai mươi ", "ba mươi ", "bốn mươi ", "năm mươi ", "sáu mươi ", "bảy mươi ", "tám mươi ", "chín mươi "]
    above_100 = {100: 'trăm', 1000: 'nghìn', 1000000: 'triệu', 1000000000: 'tỉ'}

    if num < 20:
        return under_20[num]

    if num < 100:
        return tens[(int)(num / 10) - 2] + ('' if num % 10 == 0 else ' ' + under_20[num % 10])

    # find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
    pivot = max([key for key in above_100.keys() if key <= num])

    return num2words((int)(num / pivot)) + ' ' + above_100[pivot] + (
        '' if num % pivot == 0 else ' ' + num2words(num % pivot))
print(num2words(20156))

