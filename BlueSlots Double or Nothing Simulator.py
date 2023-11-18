import random, os, time, math, winsound, subprocess
totalAttempts = 0
simulationsAmount = 1
calculationsAmount = 1
percentage = 1
price = 1
jackpot = 1
finishedCalculations = 0
grandTotalAttempts = 0
totalSimulationsAmount = None
initialTime = 0
days, hours, minutes, seconds = 0.0, 0.0, 0.0, 0
doLog = None
attemptsInSec = 0
maxTime = 0
linesplit = "------------------------------------------------------------"
calcFeedbacks = []
logfile = None

class UserAskedHelp(Exception):
    def __init__(self, message = ""):
        super().__init__(message)

def GetTotalTimeTaken(seconds):
    units = [
        ('year', 86400 * 7 * 52.178),
        ('month', 86400 * 7 * 4.348),
        ('week', 86400 * 7),
        ('day', 86400),
        ('hour', 3600),
        ('minute', 60),
        ('second', 1)
    ]
    result = []
    for unitName, unitSeconds in units:
        if seconds >= unitSeconds:
            unitCount = math.floor(seconds / unitSeconds)
            seconds %= unitSeconds
            if unitCount > 1:
                result.append(f"{unitCount} {unitName}s")
            else:
                result.append(f"{unitCount} {unitName}")
    if result:
        return ', '.join(result)
    else:
        return "0 seconds"

def PrintSimulationsprocessETA(i):
    global days, hours, minutes, seconds, maxTime
    seconds = i
    if seconds is None:
        return
    days = seconds / 86400
    hours = (seconds % 86400) / 3600
    minutes = ((seconds % 86400) % 3600) / 60
    if maxTime < seconds:
        maxTime = seconds
    if seconds > (86400 * 7 * 52.178):
        years = seconds / (86400 * 7 * 52.178)
        print(f'{format(grandTotalAttempts, ",d")} calculations done | ETA: {math.ceil(round(years, 2) * 10) / 10} year(s) (you will need a quantum computer){" " * 5}', end="\r")
    elif seconds > 86400 * 7 * 4.348:
        months = seconds / (86400 * 7 * 4.348)
        print(f'{format(grandTotalAttempts, ",d")} calculations done | ETA: {math.ceil(round(months, 2) * 10) / 10} month(s) (you might need a quantum computer){" " * 5}', end="\r")
    elif seconds > 86400 * 7:
        weeks = seconds / (86400 * 7)
        print(f'{format(grandTotalAttempts, ",d")} calculations done | ETA: {math.ceil(round(weeks, 2) * 10) / 10} week(s){" " * 50}', end="\r")
    elif seconds > (86400 * 2):
        print(f'{format(grandTotalAttempts, ",d")} calculations done | ETA: {math.ceil(round(days, 2) * 10) / 10} days{" " * 50}', end="\r")
    elif seconds > 86400:
        print(f'{format(grandTotalAttempts, ",d")} calculations done | ETA: {math.floor(days)} day, {math.ceil(round(hours, 2) * 10) / 10} hr(s){" " * 50}', end="\r")
    elif seconds > 3600:
        print(f'{format(grandTotalAttempts, ",d")} calculations done | ETA: {math.floor(hours)} hr(s), {math.ceil(minutes)} min(s){" " * 50}', end="\r")
    elif seconds > 60:
        print(f'{format(grandTotalAttempts, ",d")} calculations done | ETA: {math.ceil(round(minutes, 2) * 10) / 10} min(s){" " * 50}', end="\r")
    else:
        print(f'{format(grandTotalAttempts, ",d")} calculations done | ETA: {math.ceil(round(seconds, 0))} second(s){" " * 50}', end="\r")

def GetSimulationsprocessETA(override):
    global attemptsInSec, initialTime
    if override is True:
        if totalSimulationsAmount < grandTotalAttempts:
            print(f'{format(grandTotalAttempts, ",d")} calculations done | ETA: Now{" " * 50}', end="\r")
        else:
            PrintSimulationsprocessETA(seconds)
    if time.time() - initialTime > 1 and time.time() - initialTime < 5:
        if totalSimulationsAmount < grandTotalAttempts:
            print(f'{format(grandTotalAttempts, ",d")} calculations done | ETA: Now{" " * 50}', end="\r")
            initialTime = 0
        else:
            timeForTheRest = (time.time() - initialTime) * ((totalSimulationsAmount - grandTotalAttempts) / attemptsInSec)
            PrintSimulationsprocessETA(timeForTheRest)
            attemptsInSec = 0
            initialTime = 0
    elif initialTime == 0:
        initialTime = time.time()

