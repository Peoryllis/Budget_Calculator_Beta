import math

def convert_to_binary(num):

    originalNumber = num

    if num == 0:
        return "0000 0000"
    
    numIterations = math.ceil(num / 255)

    valuesList = list(255 for entry in range(numIterations - 1))

    valuesList.append(originalNumber - 255 * (numIterations - 1))

    result = ""

    for value in valuesList:
        power = 7
        currentValue = value
        for bit in range(8):

            if 2 ** power > currentValue:
                result += "0"
            else:
                result += "1"
                currentValue -= 2 ** power
            
            power -= 1

            if bit == 3: result += " "

        result += " "

    return result




print(convert_to_binary(357))