def GetRequiredsimulationsAmount(chancePerSim):
    totalSims = simulationsAmount * calculationsAmount
    requiredsimulationsAmount = totalSims * (100 / chancePerSim)
    return math.ceil(requiredsimulationsAmount)

def StartSimulatingsimulationsAmount():
    totalSims = simulationsAmount * calculationsAmount
    return totalSims

def GetUserInput():
    global simulationsAmount, multiplier, percentage, price, calculationsAmount, jackpot, totalSimulationsAmount, decimalPlaces, targetPercentage
    while True:
        try:
            # Multiplier
            multiplier = input("When to cash in: 1-9 (9 = jackpot): ")
            if multiplier.lower() == "help":
                os.system('cls')
                print("This simulates a 'player' continuously playing the machine.\nSet player can cash in at any time.\nBy choosing 1, the 'player' will always cash in at 2X.\nBy choosing 9, the 'player' will go for jackpot (9X).")
                input("\nPress enter to try again ")
                raise UserAskedHelp()
            multiplier = int(multiplier)
            if multiplier > 9 or multiplier < 1:
                raise ValueError(f"Value {multiplier} of type {type(multiplier)} is not in range(1-9)")
            # Jackpot
            jackpot = input("Jackpot amount: ")
            if jackpot.lower() == "help":
                os.system('cls')
                print("The jackpot is the amount of money the 'player' will receive upon reaching 9X.")
                input("\nPress enter to try again")
                raise UserAskedHelp()
            jackpot = int(jackpot)
            if jackpot < 0:
                raise ValueError(f"Value {jackpot} of type {type(jackpot)} can not be negative")
            # Calculation amount
            calculationsAmount = input("Amount of calculations: ")
            if calculationsAmount.lower() == "help":
                os.system('cls')
                print(f"The program will have calculations and simulations.\nEvery calculation has an amount of simulations inside them.\nSay you chose 5 calculations and 2 simulations:\nThe program will then do 10 total simulations of a player reaching {multiplier}X.\n")
                print(f"These will be separated like this:\n")
                for i in range(0, 5):
                    print(f"Calculating #{i+1} <--- (CALCULATION {i+1})\n...$ with ... total attempts <--- (2 SIMULATIONS)")
                print("Using 10+ calculations is recommended for better results.")
                input("\nPress enter to try again ")
                raise UserAskedHelp()
            calculationsAmount = int(calculationsAmount)
            if calculationsAmount <= 0:
                raise ValueError(f"Value {calculationsAmount} of type {type(calculationsAmount)} can not be negative")
            # simulationsAmount
            simulationsAmount = input("Amount of calculations: ")
            if simulationsAmount.lower() == "help":
                os.system('cls')
                print(f"The program will have calculations and simulations.\nEvery calculation has an amount of simulations inside them.\nSay you chose 5 calculations and 2 simulations:\nThe program will then do 10 total simulations of a player reaching {multiplier}X.\n")
                print(f"These will be separated like this:\n")
                for i in range(0, 5):
                    print(f"Calculating #{i+1} <--- (CALCULATION {i+1})\n...$ with ... total attempts <--- (2 SIMULATIONS)")
                print("Using 10+ calculations is recommended for better results.")
                input("\nPress enter to try again ")
            simulationsAmount = int(simulationsAmount)
            if simulationsAmount <= 0:
                raise ValueError(f"Value {simulationsAmount} of type {type(simulationsAmount)} can not be negative")
            # Percentage
            percentage = input("Win rate percentage (per attempt): ")
            if percentage.lower() == "help":
                os.system('cls')
                print("The chance of going from 2X to 3X or from 3X to 4X etc.\nPercentage can be a float or int")
                input("\nPress enter to try again")
                raise UserAskedHelp()
            percentage = float(percentage)
            if percentage <= 0 or percentage > 100:
                raise ValueError(f"Value {percentage} of type {type(percentage)} is not in range(0-100)")
            # Price
            price = input("Price per use: ")
            if price.lower() == "help":
                os.system('cls')
                print("The price the user has to pay every time he starts another game.\nUser pays every time he starts from 1X.")
                input("\nPress enter to try again")
                raise UserAskedHelp()
            price = int(price)
            if price < 1:
                raise ValueError(f"Value {price} of type {type(price)} is not larger than 0")
            if doLog:
                logs = open(logfile, "a")
                logs.write(f'Number: {str(multiplier)}\nJackpot amount: {str(jackpot)}\nSims per calculation: {str(simulationsAmount)}\nAmount of calculations: {str(calculationsAmount)}\nWin rate percentage: {str(percentage)}\nPrice per use: {str(price)}\n\n')
                logs.close()
            chancePerSim = (((percentage / 100) ** multiplier) * 100)
            totalSimulationsAmount = GetRequiredsimulationsAmount(chancePerSim)
            print("Winning chance per simulation: ", chancePerSim, "%")
            print("Average amount of calculations: ", format(totalSimulationsAmount, ",d"))
            break
        except TypeError as e:
            input(f"Error: {e}")
            os.system('cls')
        except ValueError as e:
            input(f"Error: {e}")
            os.system('cls')
        except UserAskedHelp:
            os.system('cls')
    if '.' in str(percentage):
        decimalPosition = str(percentage).index('.')
        decimalPlaces = (len(str(percentage)) - decimalPosition - 1) + 2
    else:
        decimalPlaces = 2
    targetPercentage = int(str(percentage).replace(',', '').replace('.', ''))
    print("------------------------------------------------------------")

def StartSimulating(numb):
    global totalAttempts, grandTotal, finishedCalculations, grandTotalAttempts, attemptsInSec, calcFeedbacks
    print(f"Calculating #{numb}", " " * 50)
    if finishedCalculations != 0:
        GetSimulationsprocessETA(True)
    finishedCalculations += 1
    attempts = 0
    addup = []
    totalWon = 0
    totalLost = 0
    totalAttempts = 0
    for i in range(0, simulationsAmount):
        attempts = 0
        while True:
            isok = True
            totalAttempts = totalAttempts + 1
            attempts = attempts + 1
            grandTotalAttempts += 1
            attemptsInSec += 1
            GetSimulationsprocessETA(False)
            for i in range(0, multiplier):
                if random.randint(0, 10 ** decimalPlaces) <= targetPercentage:
                    addup.append(1)
                else:
                    addup.append(0)
            for i in addup:
                if i == 0:
                    isok = False
            addup = []
            if isok is True:
                break
        if multiplier == 9:
            totalWon = totalWon + jackpot
        else:
            totalWon = totalWon + price * (2 ** multiplier)
        totalLost = totalLost + price * attempts
    print(f'{format(totalWon - totalLost, ",d")}$ with {format(totalAttempts, ",d")} total attempts{" " * 50}')
    # Keep output in case of logging
    tempresult = f'{format(totalWon - totalLost, ",d")} with {format(totalAttempts, ",d")} total attempts'
    calcFeedbacks.append(tempresult)
    grandTotal = grandTotal + totalWon - totalLost

def AskYesNo(Question):
    while True:
        try:
            userInput = str(input(Question))
            if userInput.lower() == "y":
                return True
            elif userInput.lower() == "n":
                return False
            raise ValueError(f"Value {userInput} is not 'y' or 'n'")
        except ValueError as e:
            print(f"Error: {e}")

def AskToLog():
    global doLog, logfile
    doLog = False
    if AskYesNo("Would you like to log the results? (y/n): "):
        doLog = True
    if doLog:
        if not os.path.exists("Logs"):
            os.makedirs("Logs")
        i = len(os.listdir("Logs")) + 1
        open('Logs\log_' + str(i) + '.txt', "w")
        logfile = 'Logs\log_' + str(i) + '.txt'
        print(f"Created Logs\log_{i}")

def ResetVariables():
    global finishedCalculations, grandTotalAttempts, initialTime, days, hours, minutes, seconds, attemptsInSec, maxTime, grandTotal, doLog, calcFeedbacks
    finishedCalculations = 0
    grandTotalAttempts = 0
    initialTime = 0
    days, hours, minutes = 0.0, 0.0, 0.0
    seconds = None
    attemptsInSec = 0
    maxTime = 0
    grandTotal = 0
    doLog = False
    calcFeedbacks = []

def StartProgram():
    ResetVariables()
    GetUserInput()
    totalTime = time.time()
    for i in range(0, calculationsAmount):
        StartSimulating(i + 1)
    timeFinished = time.time()
    print("\n")
    if grandTotal > 0:
        print("Total profit:", format(grandTotal, ",d"), " " * 50)
        print(f"Average profit per simulation: {format(round(abs(grandTotal / StartSimulatingsimulationsAmount())), ',.0f')}")
        if doLog:
            tempresult = f'\nTotal profit: {format(grandTotal, ",.2f")}\nAverage profit per simulation: {format(round(abs(grandTotal / StartSimulatingsimulationsAmount())), ",.0f")}\nAverage attempts per simulation: {format(math.ceil(grandTotalAttempts / (simulationsAmount * calculationsAmount)), ",.0f")}\n{linesplit}\nTotal calculations done: {format(abs(grandTotalAttempts), ",d")}\n{linesplit}\nTotal time taken: {GetTotalTimeTaken(timeFinished - totalTime)}'
    if grandTotal < 0:
        print("Total loss:", format(abs(grandTotal), ",d"), " " * 50)
        print(f"Average loss per simulation: {format(round(abs(grandTotal / StartSimulatingsimulationsAmount())), ',.0f')}")
        if doLog:
            tempresult = f'\nTotal loss: {format(abs(grandTotal), ",.2f")}\nAverage loss per simulation: {format(round(abs(grandTotal / StartSimulatingsimulationsAmount())), ",.0f")}\nAverage attempts per simulation: {format(math.ceil(grandTotalAttempts / (simulationsAmount * calculationsAmount)), ",.0f")}\n{linesplit}\nTotal calculations done: {format(abs(grandTotalAttempts), ",d")}\n{linesplit}\nTotal time taken: {GetTotalTimeTaken(timeFinished - totalTime)}'
    print(f"Average attempts per simulation: {format(math.ceil(grandTotalAttempts / (simulationsAmount * calculationsAmount)), ',.0f')}")
    print(linesplit)
    print(f"Total calculations done: {format(abs(grandTotalAttempts), ',d')}")
    print(f"Estimated calculations: {format(abs(totalSimulationsAmount), ',d')}")
    print(linesplit)
    print(f"Total time taken: {GetTotalTimeTaken(time.time() - totalTime)}")
    print(f"Estimated time: {GetTotalTimeTaken(maxTime)}")
    print(linesplit)
    if grandTotalAttempts == totalSimulationsAmount:
        print(f"ETA was 100% accurate")
    elif grandTotalAttempts < totalSimulationsAmount:
        print(f"ETA was {math.floor((grandTotalAttempts / totalSimulationsAmount) * 10000) / 100}% accurate")
    else:
        print(f"ETA was {math.floor((totalSimulationsAmount / grandTotalAttempts) * 10000) / 100}% accurate")
    #Ask user to log and log if approved
    AskToLog()
    if doLog:
        logs = open(logfile, "a")
        #Log the user input
        logs.write(f'Number: {str(multiplier)}\nJackpot amount: {str(jackpot)}\nSims per calculation: {str(simulationsAmount)}\nAmount of calculations: {str(calculationsAmount)}\nWin rate percentage: {str(percentage)}\nPrice per use: {str(price)}\n\n')
        #Log all the feedback lines of the calcs and sims
        for tempresult in calcFeedbacks:
            logs.write(f'{str(tempresult)}\n')
        #Log the resulting data of the session
        if grandTotal > 0:
            tempresult = f'\nTotal profit: {format(grandTotal, ",.2f")}\nAverage profit per simulation: {format(round(abs(grandTotal / StartSimulatingsimulationsAmount())), ",.0f")}\nAverage attempts per simulation: {format(math.ceil(grandTotalAttempts / (simulationsAmount * calculationsAmount)), ",.0f")}\n{linesplit}\nTotal calculations done: {format(abs(grandTotalAttempts), ",d")}\n{linesplit}\nTotal time taken: {GetTotalTimeTaken(timeFinished - totalTime)}'
            logs.write(f'{str(tempresult)}\n')
        if grandTotal < 0:
            tempresult = f'\nTotal loss: {format(abs(grandTotal), ",.2f")}\nAverage loss per simulation: {format(round(abs(grandTotal / StartSimulatingsimulationsAmount())), ",.0f")}\nAverage attempts per simulation: {format(math.ceil(grandTotalAttempts / (simulationsAmount * calculationsAmount)), ",.0f")}\n{linesplit}\nTotal calculations done: {format(abs(grandTotalAttempts), ",d")}\n{linesplit}\nTotal time taken: {GetTotalTimeTaken(timeFinished - totalTime)}'
            logs.write(f'{str(tempresult)}\n')
        logs.close()
        winsound.PlaySound(os.environ['SystemDrive'] + '\Windows\Media\Windows Background.wav', winsound.SND_ALIAS)
        if AskYesNo("Open logs folder? (y/n): "):
            subprocess.Popen(['explorer', 'Logs'], shell=True)
    input("Press enter to retry")
    
    os.system('cls')
    StartProgram()

def PrintInfo():
    os.system('cls')
    print("Welcome to the BlueSlots Double or Nothing simulator\nThis program simulates a player continuously using the Double or Nothing slot machine\nJust choose your settings and conditions and the program will start the simulations\nIf you need an explanation with a condition, type 'help'\nYou can log your results when the program is finished if necessary\nFor feedback or bug reports, contact me on discord: mathscalculator")
    input("\nPress enter to continue...")
    os.system('cls')

if __name__ == "__main__":
    PrintInfo()
    StartProgram()